"""
utils/ui_helpers.py — Shared UI utilities for SmartWaiter.

Provides inject_css() which loads and injects the centralized stylesheet.
This file contains ONLY presentation helpers — no business logic.
"""

from __future__ import annotations

import pathlib

import streamlit as st

# Path to the centralized stylesheet, relative to this file's location
_CSS_PATH = pathlib.Path(__file__).parent.parent / "assets" / "style.css"


def inject_css() -> None:
    """Load the global CSS design system and inject it into the Streamlit page.

    Called once at the top of every page (app.py + pages/*.py) immediately
    after st.set_page_config().  No session state, no business logic.
    """
    try:
        css = _CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Graceful degradation — app still functions without custom styles
        st.warning(
            f"⚠️ Custom stylesheet not found at `{_CSS_PATH}`. "
            "Falling back to default Streamlit styling.",
            icon="🎨",
        )
