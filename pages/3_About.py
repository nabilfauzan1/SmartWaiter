"""
pages/3_About.py — About page for the SmartWaiter project.
"""

from __future__ import annotations

import streamlit as st

from utils.ui_helpers import inject_css

st.set_page_config(
    page_title="About — SmartWaiter",
    page_icon="ℹ️",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────────
inject_css()

st.markdown(
    """
    <div class="page-header">
        <span class="page-header-icon">ℹ️</span>
        <h1>About SmartWaiter</h1>
        <p class="page-subtitle">Powered by Google Gemini · Built for Sorain Kitchen</p>
        <div class="restaurant-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Project Overview ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="info-card">
        <h2 style="margin-top:0;">🍜 What is SmartWaiter?</h2>
        <p>
            <strong>SmartWaiter</strong> is an AI-powered digital waiter for
            <strong>Sorain Kitchen</strong>, a modern Japanese restaurant.
            Powered by <strong>Google Gemini</strong>, SmartWaiter enables customers
            to interact naturally with an AI persona named <strong>Sora</strong>.
        </p>
        <p>
            Sora helps customers discover the perfect dish based on their taste,
            dietary restrictions, budget, and preferences — creating a personalised
            and friendly restaurant experience.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0;">🤖 AI Chat with Sora</h3>
            <ul>
                <li>Natural language conversation</li>
                <li>Bilingual: Indonesian &amp; English</li>
                <li>Session memory across the chat</li>
                <li>Quick prompt shortcuts</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0;">🛡️ Safety &amp; Privacy</h3>
            <ul>
                <li>Prompt injection protection</li>
                <li>No system prompt exposure</li>
                <li>No API key leakage</li>
                <li>Friendly error messages</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0;">🥗 Smart Filtering</h3>
            <ul>
                <li>Budget-based filtering (code-level)</li>
                <li>Allergen exclusion (deterministic)</li>
                <li>Vegetarian &amp; halal filters</li>
                <li>Spicy level preferences</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0;">🍣 Menu Browser</h3>
            <ul>
                <li>Browse all 52 menu items</li>
                <li>Filter by category, price, dietary</li>
                <li>Nutritional info per item</li>
                <li>Chef recommendation badges</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Tech Stack ────────────────────────────────────────────────────────────────
st.markdown("## 🛠️ Tech Stack")

techs = [
    "Python 3.12", "Streamlit", "Google Gemini API",
    "google-genai SDK", "pandas", "python-dotenv", "Miniconda",
]
badges_html = "".join(f'<span class="tech-badge">{t}</span>' for t in techs)
st.markdown(
    f'<div class="info-card"><div>{badges_html}</div></div>',
    unsafe_allow_html=True,
)

# ── Architecture ──────────────────────────────────────────────────────────────
st.markdown("## 🏗️ Architecture")
st.markdown(
    """
    <div class="info-card">
        <pre style="background:#FFF8F0; padding:0.75rem; border-radius:8px; font-size:0.82rem; color:#333;">
Customer Input
     │
     ▼
Preference Extraction  ← Deterministic Python rules (no LLM)
     │
     ▼
Menu Filtering         ← pandas (budget / allergen / veg / halal / spicy)
     │
     ▼
Prompt Builder         ← System Prompt + Restaurant Info + Filtered Menu + History
     │
     ▼
Google Gemini API      ← gemini-2.5-flash
     │
     ▼
Sora Response          ← Displayed in Streamlit chat UI
        </pre>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Project Info ──────────────────────────────────────────────────────────────
st.markdown("## 📋 Project Details")
st.markdown(
    """
    <div class="info-card">
        <table style="width:100%; border-collapse:collapse; font-size:0.92rem;">
            <tr><td style="padding:6px; color:#888; width:160px;">Project Name</td><td><strong>SmartWaiter</strong></td></tr>
            <tr><td style="padding:6px; color:#888;">Restaurant</td><td>Sorain Kitchen (fictional)</td></tr>
            <tr><td style="padding:6px; color:#888;">AI Waiter</td><td>Sora</td></tr>
            <tr><td style="padding:6px; color:#888;">LLM</td><td>Google Gemini 2.5 Flash</td></tr>
            <tr><td style="padding:6px; color:#888;">Platform</td><td>Streamlit</td></tr>
            <tr><td style="padding:6px; color:#888;">Language</td><td>Python 3.12</td></tr>
            <tr><td style="padding:6px; color:#888;">Version</td><td>1.0 MVP</td></tr>
        </table>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "⚠️ SmartWaiter is an academic demonstration project. "
    "All restaurant data, prices, menus, and contact information are fictional."
)
