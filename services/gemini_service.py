"""
services/gemini_service.py — Google Gemini API integration.

Wraps the google-genai SDK to send prompts and return Sora's response.
All API errors are caught here; callers receive a friendly fallback string
instead of a raw exception.
"""

from __future__ import annotations

import config


def _get_client():
    """Lazily initialise and return the Gemini client.

    Returns:
        google.genai.Client instance.

    Raises:
        ValueError: if GOOGLE_API_KEY is not set.
    """
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")
    from google import genai  # type: ignore
    return genai.Client(api_key=config.GOOGLE_API_KEY)


def send_message(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response.

    Args:
        prompt: The fully assembled prompt string from prompt_builder.

    Returns:
        Sora's response text, or a friendly error message on failure.
    """
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt,
        )
        text = response.text
        if not text or not text.strip():
            return (
                "Mohon maaf, saya tidak dapat menjawab saat ini. "
                "Silakan coba lagi dalam beberapa saat. 🙏\n\n"
                "*(I'm sorry, I'm unable to respond right now. Please try again shortly.)*"
            )
        return text.strip()

    except ValueError as exc:
        # Missing API key
        return (
            "⚠️ **API Key belum dikonfigurasi.**\n\n"
            "Silakan tambahkan `GOOGLE_API_KEY` pada file `.env` untuk mengaktifkan Sora.\n\n"
            "*(Please set your `GOOGLE_API_KEY` in the `.env` file.)*"
        )
    except Exception as exc:
        error_str = str(exc).lower()

        if "quota" in error_str or "rate" in error_str or "429" in error_str:
            return (
                "Maaf, layanan sedang sibuk. Mohon tunggu sebentar dan coba lagi. 🙏\n\n"
                "*(Service is temporarily busy. Please wait a moment and try again.)*"
            )
        if "timeout" in error_str or "deadline" in error_str:
            return (
                "Koneksi membutuhkan waktu lebih lama dari biasanya. "
                "Periksa koneksi internet Anda dan coba lagi. 🌐\n\n"
                "*(Connection timed out. Please check your internet and try again.)*"
            )
        if "network" in error_str or "connection" in error_str:
            return (
                "Tidak dapat terhubung ke layanan AI. "
                "Pastikan Anda terhubung ke internet. 🌐\n\n"
                "*(Unable to connect to AI service. Please check your internet connection.)*"
            )
        # Generic fallback — never expose the raw exception to the user
        return (
            "Mohon maaf, terjadi kendala teknis. Sora akan segera kembali! 🍵\n\n"
            "*(Sorry, a technical issue occurred. Please try again.)*"
        )


def check_api_connection() -> tuple[bool, str]:
    """Quickly test whether the API key is valid and the service is reachable.

    Returns:
        (True, "Connected")  on success.
        (False, reason_msg)  on failure.
    """
    if not config.GOOGLE_API_KEY:
        return False, "API key not set"
    if config.GOOGLE_API_KEY.startswith("YOUR_"):
        return False, "API key is placeholder"
    try:
        client = _get_client()
        # Minimal probe — list models to check connectivity without burning tokens
        client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents="Hi",
        )
        return True, "Connected"
    except Exception as exc:
        return False, str(exc)[:80]
