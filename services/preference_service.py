"""
services/preference_service.py — Deterministic preference extraction and updating.

Extracts customer preferences from natural language using keyword matching and
regular expressions — NO secondary Gemini calls are made here.

Supports both Indonesian and English expressions.
"""

from __future__ import annotations

import re


# ── Default Preference State ──────────────────────────────────────────────────

def default_preferences() -> dict:
    """Return a fresh, empty preference dict."""
    return {
        "budget": None,           # int (IDR) or None
        "vegetarian": False,
        "halal_only": False,
        "allergies": [],          # list of normalized allergen strings
        "spicy_level_max": None,  # int 0-5 or None
        "healthy": False,         # low-calorie flag
        "high_protein": False,
    }


# ── Allergen Normalization Map ────────────────────────────────────────────────

ALLERGEN_MAP: dict[str, str] = {
    # Shellfish group
    "udang": "Shellfish",
    "shrimp": "Shellfish",
    "prawn": "Shellfish",
    "kerang": "Shellfish",
    "shellfish": "Shellfish",
    "seafood": "Shellfish",
    "lobster": "Shellfish",
    "crab": "Shellfish",
    "kepiting": "Shellfish",
    # Egg
    "telur": "Egg",
    "egg": "Egg",
    # Milk / dairy
    "susu": "Milk",
    "milk": "Milk",
    "dairy": "Milk",
    "keju": "Milk",
    "cheese": "Milk",
    # Wheat / gluten
    "gandum": "Wheat",
    "wheat": "Wheat",
    "gluten": "Wheat",
    "terigu": "Wheat",
    "flour": "Wheat",
    # Soy
    "kedelai": "Soy",
    "soy": "Soy",
    "tofu": "Soy",
    "tempe": "Soy",
    # Fish
    "ikan": "Fish",
    "fish": "Fish",
    "salmon": "Fish",
    "tuna": "Fish",
    "eel": "Fish",
    "unagi": "Fish",
    # Sesame
    "wijen": "Sesame",
    "sesame": "Sesame",
    # Nuts
    "kacang": "Nuts",
    "nuts": "Nuts",
    "peanut": "Nuts",
    "almond": "Nuts",
}


def normalize_allergen_from_text(raw: str) -> str | None:
    """Map a raw allergen keyword from user text to the canonical name."""
    cleaned = raw.lower().strip()
    return ALLERGEN_MAP.get(cleaned)


# ── Budget Extraction ─────────────────────────────────────────────────────────

_BUDGET_PATTERNS: list[re.Pattern] = [
    # "Rp50.000" / "rp 50.000" / "rp50000"
    re.compile(r"rp\.?\s*([\d.,]+)", re.IGNORECASE),
    # "50 ribu" / "50ribu"
    re.compile(r"([\d.,]+)\s*ribu", re.IGNORECASE),
    # "50k" / "50K"
    re.compile(r"([\d.,]+)\s*k\b", re.IGNORECASE),
    # "maximum 50000" / "max 50000" / "budget 50000"
    re.compile(r"(?:budget|max(?:imum)?|maksimal?|maksimum)\s*[:\-]?\s*([\d.,]+)", re.IGNORECASE),
    # plain number followed by "rb"
    re.compile(r"([\d.,]+)\s*rb\b", re.IGNORECASE),
]

_BUDGET_REMOVE_PATTERN = re.compile(
    r"(?:ignore|hapus|lupakan|reset|no|tidak ada|batal|cancel|remove)\s*"
    r"(?:my\s*(?:previous\s*)?)?(?:budget|anggaran|budgetku)",
    re.IGNORECASE,
)


def _parse_amount(raw: str) -> int:
    """Clean and parse a numeric string (handles '.' and ',' as thousand separators)."""
    cleaned = raw.replace(".", "").replace(",", "")
    return int(cleaned)


def extract_budget(message: str) -> tuple[int | None, bool]:
    """Return (budget_value, should_reset).

    should_reset=True means the user wants to clear their budget.
    """
    if _BUDGET_REMOVE_PATTERN.search(message):
        return None, True

    for idx, pattern in enumerate(_BUDGET_PATTERNS):
        match = pattern.search(message)
        if match:
            try:
                raw = match.group(1)
                amount = _parse_amount(raw)
                # Patterns 1 (ribu), 2 (k), 4 (rb) need ×1000 when amount < 1000
                # Pattern 0 (Rp) and 3 (max/budget) are already in full IDR
                needs_multiply = idx in (1, 2, 4)
                if needs_multiply and amount < 1000:
                    amount *= 1000
                return amount, False
            except (ValueError, IndexError):
                continue
    return None, False


# ── Vegetarian Extraction ─────────────────────────────────────────────────────

_VEGE_ON = re.compile(
    r"\b(vegetarian|vegan|plant[- ]based|tidak makan daging|no meat|nabati)\b",
    re.IGNORECASE,
)
_VEGE_OFF = re.compile(
    r"\b(not vegetarian|no longer vegetarian|bukan vegetarian|sudah tidak vegetarian|makan daging lagi)\b",
    re.IGNORECASE,
)


def extract_vegetarian(message: str) -> bool | None:
    """Return True/False to set, or None if no signal found."""
    if _VEGE_OFF.search(message):
        return False
    if _VEGE_ON.search(message):
        return True
    return None


# ── Halal Extraction ──────────────────────────────────────────────────────────

_HALAL_ON = re.compile(r"\b(halal|halal only|halal saja|mau yang halal)\b", re.IGNORECASE)
_HALAL_OFF = re.compile(r"\b(not halal only|no longer halal|tidak perlu halal)\b", re.IGNORECASE)


def extract_halal(message: str) -> bool | None:
    if _HALAL_OFF.search(message):
        return False
    if _HALAL_ON.search(message):
        return True
    return None


# ── Spicy Level Extraction ────────────────────────────────────────────────────

_SPICY_PATTERNS: list[re.Pattern] = [
    re.compile(r"(?:spicy|pedas)\s*level\s*(\d)", re.IGNORECASE),
    re.compile(r"level\s*(\d)\s*(?:spicy|pedas|saja|is enough|cukup)", re.IGNORECASE),
    re.compile(r"(?:max|maximum|maksimal?)\s*(?:spicy|pedas)?\s*level\s*(\d)", re.IGNORECASE),
    re.compile(r"(\d)\s*(?:level)?\s*(?:spicy|pedas)", re.IGNORECASE),
]
_SPICY_RESET = re.compile(
    r"\b(not spicy|tidak pedas|no spicy|0 spicy|tanpa pedas|level 0)\b",
    re.IGNORECASE,
)
_SPICY_REMOVE = re.compile(
    r"(?:ignore|remove|reset|batal)\s*(?:my\s*)?(?:spicy|pedas)\s*(?:preference|level|limit)?",
    re.IGNORECASE,
)


def extract_spicy_level(message: str) -> int | None | str:
    """Return int level, None (meaning 'no constraint'), or 'remove' to clear."""
    if _SPICY_REMOVE.search(message):
        return "remove"
    if _SPICY_RESET.search(message):
        return 0
    for pattern in _SPICY_PATTERNS:
        match = pattern.search(message)
        if match:
            level = int(match.group(1))
            return min(max(level, 0), 5)  # clamp to 0-5
    return None


# ── Allergy Extraction ────────────────────────────────────────────────────────

# Patterns that capture everything after the trigger phrase until a hard boundary.
_ALLERGY_ADD = re.compile(
    r"(?:i(?:'m| am)?\s*)?(?:alergi(?:\s+terhadap)?|allergic to|allergy to)\s+([a-z][a-z\s]*?)(?=\s*(?:dan|and|,|\.|;|\n|$))",
    re.IGNORECASE,
)
_ALLERGY_REMOVE = re.compile(
    r"(?:i(?:'m| am)?\s*)?(?:not allergic to|no longer allergic to|tidak alergi|sudah tidak alergi|bukan alergi)\s+([a-z][a-z\s]*?)(?=\s*(?:dan|and|,|\.|;|\n|$))",
    re.IGNORECASE,
)

# Detect removal intent (separate from capture)
_REMOVE_TRIGGER = re.compile(
    r"not allergic to|no longer allergic to|tidak alergi|sudah tidak alergi|bukan alergi",
    re.IGNORECASE,
)
_ADD_TRIGGER = re.compile(
    r"alergi(?:\s+terhadap)?|allergic to|allergy to",
    re.IGNORECASE,
)


def _extract_allergens_from_text(text: str) -> list[str]:
    """Scan every word in text and collect recognized canonical allergen names."""
    found: list[str] = []
    for word in re.split(r"[\s,;.]+", text):
        canonical = normalize_allergen_from_text(word)
        if canonical and canonical not in found:
            found.append(canonical)
    return found


def extract_allergies(message: str) -> tuple[list[str], list[str]]:
    """Return (allergies_to_add, allergies_to_remove) as normalized canonical names.

    Uses a two-pass approach:
    1. Regex to capture the noun phrase after the trigger.
    2. Word-level ALLERGEN_MAP scan on captured phrase.
    If regex fails (end-of-string edge case), fall back to scanning the full
    sentence that contains the trigger.
    """
    to_add: list[str] = []
    to_remove: list[str] = []

    # ── Removal pass ──────────────────────────────────────────────────────────
    for match in _ALLERGY_REMOVE.finditer(message):
        phrase = match.group(1).strip()
        for allergen in _extract_allergens_from_text(phrase):
            if allergen not in to_remove:
                to_remove.append(allergen)

    # Fallback: if removal trigger exists but regex captured nothing
    if not to_remove and _REMOVE_TRIGGER.search(message):
        # Scan words after the trigger in the full message
        trigger_match = _REMOVE_TRIGGER.search(message)
        if trigger_match:
            after = message[trigger_match.end():]
            for allergen in _extract_allergens_from_text(after):
                if allergen not in to_remove:
                    to_remove.append(allergen)

    # ── Addition pass ─────────────────────────────────────────────────────────
    # Skip sentences that contain a removal trigger to avoid double-counting.
    add_message = message
    if _REMOVE_TRIGGER.search(message):
        # Strip sentences containing removal triggers
        sentences = re.split(r"[.;\n]", message)
        add_message = " ".join(
            s for s in sentences if not _REMOVE_TRIGGER.search(s)
        )

    for match in _ALLERGY_ADD.finditer(add_message):
        phrase = match.group(1).strip()
        for allergen in _extract_allergens_from_text(phrase):
            if allergen not in to_add:
                to_add.append(allergen)

    # Fallback: if add trigger exists but regex captured nothing
    if not to_add and _ADD_TRIGGER.search(add_message):
        trigger_match = _ADD_TRIGGER.search(add_message)
        if trigger_match:
            after = add_message[trigger_match.end():]
            for allergen in _extract_allergens_from_text(after):
                if allergen not in to_add:
                    to_add.append(allergen)

    return to_add, to_remove


# ── Healthy / High-Protein Flags ──────────────────────────────────────────────

_HEALTHY_ON = re.compile(
    r"\b(healthy|low.?calorie|diet|kalori rendah|rendah kalori|sehat|light meal|gym meal|weight loss|mau diet)\b",
    re.IGNORECASE,
)
_HEALTHY_OFF = re.compile(
    r"\b(not healthy|no diet|bukan diet|tidak diet|sudah tidak diet)\b",
    re.IGNORECASE,
)
_PROTEIN_ON = re.compile(
    r"\b(high.?protein|protein tinggi|banyak protein|muscle|gym|fitness)\b",
    re.IGNORECASE,
)
_PROTEIN_OFF = re.compile(
    r"\b(not high protein|no protein preference|tidak perlu protein tinggi)\b",
    re.IGNORECASE,
)


def extract_healthy(message: str) -> bool | None:
    if _HEALTHY_OFF.search(message):
        return False
    if _HEALTHY_ON.search(message):
        return True
    return None


def extract_high_protein(message: str) -> bool | None:
    if _PROTEIN_OFF.search(message):
        return False
    if _PROTEIN_ON.search(message):
        return True
    return None


# ── Main Update Function ──────────────────────────────────────────────────────

def update_preferences(preferences: dict, message: str) -> dict:
    """Parse the latest customer message and update the preference dict in-place.

    This is the single entry point called before every Gemini request.

    Args:
        preferences: Current preference dict (mutated in-place).
        message:     Latest raw customer message.

    Returns:
        Updated preference dict (same object).
    """
    prefs = preferences.copy()

    # Budget
    budget_value, should_reset = extract_budget(message)
    if should_reset:
        prefs["budget"] = None
    elif budget_value is not None:
        prefs["budget"] = budget_value

    # Vegetarian
    veg = extract_vegetarian(message)
    if veg is not None:
        prefs["vegetarian"] = veg

    # Halal
    halal = extract_halal(message)
    if halal is not None:
        prefs["halal_only"] = halal

    # Spicy
    spicy = extract_spicy_level(message)
    if spicy == "remove":
        prefs["spicy_level_max"] = None
    elif spicy is not None:
        prefs["spicy_level_max"] = spicy

    # Allergies
    to_add, to_remove = extract_allergies(message)
    current_allergies: list[str] = list(prefs.get("allergies", []))
    for allergen in to_add:
        if allergen not in current_allergies:
            current_allergies.append(allergen)
    for allergen in to_remove:
        if allergen in current_allergies:
            current_allergies.remove(allergen)
    prefs["allergies"] = current_allergies

    # Healthy
    healthy = extract_healthy(message)
    if healthy is not None:
        prefs["healthy"] = healthy

    # High protein
    protein = extract_high_protein(message)
    if protein is not None:
        prefs["high_protein"] = protein

    return prefs
