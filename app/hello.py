#!/usr/bin/env python3
"""
Hello - A minimal aide-frame example application.

Demonstrates how to use aide-frame for a simple web application that:
- Serves a web UI
- Accepts user input (name)
- Makes an external API call (Genderize/Agify)
- Returns a response
"""

import os
import sys

# =============================================================================
# 1. PATH SETUP - Must be done before importing aide-frame
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Add aide-frame to Python path (submodule)
AIDE_FRAME_PATH = os.path.join(PROJECT_DIR, 'aide-frame', 'python')
if os.path.isdir(AIDE_FRAME_PATH) and AIDE_FRAME_PATH not in sys.path:
    sys.path.insert(0, AIDE_FRAME_PATH)

# =============================================================================
# 2. AIDE-FRAME INIT - paths.init() MUST come before other aide-frame imports
# =============================================================================

from aide_frame import paths
paths.init(SCRIPT_DIR)

# =============================================================================
# 3. AIDE-FRAME IMPORTS - Safe now that paths is initialized
# =============================================================================

from aide_frame import http_routes, http_server
from aide_frame.log import logger, set_level
from aide_frame.config import load_config
from aide_frame.web_request import fetch_json

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_CONFIG = {
    "port": 8082,
}

# =============================================================================
# NAME INFO SERVICE
# =============================================================================

class NameInfoService:
    """Service for looking up name info using free APIs."""

    DEMO_DATA = {
        "max": {"meaning": "Greatest", "origin": "Latin (Maximus)", "gender": "masculine"},
        "anna": {"meaning": "Grace, favor", "origin": "Hebrew (Hannah)", "gender": "feminine"},
        "paul": {"meaning": "Small, humble", "origin": "Latin (Paulus)", "gender": "masculine"},
        "maria": {"meaning": "Beloved, sea of bitterness", "origin": "Hebrew (Miriam)", "gender": "feminine"},
        "peter": {"meaning": "Rock, stone", "origin": "Greek (Petros)", "gender": "masculine"},
        "sarah": {"meaning": "Princess", "origin": "Hebrew", "gender": "feminine"},
    }

    def lookup(self, name: str) -> dict:
        """Look up name info using free APIs."""
        name_lower = name.lower().strip()

        # Try free APIs (no key required)
        result = self._lookup_free_apis(name)
        if result:
            return result

        # Fallback to demo data
        if name_lower in self.DEMO_DATA:
            data = self.DEMO_DATA[name_lower]
            return {
                "name": name,
                "meaning": data["meaning"],
                "origin": data["origin"],
                "gender": data["gender"],
                "source": "demo"
            }

        # Unknown name
        return {
            "name": name,
            "meaning": "Unknown",
            "origin": "Could not find info for this name",
            "gender": "unknown",
            "source": "none"
        }

    def _lookup_free_apis(self, name: str) -> dict | None:
        """Look up name using free Genderize and Agify APIs."""
        try:
            gender_data = fetch_json(f"https://api.genderize.io/?name={name}")
            age_data = fetch_json(f"https://api.agify.io/?name={name}")

            if gender_data and gender_data.get("gender"):
                gender = gender_data.get("gender", "unknown")
                probability = gender_data.get("probability", 0)
                age = age_data.get("age") if age_data else None

                meaning = f"Predicted {gender} ({probability*100:.0f}% confidence)"
                if age:
                    meaning += f", average age {age}"

                return {
                    "name": name,
                    "meaning": meaning,
                    "origin": f"Based on {gender_data.get('count', 0):,} records",
                    "gender": gender,
                    "source": "genderize.io + agify.io"
                }
        except Exception as e:
            logger.error(f"Free API error: {e}")

        return None


# =============================================================================
# HTTP HANDLER
# =============================================================================

# Global service instance (set in main)
name_service: NameInfoService = None


class HelloHandler(http_server.JsonHandler):
    """HTTP handler for Hello app."""

    def get(self, path, params):
        if path == '/' or path == '/index.html':
            return self.file('index.html')
        if path == '/status':
            return {"ready": True}
        return {"error": "Not found"}, 404

    def post(self, path, data):
        if path == '/etymology':
            name = data.get('name', '').strip()
            if not name:
                return {"error": "Name is required"}, 400
            return name_service.lookup(name)
        return {"error": "Not found"}, 404


# =============================================================================
# MAIN
# =============================================================================

def main():
    global name_service

    import argparse
    parser = argparse.ArgumentParser(description='Hello - Name Info Lookup')
    parser.add_argument('--config', '-c', default='hello_config.json', help='Config file')
    parser.add_argument('--port', '-p', type=int, help='Override port')
    parser.add_argument('--log-level', '-l', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    args = parser.parse_args()

    set_level(args.log_level)

    config = load_config(
        config_path=args.config,
        search_paths=[
            os.path.join(PROJECT_DIR, 'hello_config.json'),
            os.path.join(SCRIPT_DIR, 'hello_config.json'),
        ],
        defaults=DEFAULT_CONFIG
    )

    if args.port:
        config['port'] = args.port

    # Initialize service
    name_service = NameInfoService()

    # Configure docs/help routes
    docs_config = http_routes.DocsConfig(
        app_name="Hello",
        back_link="/",
        back_text="Home",
    )

    # Start server
    server = http_server.HttpServer(
        port=config['port'],
        handler_class=HelloHandler,
        app_dir=SCRIPT_DIR,
        docs_config=docs_config,
    )
    server.run()


if __name__ == '__main__':
    main()
