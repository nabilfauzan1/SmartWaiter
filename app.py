"""
app.py — SmartWaiter main Streamlit application.

Entry point: streamlit run app.py

This file owns the chat UI, sidebar, quick-prompt buttons, and the
orchestration loop:
  1. Extract preferences from user message
  2. Filter menu via pandas
  3. Build prompt
  4. Call Gemini
  5. Display response
"""

from __future__ import annotations

import os

import streamlit as st

import config
from services.gemini_service import send_message, check_api_connection
from services.menu_service import load_menu, filter_menu, get_menu_context
from services.preference_service import default_preferences, update_preferences
from services.prompt_builder import build_prompt
from utils.formatter import (
    load_restaurant_info,
    load_greeting,
    preference_summary,
    format_price,
)
from utils.ui_helpers import inject_css, render_theme_toggle

# ── Page Configuration ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SmartWaiter — Sorain Kitchen",
    page_icon="🍵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────

inject_css()

# ── Session State Initialisation ──────────────────────────────────────────────

def _init_session() -> None:
    """Initialise all session state keys on first load."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "preferences" not in st.session_state:
        st.session_state["preferences"] = default_preferences()
    if "greeting_shown" not in st.session_state:
        st.session_state["greeting_shown"] = False
    if "api_status" not in st.session_state:
        st.session_state["api_status"] = None  # None = not yet checked
    if "pending_prompt" not in st.session_state:
        st.session_state["pending_prompt"] = None


def _reset_chat() -> None:
    """Clear chat history and preference state (New Chat action)."""
    st.session_state["messages"] = []
    st.session_state["preferences"] = default_preferences()
    st.session_state["greeting_shown"] = False
    st.session_state["pending_prompt"] = None


# ── Data Loading ──────────────────────────────────────────────────────────────

def _load_data():
    """Load menu and restaurant info, returning errors as strings."""
    menu_df, menu_error = load_menu()
    restaurant_info, info_error = load_restaurant_info()
    return menu_df, menu_error, restaurant_info, info_error


# ── Sidebar ───────────────────────────────────────────────────────────────────

def _render_sidebar(restaurant_info: dict | None) -> None:
    """Render the sidebar: theme toggle, new chat, nav info, preferences, API status."""
    with st.sidebar:
        # Theme toggle (Light / Dark Mode)
        render_theme_toggle()

        st.markdown("---")

        # New Chat button — accent orange CTA
        if st.button("✨ New Chat", key="new_chat_btn"):
            _reset_chat()
            st.rerun()

        st.markdown("---")

        # Restaurant info snippet
        if restaurant_info:
            r = restaurant_info.get("restaurant", {})
            hours = restaurant_info.get("operating_hours", {})
            st.markdown(f"**{r.get('name', 'Sorain Kitchen')}**")
            st.markdown(f"*{r.get('tagline', '')}*")
            st.markdown(f"📍 {r.get('address', '')}")
            st.markdown(f"📞 {r.get('phone', '')}")
            st.markdown(
                f"⏰ Mon–Thu: {hours.get('monday', '-')} | "
                f"Fri–Sat: {hours.get('friday', '-')}"
            )
        else:
            st.markdown("**Sorain Kitchen**")
            st.caption("Restaurant information unavailable.")

        st.markdown("---")

        # Active preferences
        st.markdown("**🎯 Your Preferences**")
        prefs = st.session_state.get("preferences", {})
        pref_text = preference_summary(prefs)
        st.caption(pref_text)

        st.markdown("---")

        # API connection status
        api_status = st.session_state.get("api_status")
        if api_status is True:
            st.markdown(
                '<span class="status-badge status-online">● Sora Online</span>',
                unsafe_allow_html=True,
            )
        elif api_status is False:
            st.markdown(
                '<span class="status-badge status-offline">● Service Unavailable</span>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("Checking connection…")

        st.markdown("---")
        st.caption("SmartWaiter v1.0 · Sorain Kitchen")


# ── Quick Prompts ─────────────────────────────────────────────────────────────

QUICK_PROMPTS: list[tuple[str, str]] = [
    ("🍽️ Recommend", "Rekomendasikan menu untuk saya"),
    ("🌶️ Spicy", "Saya mau makanan yang pedas"),
    ("🥗 Healthy", "Saya mau makanan yang sehat dan rendah kalori"),
    ("👨‍🍳 Chef's Pick", "Apa rekomendasi chef?"),
    ("🍰 Dessert", "Saya mau dessert"),
    ("🍵 Drinks", "Rekomendasikan minuman"),
    ("💰 Budget", "Rekomendasikan menu dengan budget terbaik"),
]


def _render_quick_prompts() -> str | None:
    """Render quick-prompt pill buttons. Returns clicked prompt text or None.

    Uses st.columns so Streamlit handles click state correctly.
    CSS in assets/style.css handles white-space:nowrap and hover effects.
    """
    st.markdown(
        '<p class="quick-prompts-label">✦ Quick Prompts</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(len(QUICK_PROMPTS))
    for col, (label, prompt_text) in zip(cols, QUICK_PROMPTS):
        with col:
            if st.button(label, key=f"qp_{label}"):
                return prompt_text
    return None


# ── Chat Handling ─────────────────────────────────────────────────────────────

def _process_message(
    user_input: str,
    menu_df,
    restaurant_info: dict | None,
) -> None:
    """Core orchestration: update prefs → filter menu → build prompt → call Gemini."""

    # 1. Update preferences deterministically
    prefs = update_preferences(st.session_state["preferences"], user_input)
    st.session_state["preferences"] = prefs

    # 2. Filter menu with pandas
    filtered_df = filter_menu(menu_df, prefs) if menu_df is not None else None
    menu_is_empty = (filtered_df is None or filtered_df.empty)
    menu_ctx = get_menu_context(filtered_df) if filtered_df is not None else "Menu data unavailable."

    # 3. Build prompt (history excludes current message)
    history = st.session_state["messages"][:-1]  # all turns except the just-appended user turn
    prompt = build_prompt(
        menu_context=menu_ctx,
        history=history,
        user_message=user_input,
        restaurant_info=restaurant_info or {},
        preferences=prefs,
        menu_is_empty=menu_is_empty,
    )

    # 4. Call Gemini
    with st.spinner("Sora is thinking… 🍵"):
        response = send_message(prompt)

    # 5. Store and display
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.session_state["api_status"] = True


# ── Greeting ──────────────────────────────────────────────────────────────────

def _maybe_show_greeting() -> None:
    """Show the initial greeting once per session."""
    if not st.session_state["greeting_shown"]:
        greeting = load_greeting()
        st.session_state["messages"].insert(0, {"role": "assistant", "content": greeting})
        st.session_state["greeting_shown"] = True


# ── Main ──────────────────────────────────────────────────────────────────────

def _render_hero(restaurant_info: dict | None) -> None:
    """Render the landing hero section shown on empty-chat state."""
    import os
    logo_path = config.LOGO_PATH
    logo_html = ""
    if os.path.exists(logo_path):
        import base64
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = (
            f'<div class="hero-logo-wrap">'
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'style="width:100%;border-radius:16px;" alt="Sorain Kitchen"/>'
            f'</div>'
        )

    st.markdown(
        f"""
        <div class="hero-section">
            {logo_html}
            <h1 class="hero-headline">Irasshaimase!<br>Selamat Datang di Sorain Kitchen 🍵</h1>
            <p class="hero-sub">
                Saya Sora, pelayan AI Anda hari ini. Saya siap membantu Anda
                menemukan hidangan Jepang yang sempurna — sesuai selera, kebutuhan
                diet, dan anggaran Anda.
            </p>
            <div class="hero-badges">
                <span class="hero-badge">🍜 Ramen &amp; Sushi</span>
                <span class="hero-badge">🥗 Healthy Options</span>
                <span class="hero-badge">💰 Budget Friendly</span>
                <span class="hero-badge">☪️ Halal Friendly</span>
            </div>
            <div class="restaurant-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    _init_session()

    # Load data
    menu_df, menu_error, restaurant_info, info_error = _load_data()

    # Sidebar
    _render_sidebar(restaurant_info)

    # Data errors (non-fatal)
    if menu_error:
        st.warning(menu_error)
    if info_error:
        st.warning(info_error)

    # API key check (done lazily once per session)
    if st.session_state["api_status"] is None:
        if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY.startswith("YOUR_"):
            st.error(
                "⚠️ **Google API Key belum diatur.**\n\n"
                "Buka file `.env` di root project dan isi nilai `GOOGLE_API_KEY`.\n\n"
                "*(Open the `.env` file and set your `GOOGLE_API_KEY` to enable Sora.)*"
            )
            st.session_state["api_status"] = False
        else:
            st.session_state["api_status"] = True  # Mark as potentially valid; errors caught on send

    # Show greeting
    _maybe_show_greeting()

    # ── Hero (empty-chat state: only greeting message present) ──
    is_empty_chat = len(st.session_state["messages"]) <= 1
    if is_empty_chat:
        _render_hero(restaurant_info)
    else:
        # Compact header for active conversation
        st.markdown(
            '<div style="text-align:center;padding:0.5rem 0 0.25rem;">'
            '<div class="restaurant-divider"></div></div>',
            unsafe_allow_html=True,
        )

    # Render chat history
    # In hero mode (only the greeting exists), skip showing the greeting as a plain
    # chat bubble — the hero section already presents a richer welcome visual.
    # Once the user sends a message (active conversation), all messages render normally.
    for i, msg in enumerate(st.session_state["messages"]):
        if is_empty_chat and i == 0 and msg["role"] == "assistant":
            continue  # suppressed in hero mode; shown via _render_hero()
        avatar = "🍵" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # ── Quick Prompts ──
    clicked_prompt = _render_quick_prompts()

    # Jika quick prompt diklik, simpan ke session_state lalu rerun
    # agar chat_input tetap muncul di run berikutnya
    if clicked_prompt:
        st.session_state["pending_prompt"] = clicked_prompt
        st.rerun()

    # Chat input selalu dirender (tidak di dalam else), sehingga kolom
    # chat tidak pernah hilang meskipun quick prompt baru saja diklik
    typed = st.chat_input("Tanya Sora apa saja tentang menu kami… 🍣")

    # Tentukan input aktual: pending_prompt (dari quick prompt) ATAU typed
    user_input: str | None = None
    if st.session_state.get("pending_prompt"):
        user_input = st.session_state.pop("pending_prompt")
    elif typed and typed.strip():
        user_input = typed.strip()

    # Process input
    if user_input:
        # Simpan pesan user
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Tampilkan pesan user segera
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        if menu_df is None:
            st.warning(
                "⚠️ Menu data unavailable. Sora will respond without menu context."
            )

        _process_message(user_input, menu_df, restaurant_info)

        # Tampilkan respons terbaru assistant
        latest = st.session_state["messages"][-1]
        if latest["role"] == "assistant":
            with st.chat_message("assistant", avatar="🍵"):
                st.markdown(latest["content"])


if __name__ == "__main__":
    main()
