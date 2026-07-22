"""
config.py — Application configuration for SmartWaiter.

Reads environment variables from .env and exposes them as typed constants.
All other modules must import settings from here, never from os.environ directly.
"""

import os

from dotenv import load_dotenv

# Load .env at import time so every module that imports config is covered.
load_dotenv()


def _get_setting(key: str, default: str = "") -> str:
    """Retrieve configuration setting prioritizing Streamlit secrets (for public cloud deploy),

    then environment variables (.env for local development), and finally default.
    """
    # 1. Check Streamlit Secrets (active when deployed on Streamlit Cloud)
    try:
        import streamlit as st
        if key in st.secrets:
            val = str(st.secrets[key]).strip()
            if val:
                return val
    except Exception:
        pass

    # 2. Check local environment variables (.env)
    val = os.getenv(key, "").strip()
    if val:
        return val

    return default


# ── Google Gemini ─────────────────────────────────────────────────────────────
GOOGLE_API_KEY: str = _get_setting("GOOGLE_API_KEY", "")
GEMINI_MODEL: str = _get_setting("GEMINI_MODEL", "gemini-3.1-flash-lite")

# ── File Paths ────────────────────────────────────────────────────────────────
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
MENU_CSV_PATH: str = os.path.join(BASE_DIR, "data", "menu.csv")
RESTAURANT_JSON_PATH: str = os.path.join(BASE_DIR, "data", "restaurant_info.json")
SYSTEM_PROMPT_PATH: str = os.path.join(BASE_DIR, "prompts", "system_prompt.txt")
GREETING_PATH: str = os.path.join(BASE_DIR, "prompts", "greeting.txt")
LOGO_PATH: str = os.path.join(BASE_DIR, "assets", "logo.png")

# ── Brand Colors (fallback if JSON is unavailable) ───────────────────────────
PRIMARY_COLOR: str = "#C8102E"
SECONDARY_COLOR: str = "#FAF6F0"
ACCENT_COLOR: str = "#FF6B00"
TEXT_COLOR: str = "#1E1E24"

# ── Chat / Prompt Settings ────────────────────────────────────────────────────
MAX_HISTORY_TURNS: int = 10          # Maximum number of past turns sent to Gemini
MAX_MENU_ROWS_IN_PROMPT: int = 30    # Safety cap on filtered menu rows sent to LLM

# ── Required Menu CSV Columns ─────────────────────────────────────────────────
REQUIRED_MENU_COLUMNS: list[str] = [
    "menu_id", "menu_name", "category", "description", "price",
    "calories", "protein", "carbs", "fat", "spicy_level",
    "halal", "vegetarian", "contains", "recommended_for",
    "chef_recommendation", "availability",
]
