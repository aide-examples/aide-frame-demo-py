#!/usr/bin/env python3
"""Minimal aide-frame example - demonstrates the framework basics."""

import os
import sys

# =============================================================================
# 1. PATH SETUP
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

AIDE_FRAME_PATH = os.path.join(PROJECT_DIR, 'aide-frame', 'python')
if os.path.isdir(AIDE_FRAME_PATH) and AIDE_FRAME_PATH not in sys.path:
    sys.path.insert(0, AIDE_FRAME_PATH)

# =============================================================================
# 2. AIDE-FRAME INIT
# =============================================================================

from aide_frame import paths
paths.init(SCRIPT_DIR)

# =============================================================================
# 3. AIDE-FRAME IMPORTS
# =============================================================================

from aide_frame import http_routes, http_server, update_routes
from aide_frame.args import add_common_args, apply_common_args

# =============================================================================
# 4. APP IMPORTS
# =============================================================================

from demos import DEMOS

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_CONFIG = {"port": 8082}

# =============================================================================
# HTTP HANDLER
# =============================================================================

class HelloHandler(http_server.JsonHandler):
    """HTTP handler routing to demo modules."""

    def get(self, path, params):
        if path == '/' or path == '/index.html':
            return self.file('demo/demo.html')
        if path == '/api/demos':
            return {"demos": list(DEMOS.keys())}
        return {"error": "Not found"}, 404

    def post(self, path, data):
        # Route /api/demo/<name> to demo modules
        if path.startswith('/api/demo/'):
            demo_name = path[10:]  # Remove '/api/demo/'
            if demo_name in DEMOS:
                return DEMOS[demo_name].run(data)
            return {"error": f"Unknown demo: {demo_name}"}, 404
        return {"error": "Not found"}, 404

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='AIDE Frame Demo App')
    add_common_args(parser, config_default='config.json')
    parser.add_argument('--port', '-p', type=int, help='Override port')
    args = parser.parse_args()

    config = apply_common_args(
        args,
        config_search_paths=[os.path.join(PROJECT_DIR, 'config.json')],
        config_defaults=DEFAULT_CONFIG
    )

    if args.port:
        config['port'] = args.port

    server = http_server.HttpServer(
        port=config['port'],
        handler_class=HelloHandler,
        app_dir=SCRIPT_DIR,
        docs_config=http_routes.DocsConfig(
            app_name="AIDE Demo",
            custom_roots={
                "sample_docs": http_routes.CustomRoot(
                    dir_key="SAMPLE_DOCS_DIR",
                    title="Sample Docs",
                    route="/sample_docs",
                    subdir="sample_docs",
                )
            }
        ),
        update_config=update_routes.UpdateConfig(
            github_repo="aide-examples/aide-hello",
            service_name="aide-hello"
        ),
    )
    server.run()
