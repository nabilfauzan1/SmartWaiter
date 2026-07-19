"""
services/prompt_builder.py — Assembles the full prompt sent to Gemini.

Prompt construction order (mandatory):
  1. system_prompt.txt
  2. Restaurant information (relevant fields from restaurant_info.json)
  3. Filtered menu context
  4. Conversation history (trimmed to MAX_HISTORY_TURNS)
  5. Latest user message
"""

from __future__ import annotations

import json

import config


def _load_system_prompt() -> str:
    """Read system_prompt.txt from disk."""
    try:
        with open(config.SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "You are Sora, the AI waiter of Sorain Kitchen. Be friendly and helpful."
    except Exception:
        return "You are Sora, the AI waiter of Sorain Kitchen. Be friendly and helpful."


def _build_restaurant_context(restaurant_info: dict) -> str:
    """Extract relevant fields from restaurant_info.json for the prompt."""
    if not restaurant_info:
        return ""

    r = restaurant_info.get("restaurant", {})
    hours = restaurant_info.get("operating_hours", {})
    service = restaurant_info.get("service", {})
    dietary = restaurant_info.get("dietary_information", {})

    lines = [
        "=== RESTAURANT INFORMATION ===",
        f"Name: {r.get('name', 'Sorain Kitchen')}",
        f"Tagline: {r.get('tagline', '')}",
        f"Address: {r.get('address', '')}",
        f"Phone: {r.get('phone', '')}",
        f"Email: {r.get('email', '')}",
        f"Instagram: {r.get('instagram', '')}",
        f"Website: {r.get('website', '')}",
        "",
        "Operating Hours:",
    ]
    day_map = {
        "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
        "thursday": "Thursday", "friday": "Friday",
        "saturday": "Saturday", "sunday": "Sunday",
    }
    for key, label in day_map.items():
        if key in hours:
            lines.append(f"  {label}: {hours[key]}")

    lines += [
        "",
        f"Services: Dine-in={service.get('dine_in')}, Takeaway={service.get('takeaway')}, "
        f"Delivery={service.get('delivery')}",
        f"Payment: {', '.join(service.get('payment_methods', []))}",
        "",
        f"Halal-friendly: {dietary.get('halal_friendly')}",
        f"Pork served: {dietary.get('pork_served')}",
        f"Alcohol served: {dietary.get('alcohol_served')}",
        f"Vegetarian options: {dietary.get('vegetarian_options_available')}",
        f"Allergen notice: {dietary.get('allergen_notice', '')}",
    ]
    return "\n".join(lines)


def _build_history_context(history: list[dict]) -> str:
    """Format recent conversation turns for the prompt."""
    if not history:
        return ""

    # Take only the last MAX_HISTORY_TURNS turns
    recent = history[-config.MAX_HISTORY_TURNS:]

    lines = ["=== CONVERSATION HISTORY ==="]
    for turn in recent:
        role = "Customer" if turn["role"] == "user" else "Sora"
        lines.append(f"{role}: {turn['content']}")
    return "\n".join(lines)


def _build_preferences_context(preferences: dict) -> str:
    """Summarize active preferences so the LLM is explicitly aware of them."""
    active: list[str] = []

    if preferences.get("budget"):
        active.append(f"Budget: max Rp{preferences['budget']:,}")
    if preferences.get("vegetarian"):
        active.append("Dietary: Vegetarian")
    if preferences.get("halal_only"):
        active.append("Dietary: Halal only")
    if preferences.get("allergies"):
        active.append(f"Allergies: {', '.join(preferences['allergies'])}")
    if preferences.get("spicy_level_max") is not None:
        active.append(f"Max spicy level: {preferences['spicy_level_max']}")
    if preferences.get("healthy"):
        active.append("Preference: Healthy / low-calorie")
    if preferences.get("high_protein"):
        active.append("Preference: High protein")

    if not active:
        return ""
    return "=== CUSTOMER ACTIVE PREFERENCES ===\n" + "\n".join(active)


def build_prompt(
    menu_context: str,
    history: list[dict],
    user_message: str,
    restaurant_info: dict,
    preferences: dict,
    menu_is_empty: bool = False,
) -> str:
    """Assemble the full prompt for Gemini.

    Args:
        menu_context:    Pre-filtered menu text from menu_service.
        history:         List of {'role': 'user'|'assistant', 'content': str} dicts.
                         Must NOT include the current user_message.
        user_message:    The latest customer message (appended last).
        restaurant_info: Parsed restaurant_info.json dict.
        preferences:     Current customer preference dict.
        menu_is_empty:   If True, instructs Sora to explain no matches and suggest loosening.

    Returns:
        Single assembled prompt string.
    """
    sections: list[str] = []

    # 1. System prompt
    system_prompt = _load_system_prompt()
    if system_prompt:
        sections.append(system_prompt)

    # Empty-menu directive
    if menu_is_empty:
        sections.append(
            "=== IMPORTANT NOTE FOR SORA ===\n"
            "No menu items match the customer's current preferences/filters. "
            "Do NOT invent or guess menu items. "
            "Politely explain that no suitable menu exists under these constraints "
            "and suggest which preference could be relaxed (e.g., increase budget, "
            "remove an allergy filter, allow non-vegetarian, raise spicy limit)."
        )

    # 2. Restaurant information
    restaurant_ctx = _build_restaurant_context(restaurant_info)
    if restaurant_ctx:
        sections.append(restaurant_ctx)

    # Active preferences summary
    pref_ctx = _build_preferences_context(preferences)
    if pref_ctx:
        sections.append(pref_ctx)

    # 3. Filtered menu context
    sections.append(menu_context)

    # 4. Conversation history (previous turns only — NOT the current message)
    history_ctx = _build_history_context(history)
    if history_ctx:
        sections.append(history_ctx)

    # 5. Current user message
    sections.append(f"Customer: {user_message}")
    sections.append("Sora:")

    return "\n\n".join(sections)
