"""
pages/3_About.py — About page for the SmartWaiter project.
"""

from __future__ import annotations

import os
import streamlit as st

import config
from utils.ui_helpers import inject_css, render_theme_toggle

st.set_page_config(
    page_title="About — SmartWaiter",
    page_icon="ℹ️",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────────
inject_css()

with st.sidebar:
    render_theme_toggle()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="page-header">
        <span class="page-header-icon">ℹ️</span>
        <h1>About SmartWaiter</h1>
        <p class="page-subtitle">Powered by Google Gemini · Sorain Kitchen AI Digital Waiter</p>
        <div class="restaurant-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Restaurant Logo Display ──────────────────────────────────────────────────
logo_path = config.LOGO_PATH
if os.path.exists(logo_path):
    col_logo, col_desc = st.columns([1, 3])
    with col_logo:
        st.markdown('<div class="info-card" style="text-align:center; padding:1rem;">', unsafe_allow_html=True)
        st.image(logo_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_desc:
        st.markdown(
            """
            <div class="info-card">
                <h2 style="margin-top:0; color:var(--primary);">🍜 Sorain Kitchen &amp; Sora AI</h2>
                <p>
                    <strong>SmartWaiter</strong> adalah sistem asisten pelayan digital interaktif berbasis AI
                    yang dikembangkan untuk <strong>Sorain Kitchen</strong>. Menggunakan teknologi terkini dari
                    <strong>Google Gemini API</strong>, pelanggan dapat berkonsultasi secara alami mengenai menu,
                    rekomendasi makanan, kebutuhan diet, hingga batas anggaran (budget).
                </p>
                <p>
                    Persona AI bernama <strong>Sora</strong> dirancang untuk memberikan pelayanan yang ramah, sopan,
                    dan solutif layaknya pelayan restoran berpengalaman.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
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
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Creator & Developer Credit ────────────────────────────────────────────────
st.markdown("## 👨‍💻 Creator & Developer")
st.markdown(
    """
    <div class="info-card" style="border-left: 5px solid var(--accent);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
            <div>
                <h3 style="margin:0 0 0.3rem; color:var(--primary); font-size:1.4rem;">Muhammad Nabil Fauzan</h3>
                <p style="margin:0 0 0.5rem; font-weight:700; color:var(--accent-dark);">
                    🎓 Mahasiswa CCIT FTUI (Center for Computing and Information Technology - Fakultas Teknik Universitas Indonesia)
                </p>
                <p style="margin:0 0 0.75rem; color:var(--warm-gray); line-height:1.6;">
                    Pencipta dan Pengembang Utama (Creator &amp; AI Engineer) dari aplikasi <strong>SmartWaiter (Sora AI Waiter)</strong>.
                    Sistem ini dibangun sebagai inovasi asisten digital cerdas berbasis LLM (Google Gemini) yang mengintegrasikan
                    ekstraksi preferensi pengguna secara deterministik dan rekomendasi menu kontekstual.
                </p>
                <div>
                    <span class="tech-badge">Creator &amp; Developer</span>
                    <span class="tech-badge">CCIT FTUI</span>
                    <span class="tech-badge">AI Engineer</span>
                </div>
            </div>
        </div>
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
    "google-genai SDK", "pandas", "python-dotenv", "CCIT FTUI Project",
]
badges_html = "".join(f'<span class="tech-badge">{t}</span>' for t in techs)
st.markdown(
    f'<div class="info-card"><div>{badges_html}</div></div>',
    unsafe_allow_html=True,
)

# ── Project Info ──────────────────────────────────────────────────────────────
st.markdown("## 📋 Project Details")
st.markdown(
    """
    <div class="info-card">
        <table style="width:100%; border-collapse:collapse; font-size:0.92rem;">
            <tr><td style="padding:6px; color:#888; width:180px;">Project Name</td><td><strong>SmartWaiter (Sora AI)</strong></td></tr>
            <tr><td style="padding:6px; color:#888;">Creator / Developer</td><td><strong>Muhammad Nabil Fauzan (Nabil Fauzan)</strong></td></tr>
            <tr><td style="padding:6px; color:#888;">Institution</td><td>CCIT FTUI (Fakultas Teknik Universitas Indonesia)</td></tr>
            <tr><td style="padding:6px; color:#888;">Restaurant</td><td>Sorain Kitchen</td></tr>
            <tr><td style="padding:6px; color:#888;">AI Waiter</td><td>Sora</td></tr>
            <tr><td style="padding:6px; color:#888;">LLM Service</td><td>Google Gemini API (gemini-flash-latest)</td></tr>
            <tr><td style="padding:6px; color:#888;">Platform</td><td>Streamlit</td></tr>
            <tr><td style="padding:6px; color:#888;">Version</td><td>1.0 MVP</td></tr>
        </table>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "⚠️ SmartWaiter is an academic demonstration project developed by Muhammad Nabil Fauzan (CCIT FTUI). "
    "All restaurant data, prices, menus, and contact information are created for demonstration purposes."
)
