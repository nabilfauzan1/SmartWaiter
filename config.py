"""
config.py — Application configuration for SmartWaiter.

Reads environment variables from .env and exposes them as typed constants.
All other modules must import settings from here, never from os.environ directly.
"""

import os
from dotenv import load_dotenv

# Load .env at import time so every module that imports config is covered.
load_dotenv()


# ── Google Gemini ─────────────────────────────────────────────────────────────
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# ── File Paths ────────────────────────────────────────────────────────────────
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
MENU_CSV_PATH: str = os.path.join(BASE_DIR, "data", "menu.csv")
RESTAURANT_JSON_PATH: str = os.path.join(BASE_DIR, "data", "restaurant_info.json")
SYSTEM_PROMPT_PATH: str = os.path.join(BASE_DIR, "prompts", "system_prompt.txt")
GREETING_PATH: str = os.path.join(BASE_DIR, "prompts", "greeting.txt")
LOGO_PATH: str = os.path.join(BASE_DIR, "assets", "logo.png")

# ── Brand Colors (fallback if JSON is unavailable) ───────────────────────────
PRIMARY_COLOR: str = "#B22222"
SECONDARY_COLOR: str = "#FFF8F0"
ACCENT_COLOR: str = "#D4AF37"
TEXT_COLOR: str = "#222222"

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
