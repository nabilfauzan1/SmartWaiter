"""
pages/2_Restaurant_Info.py — Restaurant information page.

Displays address, operating hours, contact details, service info,
and dietary information loaded from data/restaurant_info.json.
"""

from __future__ import annotations

import streamlit as st

from utils.formatter import load_restaurant_info
from utils.ui_helpers import inject_css

st.set_page_config(
    page_title="Restaurant Info — Sorain Kitchen",
    page_icon="📍",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────────
inject_css()

# ── Load Data ─────────────────────────────────────────────────────────────────
info, error = load_restaurant_info()

st.markdown(
    """
    <div class="page-header">
        <span class="page-header-icon">📍</span>
        <h1>Restaurant Information</h1>
        <p class="page-subtitle">Sorain Kitchen — Authentic Japanese Comfort Food</p>
        <div class="restaurant-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if error:
    st.error(error)
    st.info("Please contact restaurant management to resolve this issue.")
    st.stop()

assert info is not None

r = info.get("restaurant", {})
hours = info.get("operating_hours", {})
service = info.get("service", {})
dietary = info.get("dietary_information", {})
ai = info.get("ai_waiter", {})

# ── About ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        f"""
        <div class="info-card">
            <h2 style="margin-top:0;">{r.get('name', 'Sorain Kitchen')}</h2>
            <p style="color:#8B0000; font-style:italic; font-size:1.05rem;">{r.get('tagline', '')}</p>
            <p style="color:#555;">{r.get('description', '')}</p>
            <hr style="border-color:#f0e0d0;">
            <p>🏙️ <strong>City:</strong> {r.get('city', '')}, {r.get('country', '')}</p>
            <p>📍 <strong>Address:</strong> {r.get('address', '')}</p>
            <p>📞 <strong>Phone:</strong> {r.get('phone', '')}</p>
            <p>📧 <strong>Email:</strong> {r.get('email', '')}</p>
            <p>📸 <strong>Instagram:</strong> {r.get('instagram', '')}</p>
            <p>🌐 <strong>Website:</strong> {r.get('website', '')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    # Service info
    st.markdown(
        f"""
        <div class="info-card">
            <h3 style="margin-top:0;">🛎️ Services</h3>
            <p>{'✅' if service.get('dine_in') else '❌'} Dine-in</p>
            <p>{'✅' if service.get('takeaway') else '❌'} Takeaway</p>
            <p>{'✅' if service.get('delivery') else '❌'} Delivery</p>
            <p>{'✅' if service.get('reservation_available') else '❌'} Reservations</p>
            <hr style="border-color:#f0e0d0;">
            <p>👥 Capacity: <strong>{service.get('capacity', '-')} pax</strong></p>
            <p>⏱️ Avg wait: <strong>{service.get('average_waiting_time_minutes', '-')} min</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Payment
    methods = service.get("payment_methods", [])
    methods_str = " · ".join(methods) if methods else "-"
    st.markdown(
        f"""
        <div class="info-card">
            <h3 style="margin-top:0;">💳 Payment</h3>
            <p style="font-size:0.9rem;">{methods_str}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Operating Hours ───────────────────────────────────────────────────────────
st.markdown("## ⏰ Operating Hours")

day_labels = {
    "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
    "thursday": "Thursday", "friday": "Friday",
    "saturday": "Saturday", "sunday": "Sunday",
}
last_order = hours.get("last_order_minutes_before_close", 30)

hours_html = '<div class="info-card">'
for key, label in day_labels.items():
    if key in hours:
        hours_html += (
            f'<div class="hours-row">'
            f'<span class="day-label">{label}</span>'
            f'<span>{hours[key]}</span>'
            f'</div>'
        )
hours_html += f'<p style="margin-top:0.75rem; font-size:0.85rem; color:#888;">⚠️ Last order {last_order} minutes before closing.</p>'
hours_html += "</div>"
st.markdown(hours_html, unsafe_allow_html=True)

# ── Dietary Information ───────────────────────────────────────────────────────
st.markdown("## 🥗 Dietary & Allergen Information")
st.markdown(
    f"""
    <div class="info-card">
        <p>{'☪️ ✅' if dietary.get('halal_friendly') else '☪️ ❌'} <strong>Halal Friendly</strong></p>
        <p>{'🐷 ❌' if not dietary.get('pork_served') else '🐷 ✅'} <strong>{'No Pork Served' if not dietary.get('pork_served') else 'Pork Available'}</strong></p>
        <p>{'🍷 ❌' if not dietary.get('alcohol_served') else '🍷 ✅'} <strong>{'No Alcohol Served' if not dietary.get('alcohol_served') else 'Alcohol Available'}</strong></p>
        <p>{'🥦 ✅' if dietary.get('vegetarian_options_available') else '🥦 ❌'} <strong>Vegetarian Options Available</strong></p>
        <p>{'🌱 ✅' if dietary.get('vegan_options_available') else '🌱 ❌'} <strong>Vegan Options Available</strong></p>
        <hr style="border-color:#f0e0d0;">
        <p style="font-size:0.88rem; color:#666;">⚠️ <strong>Allergen Notice:</strong> {dietary.get('allergen_notice', '')}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Meet Sora ─────────────────────────────────────────────────────────────────
st.markdown("## 🍵 Meet Sora — Your AI Waiter")
personality = ", ".join(ai.get("personality", []))
languages = ", ".join(ai.get("supported_languages", []))
responsibilities = ai.get("responsibilities", [])

st.markdown(
    f"""
    <div class="info-card">
        <p><strong>Name:</strong> {ai.get('name', 'Sora')} | <strong>Role:</strong> {ai.get('role', 'AI Waiter')}</p>
        <p><strong>Personality:</strong> {personality}</p>
        <p><strong>Languages:</strong> {languages}</p>
        <hr style="border-color:#f0e0d0;">
        <strong>Sora can help you with:</strong>
        <ul>
            {''.join(f"<li>{r}</li>" for r in responsibilities)}
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(info.get("disclaimer", ""))
