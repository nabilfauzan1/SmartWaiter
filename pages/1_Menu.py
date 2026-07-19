"""
pages/1_Menu.py — Full menu browser with interactive filters.

Customers can filter by: category, price range, vegetarian, halal,
spicy level, chef recommendation, and availability.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from services.menu_service import load_menu
from utils.formatter import format_price, normalize_allergen, spicy_label
from utils.ui_helpers import inject_css

st.set_page_config(
    page_title="Menu — Sorain Kitchen",
    page_icon="🍣",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────────
inject_css()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <span class="page-header-icon">🍣</span>
        <h1>Our Menu</h1>
        <p class="page-subtitle">Sorain Kitchen — Modern Japanese Dining</p>
        <div class="restaurant-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Load Menu ─────────────────────────────────────────────────────────────────
menu_df, menu_error = load_menu()

if menu_error:
    st.error(menu_error)
    st.stop()

assert menu_df is not None  # satisfied by the error check above

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filter Menu")
    st.markdown("---")

    # Category
    categories = ["All"] + sorted(menu_df["category"].unique().tolist())
    selected_category = st.selectbox("Category", categories, key="menu_category")

    # Price range
    min_price = int(menu_df["price"].min())
    max_price = int(menu_df["price"].max())
    price_range = st.slider(
        "Price Range (Rp)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=1000,
        key="menu_price",
    )

    st.markdown("---")

    # Toggles
    veg_only = st.checkbox("🥦 Vegetarian Only", key="menu_veg")
    halal_only = st.checkbox("☪️ Halal Only", key="menu_halal")
    chef_only = st.checkbox("👨‍🍳 Chef Recommendation Only", key="menu_chef")
    avail_only = st.checkbox("✅ Available Only", value=True, key="menu_avail")

    st.markdown("---")

    # Spicy level
    max_spicy = st.slider("Max Spicy Level", 0, 5, 5, key="menu_spicy")

    st.markdown("---")
    if st.button("↩️ Reset Filters", key="reset_filters"):
        for key in ["menu_category", "menu_price", "menu_veg", "menu_halal",
                    "menu_chef", "menu_avail", "menu_spicy"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = menu_df.copy()

if selected_category != "All":
    filtered = filtered[filtered["category"] == selected_category]

filtered = filtered[
    (filtered["price"] >= price_range[0]) & (filtered["price"] <= price_range[1])
]

if veg_only:
    filtered = filtered[filtered["vegetarian"].str.lower() == "yes"]
if halal_only:
    filtered = filtered[filtered["halal"].str.lower() == "yes"]
if chef_only:
    filtered = filtered[filtered["chef_recommendation"].str.lower() == "yes"]
if avail_only:
    filtered = filtered[filtered["availability"].str.lower() == "available"]

filtered = filtered[filtered["spicy_level"] <= max_spicy]

# ── Results ───────────────────────────────────────────────────────────────────
st.markdown(f"**{len(filtered)} item(s) found**")

if filtered.empty:
    st.info("No menu items match your filters. Try adjusting the criteria. 🍵")
    st.stop()

# Group by category for cleaner layout
for category, group in filtered.groupby("category"):
    st.markdown(f"### {category}")
    for _, row in group.iterrows():
        allergens = normalize_allergen(row["contains"])
        allergen_str = ", ".join(allergens) if allergens else "None"
        is_available = row["availability"].strip().lower() == "available"
        is_chef = row["chef_recommendation"].strip().lower() == "yes"
        is_halal = row["halal"].strip().lower() == "yes"
        is_veg = row["vegetarian"].strip().lower() == "yes"

        badges = ""
        if is_available:
            badges += '<span class="badge badge-avail">✅ Available</span>'
        else:
            badges += '<span class="badge badge-unavail">❌ Unavailable</span>'
        if is_halal:
            badges += '<span class="badge badge-halal">☪️ Halal</span>'
        if is_veg:
            badges += '<span class="badge badge-veg">🥦 Vegetarian</span>'
        if is_chef:
            badges += '<span class="badge badge-chef">👨‍🍳 Chef\'s Pick</span>'

        st.markdown(
            f"""
            <div class="menu-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <strong style="font-size:1.05rem;">{row['menu_name']}</strong>
                        &nbsp;&nbsp;{badges}
                    </div>
                    <span class="price-tag">{format_price(row['price'])}</span>
                </div>
                <p style="color:#555; margin:0.35rem 0 0.5rem; font-size:0.9rem;">{row['description']}</p>
                <div style="display:flex; gap:1.5rem; font-size:0.82rem; color:#666; flex-wrap:wrap;">
                    <span>🌶️ {spicy_label(row['spicy_level'])}</span>
                    <span>🔥 {int(row['calories'])} kcal</span>
                    <span>💪 Protein: {row['protein']}g</span>
                    <span>🍞 Carbs: {row['carbs']}g</span>
                    <span>🧈 Fat: {row['fat']}g</span>
                </div>
                <div style="margin-top:0.4rem; font-size:0.8rem; color:#888;">
                    ⚠️ Contains: {allergen_str}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
