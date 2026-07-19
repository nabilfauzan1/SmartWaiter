"""
utils/formatter.py — Helper functions for display formatting and data normalization.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

import config


# ── Currency Formatting ───────────────────────────────────────────────────────

def format_price(price: int | float) -> str:
    """Format an integer price as Indonesian Rupiah string."""
    return f"Rp{int(price):,}".replace(",", ".")


# ── Allergen Normalization ────────────────────────────────────────────────────

def normalize_allergen(raw: str) -> list[str]:
    """Split a 'contains' cell string by '|' and return clean canonical allergen names.

    Treats None / NaN / empty / 'None' as an empty list.
    """
    if not raw or str(raw).strip().lower() in ("none", "nan", ""):
        return []
    return [part.strip() for part in str(raw).split("|") if part.strip()]


# ── Spicy Level Display ───────────────────────────────────────────────────────

_SPICY_LABELS: dict[int, str] = {
    0: "🟢 Not Spicy",
    1: "🟡 Mild",
    2: "🟠 Medium",
    3: "🔴 Spicy",
    4: "🔥 Very Spicy",
    5: "💥 Extremely Spicy",
}


def spicy_label(level: int) -> str:
    """Return a human-readable spicy level label with emoji."""
    return _SPICY_LABELS.get(int(level), f"Level {level}")


# ── Restaurant Info Loading ───────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_restaurant_info() -> tuple[dict | None, str | None]:
    """Load and validate data/restaurant_info.json.

    Returns:
        (dict, None)       on success.
        (None, error_msg)  on failure.
    """
    try:
        with open(config.RESTAURANT_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None, "❌ Restaurant info file not found."
    except json.JSONDecodeError as exc:
        return None, f"❌ Restaurant info JSON is malformed: {exc}"
    except Exception as exc:
        return None, f"❌ Could not read restaurant info: {exc}"

    # Basic structural validation
    if "restaurant" not in data:
        return None, "❌ Restaurant info JSON is missing the 'restaurant' key."

    return data, None


# ── Greeting Loader ───────────────────────────────────────────────────────────

def load_greeting() -> str:
    """Load the greeting text from prompts/greeting.txt."""
    try:
        with open(config.GREETING_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return (
            "🍵 Irasshaimase! Welcome to Sorain Kitchen. "
            "I'm Sora, your AI Waiter today! How may I help you? 😊"
        )


# ── Preference Summary Display ────────────────────────────────────────────────

def preference_summary(preferences: dict) -> str:
    """Return a short human-readable string of active preferences for the sidebar."""
    parts: list[str] = []
    if preferences.get("budget"):
        parts.append(f"💰 Budget: {format_price(preferences['budget'])}")
    if preferences.get("vegetarian"):
        parts.append("🥦 Vegetarian")
    if preferences.get("halal_only"):
        parts.append("☪️ Halal only")
    if preferences.get("allergies"):
        parts.append(f"⚠️ Allergy: {', '.join(preferences['allergies'])}")
    if preferences.get("spicy_level_max") is not None:
        parts.append(f"🌶️ Max spicy: {preferences['spicy_level_max']}")
    if preferences.get("healthy"):
        parts.append("🥗 Healthy")
    if preferences.get("high_protein"):
        parts.append("💪 High protein")
    return "\n".join(parts) if parts else "No active preferences"
