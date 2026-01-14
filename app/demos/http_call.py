"""Demo: HTTP API calls using aide_frame.web_request."""

from aide_frame.web_request import fetch_json
from aide_frame.log import logger

TITLE = "HTTP API Call"
DESCRIPTION = "Demonstrates fetching JSON from external APIs (Genderize.io)"

# Demo data for offline fallback
DEMO_DATA = {
    "max": {"gender": "male", "probability": 0.99},
    "anna": {"gender": "female", "probability": 0.98},
    "alex": {"gender": "male", "probability": 0.62},
}


def run(data: dict) -> dict:
    """
    Run the HTTP call demo.

    Input: {"name": "Max"}
    Output: {"name": "Max", "gender": "male", "probability": 0.99, "source": "api"}
    """
    name = data.get('name', '').strip()
    if not name:
        return {"error": "Name is required"}, 400

    # Try live API first
    try:
        result = fetch_json(f"https://api.genderize.io/?name={name}")
        if result and result.get("gender"):
            return {
                "name": result.get("name", name),
                "gender": result.get("gender"),
                "probability": result.get("probability", 0),
                "count": result.get("count", 0),
                "source": "genderize.io"
            }
    except Exception as e:
        logger.warning(f"API call failed: {e}")

    # Fallback to demo data
    name_lower = name.lower()
    if name_lower in DEMO_DATA:
        demo = DEMO_DATA[name_lower]
        return {
            "name": name,
            "gender": demo["gender"],
            "probability": demo["probability"],
            "count": 0,
            "source": "demo_data"
        }

    return {
        "name": name,
        "gender": "unknown",
        "probability": 0,
        "count": 0,
        "source": "not_found"
    }
