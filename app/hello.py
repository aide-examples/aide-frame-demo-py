#!/usr/bin/env python3
"""
Hello - A minimal aide-frame example application.

Demonstrates how to use our set of technical components (*aide-frame*) for a simple web application that:
- Serves a web UI
- Accepts user input (name)
- Makes an external API call (Behind The Name)
- Returns a response
"""

import os
import sys
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# =============================================================================
# PATH SETUP
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Add app directory to Python path
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Add aide-frame to Python path (submodule or embedded)
AIDE_FRAME_PATH = os.path.join(PROJECT_DIR, 'aide-frame', 'python')
if os.path.isdir(AIDE_FRAME_PATH) and AIDE_FRAME_PATH not in sys.path:
    sys.path.insert(0, AIDE_FRAME_PATH)

# =============================================================================
# AIDE-FRAME IMPORTS
# =============================================================================

from aide_frame import paths
paths.init(SCRIPT_DIR)

# Register help directory
paths.register("HELP_DIR", os.path.join(paths.APP_DIR, "help"))

from aide_frame.log import logger, set_level
from aide_frame.config import load_config
from aide_frame.web_request import fetch_json

# Local imports
import help_viewer

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_CONFIG = {
    "port": 8082,
    "btn_api_key": "",  # Behind The Name API key (optional)
}

# =============================================================================
# NAME ETYMOLOGY SERVICE
# =============================================================================

class EtymologyService:
    """Service for looking up name etymologies."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.demo_data = {
            "max": {"meaning": "Greatest", "origin": "Latin (Maximus)", "gender": "masculine"},
            "anna": {"meaning": "Grace, favor", "origin": "Hebrew (Hannah)", "gender": "feminine"},
            "paul": {"meaning": "Small, humble", "origin": "Latin (Paulus)", "gender": "masculine"},
            "maria": {"meaning": "Beloved, sea of bitterness", "origin": "Hebrew (Miriam)", "gender": "feminine"},
            "peter": {"meaning": "Rock, stone", "origin": "Greek (Petros)", "gender": "masculine"},
            "sarah": {"meaning": "Princess", "origin": "Hebrew", "gender": "feminine"},
        }

    def lookup(self, name):
        """Look up name info using free APIs."""
        name_lower = name.lower().strip()

        # Try free APIs (no key required)
        result = self._lookup_free_apis(name)
        if result:
            return result

        # Fallback to demo data for etymology
        if name_lower in self.demo_data:
            data = self.demo_data[name_lower]
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

    def _lookup_free_apis(self, name):
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
# HTTP SERVER
# =============================================================================

class HelloApp:
    """Main application class."""

    def __init__(self, config):
        self.config = config
        self.port = config.get("port", 8082)
        self.etymology = EtymologyService(config.get("btn_api_key"))
        self._server = None
        self._thread = None

    def start(self):
        """Start the HTTP server."""
        handler = self._create_handler()
        self._server = HTTPServer(('0.0.0.0', self.port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        logger.info(f"Hello server started on http://localhost:{self.port}")

    def stop(self):
        """Stop the HTTP server."""
        if self._server:
            self._server.shutdown()

    def _create_handler(self):
        """Create HTTP request handler."""
        app = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                logger.debug(f"HTTP: {args[0]}")

            def send_json(self, data, status=200):
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            def send_html(self, html):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode())

            def send_text(self, text, content_type='text/plain'):
                self.send_response(200)
                self.send_header('Content-Type', f'{content_type}; charset=utf-8')
                self.end_headers()
                self.wfile.write(text.encode())

            def send_css(self, css):
                self.send_response(200)
                self.send_header('Content-Type', 'text/css; charset=utf-8')
                self.end_headers()
                self.wfile.write(css.encode())

            def do_GET(self):
                parsed = urlparse(self.path)
                path = parsed.path
                query = parse_qs(parsed.query)

                if path == '/' or path == '/index.html':
                    self.serve_index()
                elif path == '/help' or path == '/help.html':
                    self.serve_help()
                elif path == '/status':
                    self.send_json({"ready": True, "api_configured": bool(app.config.get("btn_api_key"))})
                elif path == '/static/base.css':
                    self.serve_static('base.css', 'text/css')
                elif path == '/api/help/structure':
                    self.send_json(help_viewer.get_help_structure())
                elif path.startswith('/api/help/'):
                    filename = path[10:]  # Remove '/api/help/'
                    content = help_viewer.load_help_file(filename)
                    if content:
                        self.send_text(content, 'text/markdown')
                    else:
                        self.send_json({"error": "Help file not found"}, 404)
                else:
                    self.send_json({"error": "Not found"}, 404)

            def do_POST(self):
                parsed = urlparse(self.path)
                path = parsed.path

                # Read POST body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'

                try:
                    data = json.loads(body) if body else {}
                except json.JSONDecodeError:
                    self.send_json({"error": "Invalid JSON"}, 400)
                    return

                if path == '/etymology':
                    name = data.get('name', '').strip()
                    if not name:
                        self.send_json({"error": "Name is required"}, 400)
                        return

                    result = app.etymology.lookup(name)
                    self.send_json(result)
                else:
                    self.send_json({"error": "Not found"}, 404)

            def serve_index(self):
                """Serve the main HTML page."""
                static_path = os.path.join(SCRIPT_DIR, 'static', 'index.html')
                with open(static_path, 'r') as f:
                    self.send_html(f.read())

            def serve_help(self):
                """Serve the help page."""
                static_path = os.path.join(SCRIPT_DIR, 'static', 'help.html')
                with open(static_path, 'r') as f:
                    self.send_html(f.read())

            def serve_static(self, filename, content_type):
                """Serve a static file."""
                static_path = os.path.join(SCRIPT_DIR, 'static', filename)
                try:
                    with open(static_path, 'r') as f:
                        self.send_text(f.read(), content_type)
                except FileNotFoundError:
                    self.send_json({"error": "File not found"}, 404)

        return Handler

# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Hello - Name Etymology Lookup')
    parser.add_argument('--config', '-c', default='hello_config.json',
                        help='Path to config file')
    parser.add_argument('--port', '-p', type=int,
                        help='Override port')
    parser.add_argument('--log-level', '-l', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Log level')
    args = parser.parse_args()

    # Set log level
    set_level(args.log_level)

    # Load config
    config = load_config(
        config_path=args.config,
        search_paths=[
            os.path.join(PROJECT_DIR, 'hello_config.json'),
            os.path.join(SCRIPT_DIR, 'hello_config.json'),
        ],
        defaults=DEFAULT_CONFIG
    )

    # Override port if specified
    if args.port:
        config['port'] = args.port

    # Start app
    app = HelloApp(config)
    app.start()

    logger.info("Press Ctrl+C to stop")

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        app.stop()

if __name__ == '__main__':
    main()
