"""Demo: Configuration loading with aide_frame.config."""

import os

from aide_frame import config, paths

TITLE = "Configuration"
DESCRIPTION = "Demonstrates config loading with defaults, search paths, and overrides"


def run(data: dict) -> dict:
    """
    Run the config demo.

    Input: {"key": "port", "default": 8080}
    Output: {"key": "port", "value": 8080, "source": "default"}
    """
    action = data.get('action', 'show_paths')

    if action == 'show_paths':
        # Show registered paths
        return {
            "action": "show_paths",
            "paths": {
                "APP_DIR": paths.get("APP_DIR", "not set"),
                "STATIC_DIR": paths.get("STATIC_DIR", "not set"),
                "DOCS_DIR": paths.get("DOCS_DIR", "not set"),
            }
        }

    elif action == 'load_config':
        # Demonstrate config loading with defaults
        defaults = {"port": 8080, "debug": False, "name": "Demo App"}
        # Resolve config path relative to APP_DIR
        config_path = data.get('config_path', 'config.json')
        app_dir = paths.get("APP_DIR")
        if app_dir and not os.path.isabs(config_path):
            config_path = os.path.join(app_dir, config_path)
        cfg = config.load_config(
            config_path=config_path,
            defaults=defaults
        )
        return {
            "action": "load_config",
            "config": cfg,
            "defaults_used": defaults
        }

    elif action == 'get_value':
        # Get a specific config value
        key = data.get('key', 'port')
        default = data.get('default', None)
        defaults = {key: default} if default is not None else {}
        cfg = config.load_config(defaults=defaults)
        return {
            "action": "get_value",
            "key": key,
            "value": cfg.get(key, default),
            "found": key in cfg
        }

    return {"error": f"Unknown action: {action}"}, 400
