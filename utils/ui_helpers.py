"""
utils/ui_helpers.py — Shared UI utilities for SmartWaiter.

Provides inject_css() which loads the centralized stylesheet and handles
Light Mode / Dark Mode dynamic theme switching.
"""

from __future__ import annotations

import pathlib
import streamlit as st

_CSS_PATH = pathlib.Path(__file__).parent.parent / "assets" / "style.css"


def inject_css() -> None:
    """Load the global CSS design system and apply theme settings."""
    try:
        css = _CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

        # Check if Dark Mode is active
        if st.session_state.get("theme_dark", False):
            dark_css = """
            :root {
                --primary:          #FF4D6D !important;
                --primary-dark:     #E63946 !important;
                --primary-light:    #36151A !important;
                --secondary:        #171A21 !important;
                --accent:           #FF7A00 !important;
                --accent-dark:      #E06B00 !important;
                --accent-light:     #2D1B10 !important;
                --charcoal:         #F5F5F5 !important;
                --warm-gray:        #C7CBD1 !important;
                --border-warm:      #2A2F3D !important;
                --card-bg:          #232734 !important;
                --card-radius:      16px !important;
                --pill-radius:      24px !important;
                --shadow-sm:        0 2px 10px rgba(0, 0, 0, 0.2) !important;
                --shadow-md:        0 6px 20px rgba(0, 0, 0, 0.4) !important;
            }

            [data-testid="stAppViewContainer"] {
                background-color: #171A21 !important;
                background-image:
                    radial-gradient(at 10% 10%, rgba(255, 122, 0, 0.05) 0px, transparent 50%),
                    radial-gradient(at 90% 90%, rgba(255, 77, 109, 0.05) 0px, transparent 50%),
                    linear-gradient(180deg, #171A21 0%, #111318 100%) !important;
                background-size: cover !important;
                background-attachment: fixed !important;
            }

            h1, h2, h3 {
                color: #FF4D6D !important;
            }

            p, span, li, div {
                color: #F5F5F5;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(175deg, #0E0406 0%, #17080B 50%, #1A0A0E 100%) !important;
                border-right: 1.5px solid rgba(255, 122, 0, 0.3) !important;
            }

            /* Sora (assistant) bubble in Dark Mode */
            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
            .sora-bubble {
                background: #232734 !important;
                border: 1px solid #2A2F3D !important;
                border-left: 5px solid #FF7A00 !important;
                box-shadow: 0 4px 18px rgba(0,0,0,0.3) !important;
            }

            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
            .sora-bubble p {
                color: #F5F5F5 !important;
            }

            /* User bubble in Dark Mode — Deep Red with White Text */
            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
            .user-bubble {
                background: #7F1D1D !important;
                border: 1px solid #991B1B !important;
                border-right: 4px solid #FF7A00 !important;
                box-shadow: 0 4px 18px rgba(0,0,0,0.3) !important;
            }

            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span,
            .user-bubble p, .user-bubble span {
                color: #FFFFFF !important;
            }

            .menu-card, .info-card {
                background: #232734 !important;
                border-color: #2A2F3D !important;
                color: #F5F5F5 !important;
            }

            .menu-card p, .info-card p, .info-card span, .hours-row span {
                color: #C7CBD1 !important;
            }

            .hero-sub {
                color: #C7CBD1 !important;
            }

            .hero-badge {
                background: rgba(255, 122, 0, 0.12) !important;
                border-color: rgba(255, 122, 0, 0.35) !important;
                color: #FF9433 !important;
            }

            /* Quick Prompts Buttons in Dark Mode: #232734 background & #F5F5F5 font */
            div[data-testid="column"] button,
            .stHorizontalBlock button,
            [data-testid="stHorizontalBlock"] button,
            div[data-testid="column"] .stButton > button {
                background: #232734 !important;
                color: #F5F5F5 !important;
                border: 1.5px solid #2A2F3D !important;
                font-size: 0.80rem !important;
                padding: 0.4rem 0.4rem !important;
                overflow: visible !important;
                text-overflow: unset !important;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
            }

            div[data-testid="column"] button *,
            .stHorizontalBlock button *,
            [data-testid="stHorizontalBlock"] button * {
                color: #F5F5F5 !important;
            }

            div[data-testid="column"] button:hover,
            .stHorizontalBlock button:hover,
            [data-testid="stHorizontalBlock"] button:hover,
            div[data-testid="column"] .stButton > button:hover {
                background: linear-gradient(135deg, #FF4D6D, #FF7A00) !important;
                color: #FFFFFF !important;
                border-color: #FF4D6D !important;
                box-shadow: 0 4px 14px rgba(255, 122, 0, 0.3) !important;
                transform: translateY(-2px) !important;
            }

            div[data-testid="column"] button:hover *,
            .stHorizontalBlock button:hover * {
                color: #FFFFFF !important;
            }

            /* Bottom Container in Dark Mode */
            [data-testid="stBottom"],
            div[data-testid="stBottom"],
            section[data-testid="stBottom"],
            [data-testid="stBottom"] > div,
            .stChatInputContainer,
            .stBottom {
                background-color: #171A21 !important;
                background: #171A21 !important;
                border-top: 1px solid #2A2F3D !important;
            }

            [data-testid="stChatInput"] {
                background: #232734 !important;
                border: 1.5px solid #2A2F3D !important;
                box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3) !important;
            }

            [data-testid="stChatInputTextArea"] {
                color: #F5F5F5 !important;
            }

            [data-testid="stChatInputTextArea"]::placeholder {
                color: rgba(245, 245, 245, 0.45) !important;
            }

            /* Dark Mode Streamlit Header & Adaptive Toolbar Icons */
            header[data-testid="stHeader"] {
                background: rgba(23, 26, 33, 0.88) !important;
                border-bottom-color: #2A2F3D !important;
            }

            [data-testid="stHeader"] *,
            [data-testid="stToolbar"] *,
            [data-testid="stHeader"] button,
            [data-testid="stHeader"] button *,
            [data-testid="stHeader"] svg,
            [data-testid="stHeader"] path,
            [data-testid="stHeader"] g,
            [data-testid="stHeader"] span,
            [data-testid="stHeader"] a,
            [data-testid="stToolbar"] button,
            [data-testid="stToolbar"] svg,
            [data-testid="stToolbar"] path,
            [data-testid="stToolbar"] g {
                color: #F5F5F5 !important;
                fill: #F5F5F5 !important;
            }

            [data-testid="stHeader"] button:hover,
            [data-testid="stToolbar"] button:hover {
                background-color: rgba(255, 255, 255, 0.12) !important;
                border-radius: 8px !important;
            }
            """
            st.markdown(f"<style>{dark_css}</style>", unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("⚠️ Custom stylesheet not found at `{_CSS_PATH}`.", icon="🎨")


def render_theme_toggle() -> None:
    """Render a toggle switch for Light/Dark Mode in the sidebar."""
    current_dark = st.session_state.get("theme_dark", False)
    is_dark = st.sidebar.toggle(
        "🌙 Dark Mode",
        value=current_dark,
        key="theme_dark_toggle",
    )
    if is_dark != current_dark:
        st.session_state["theme_dark"] = is_dark
        st.rerun()
