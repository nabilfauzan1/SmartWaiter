"""
services/menu_service.py — Menu loading, validation, and pandas-based filtering.

All menu data is read from data/menu.csv.
This module performs deterministic, code-level filtering so the LLM
never receives menu items that violate the customer's constraints.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

import config
from utils.formatter import normalize_allergen


# ── Loading & Validation ──────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_menu() -> tuple[pd.DataFrame | None, str | None]:
    """Load and validate menu.csv.

    Returns:
        (DataFrame, None)  on success.
        (None, error_msg)  on failure.
    """
    try:
        df = pd.read_csv(config.MENU_CSV_PATH)
    except FileNotFoundError:
        return None, "❌ Menu file not found. Please contact restaurant management."
    except Exception as exc:
        return None, f"❌ Could not read menu file: {exc}"

    missing = [col for col in config.REQUIRED_MENU_COLUMNS if col not in df.columns]
    if missing:
        return None, f"❌ Menu file is missing required columns: {', '.join(missing)}"

    # Normalize text columns
    df["halal"] = df["halal"].astype(str).str.strip()
    df["vegetarian"] = df["vegetarian"].astype(str).str.strip()
    df["availability"] = df["availability"].astype(str).str.strip()
    df["chef_recommendation"] = df["chef_recommendation"].astype(str).str.strip()
    df["contains"] = df["contains"].fillna("None").astype(str).str.strip()
    df["spicy_level"] = pd.to_numeric(df["spicy_level"], errors="coerce").fillna(0).astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
    df["calories"] = pd.to_numeric(df["calories"], errors="coerce").fillna(0).astype(int)
    df["protein"] = pd.to_numeric(df["protein"], errors="coerce").fillna(0).astype(float)

    return df, None


# ── Filtering ─────────────────────────────────────────────────────────────────

def filter_menu(df: pd.DataFrame, preferences: dict) -> pd.DataFrame:
    """Apply deterministic pandas filtering based on customer preferences.

    Filtering order (highest priority first):
      1. Allergies
      2. Availability
      3. Vegetarian
      4. Halal
      5. Budget
      6. Spicy level
      7. Calories (healthy/low-cal flag)

    Args:
        df:          Full menu DataFrame.
        preferences: Customer preference dict from session state.

    Returns:
        Filtered DataFrame (may be empty if no items match).
    """
    result = df.copy()

    # 1. Allergy filter — remove any row whose 'contains' field includes an allergen
    allergies: list[str] = preferences.get("allergies", [])
    if allergies:
        normalized_allergies = [a.lower().strip() for a in allergies]

        def contains_allergen(contains_str: str) -> bool:
            """Return True if the menu item contains a customer allergen."""
            if contains_str.lower() in ("none", "nan", ""):
                return False
            item_allergens = [c.lower().strip() for c in contains_str.split("|")]
            return any(allergen in item_allergens for allergen in normalized_allergies)

        result = result[~result["contains"].apply(contains_allergen)]

    # 2. Availability filter — only show available items
    result = result[result["availability"].str.lower() == "available"]

    # 3. Vegetarian filter
    if preferences.get("vegetarian"):
        result = result[result["vegetarian"].str.lower() == "yes"]

    # 4. Halal filter
    if preferences.get("halal_only"):
        result = result[result["halal"].str.lower() == "yes"]

    # 5. Budget filter
    budget: int | None = preferences.get("budget")
    if budget is not None:
        result = result[result["price"] <= budget]

    # 6. Spicy level filter
    spicy_max: int | None = preferences.get("spicy_level_max")
    if spicy_max is not None:
        result = result[result["spicy_level"] <= spicy_max]

    # 7. Healthy / low-calorie filter — prefer items <= 500 kcal but don't hard-exclude
    if preferences.get("healthy"):
        low_cal = result[result["calories"] <= 500]
        result = low_cal if not low_cal.empty else result

    return result.reset_index(drop=True)


def get_menu_context(df: pd.DataFrame) -> str:
    """Convert a (filtered) DataFrame to a readable text block for the LLM prompt."""
    if df.empty:
        return "No menu items match the current filters."

    lines: list[str] = ["=== AVAILABLE MENU ==="]
    for _, row in df.head(config.MAX_MENU_ROWS_IN_PROMPT).iterrows():
        allergen_info = row["contains"] if row["contains"].lower() not in ("none", "nan", "") else "None"
        line = (
            f"[{row['menu_id']}] {row['menu_name']} | {row['category']} | "
            f"Rp{row['price']:,} | {row['calories']} kcal | "
            f"Protein: {row['protein']}g | Spicy: {row['spicy_level']} | "
            f"Halal: {row['halal']} | Vegetarian: {row['vegetarian']} | "
            f"Contains: {allergen_info} | "
            f"Chef Pick: {row['chef_recommendation']} | "
            f"Desc: {row['description']}"
        )
        lines.append(line)
    return "\n".join(lines)
