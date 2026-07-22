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
                --secondary:        #121218 !important;
                --accent:           #FF7A00 !important;
                --accent-dark:      #E06B00 !important;
                --accent-light:     #2D1B10 !important;
                --charcoal:         #F5EFE6 !important;
                --warm-gray:        #CBD5E0 !important;
                --border-warm:      #2D2D3B !important;
                --card-bg:          #1C1C26 !important;
                --card-radius:      16px !important;
                --pill-radius:      30px !important;
                --shadow-sm:        0 2px 10px rgba(0, 0, 0, 0.2) !important;
                --shadow-md:        0 6px 20px rgba(0, 0, 0, 0.4) !important;
            }

            [data-testid="stAppViewContainer"] {
                background-color: #121218 !important;
                background-image:
                    radial-gradient(at 10% 10%, rgba(255, 122, 0, 0.08) 0px, transparent 50%),
                    radial-gradient(at 90% 90%, rgba(255, 77, 109, 0.08) 0px, transparent 50%),
                    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='1' cy='1' r='1' fill='rgba(255%2C255%2C255%2C0.03)'/%3E%3C/svg%3E") !important;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(175deg, #0E0406 0%, #17080B 50%, #1A0A0E 100%) !important;
                border-right: 2px solid rgba(255, 122, 0, 0.4) !important;
            }

            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]),
            .sora-bubble {
                background: #1C1C26 !important;
                border: 1px solid #2D2D3B !important;
                border-left: 5px solid #FF7A00 !important;
                box-shadow: 0 4px 18px rgba(0,0,0,0.3) !important;
            }

            [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]),
            .user-bubble {
                background: #2A141A !important;
                border: 1px solid rgba(255, 77, 109, 0.3) !important;
                border-right: 5px solid #FF4D6D !important;
                box-shadow: 0 4px 18px rgba(0,0,0,0.3) !important;
            }

            [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {
                color: #F5EFE6 !important;
            }

            .menu-card, .info-card {
                background: #1C1C26 !important;
                border-color: #2D2D3B !important;
                color: #F5EFE6 !important;
            }

            .menu-card p, .info-card p, .info-card span, .hours-row span {
                color: #CBD5E0 !important;
            }

            .hero-sub {
                color: #CBD5E0 !important;
            }

            .hero-badge {
                background: rgba(255, 122, 0, 0.12) !important;
                border-color: rgba(255, 122, 0, 0.35) !important;
                color: #FF9433 !important;
            }

            div[data-testid="column"] .stButton > button {
                background: #1C1C26 !important;
                color: #FF4D6D !important;
                border-color: rgba(255, 77, 109, 0.4) !important;
            }

            div[data-testid="column"] .stButton > button:hover {
                background: linear-gradient(135deg, #FF4D6D, #FF7A00) !important;
                color: #FFFFFF !important;
                border-color: #FF4D6D !important;
            }

            [data-testid="stChatInput"] {
                background: #1C1C26 !important;
                border-color: #FF7A00 !important;
                box-shadow: 0 6px 24px rgba(255, 122, 0, 0.25) !important;
            }

            [data-testid="stChatInputTextArea"] {
                color: #F5EFE6 !important;
            }

            [data-testid="stChatInputTextArea"]::placeholder {
                color: rgba(245, 239, 230, 0.45) !important;
            }

            header[data-testid="stHeader"] {
                background: rgba(18, 18, 24, 0.85) !important;
                border-bottom-color: #2D2D3B !important;
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
