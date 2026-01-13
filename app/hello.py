#!/usr/bin/env python3
"""
Hello - A minimal aide-frame example application.

Demonstrates how to use aide-frame for a simple web application that:
- Serves a web UI
- Accepts user input (name)
- Makes an external API call (Behind The Name)
- Returns a response

This is a reference implementation showing aide-frame usage without
any slideshow/video-specific code.
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

from aide_frame.log import logger, set_level
from aide_frame.config import load_config
from aide_frame.web_request import fetch_json

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
        """Look up etymology for a name."""
        name_lower = name.lower().strip()

        # Try API if key is configured
        if self.api_key:
            result = self._lookup_api(name)
            if result:
                return result

        # Fallback to demo data
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
            "origin": "Could not find etymology for this name",
            "gender": "unknown",
            "source": "none"
        }

    def _lookup_api(self, name):
        """Look up name via Behind The Name API."""
        url = f"https://www.behindthename.com/api/lookup.json?name={name}&key={self.api_key}"

        try:
            data = fetch_json(url)
            if data and isinstance(data, list) and len(data) > 0:
                entry = data[0]
                return {
                    "name": entry.get("name", name),
                    "meaning": entry.get("info", {}).get("meaning", "Unknown"),
                    "origin": ", ".join([u.get("usage", "") for u in entry.get("usages", [])]),
                    "gender": entry.get("gender", "unknown"),
                    "source": "behindthename.com"
                }
        except Exception as e:
            logger.error(f"API error: {e}")

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

            def do_GET(self):
                parsed = urlparse(self.path)
                path = parsed.path

                if path == '/' or path == '/index.html':
                    self.serve_index()
                elif path == '/status':
                    self.send_json({"ready": True, "api_configured": bool(app.config.get("btn_api_key"))})
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
                if os.path.exists(static_path):
                    with open(static_path, 'r') as f:
                        self.send_html(f.read())
                else:
                    self.send_html(EMBEDDED_HTML)

        return Handler

# =============================================================================
# EMBEDDED HTML (fallback if static/index.html doesn't exist)
# =============================================================================

EMBEDDED_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello - Name Etymology</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e; color: #eee; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
        }
        .container { max-width: 500px; width: 90%; padding: 2rem; }
        h1 { text-align: center; margin-bottom: 2rem; color: #60a5fa; }
        .card {
            background: #16213e; border-radius: 12px; padding: 1.5rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            width: 100%; padding: 12px; border: none; border-radius: 8px;
            background: #0f3460; color: #fff; font-size: 1rem;
            margin-bottom: 1rem;
        }
        input[type="text"]::placeholder { color: #888; }
        button {
            width: 100%; padding: 12px; border: none; border-radius: 8px;
            background: #60a5fa; color: #000; font-size: 1rem;
            font-weight: 600; cursor: pointer; transition: background 0.2s;
        }
        button:hover { background: #93c5fd; }
        button:disabled { background: #444; cursor: not-allowed; }
        .result { display: none; }
        .result.show { display: block; }
        .result h2 { color: #60a5fa; margin-bottom: 0.5rem; }
        .result p { margin: 0.5rem 0; color: #ccc; }
        .result .label { color: #888; font-size: 0.9rem; }
        .source { font-size: 0.8rem; color: #666; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello!</h1>
        <div class="card">
            <input type="text" id="name-input" placeholder="Enter a name..." autofocus>
            <button onclick="lookup()" id="submit-btn">What does it mean?</button>
        </div>
        <div class="card result" id="result">
            <h2 id="result-name"></h2>
            <p><span class="label">Meaning:</span> <span id="result-meaning"></span></p>
            <p><span class="label">Origin:</span> <span id="result-origin"></span></p>
            <p><span class="label">Gender:</span> <span id="result-gender"></span></p>
            <p class="source">Source: <span id="result-source"></span></p>
        </div>
    </div>
    <script>
        const input = document.getElementById('name-input');
        const btn = document.getElementById('submit-btn');
        const result = document.getElementById('result');

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') lookup();
        });

        async function lookup() {
            const name = input.value.trim();
            if (!name) return;

            btn.disabled = true;
            btn.textContent = 'Looking up...';

            try {
                const res = await fetch('/etymology', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name})
                });
                const data = await res.json();

                document.getElementById('result-name').textContent = data.name;
                document.getElementById('result-meaning').textContent = data.meaning;
                document.getElementById('result-origin').textContent = data.origin;
                document.getElementById('result-gender').textContent = data.gender;
                document.getElementById('result-source').textContent = data.source;
                result.classList.add('show');
            } catch (e) {
                alert('Error: ' + e.message);
            } finally {
                btn.disabled = false;
                btn.textContent = 'What does it mean?';
            }
        }
    </script>
</body>
</html>
"""

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
