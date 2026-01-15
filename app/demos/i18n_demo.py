"""
i18n Demo - Demonstrates internationalization features.

This demo shows how aide-frame handles multiple languages
using Polyglot.js on the frontend. The language switching
is handled client-side via the i18n.js module.
"""


def run(data):
    """
    Get information about supported languages.

    Args:
        data: Request data (not used)

    Returns:
        dict with language information
    """
    return {
        "supported_languages": ["en", "de"],
        "language_names": {
            "en": "English",
            "de": "Deutsch"
        },
        "info": "Language switching is handled client-side via i18n.setLanguage()"
    }
