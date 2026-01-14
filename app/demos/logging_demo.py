"""Demo: Logging with aide_frame.log."""

import logging
from aide_frame.log import logger, set_level

TITLE = "Logging"
DESCRIPTION = "Demonstrates logging levels and structured log output"


def run(data: dict) -> dict:
    """
    Run the logging demo.

    Input: {"action": "log", "level": "INFO", "message": "Test message"}
    Output: {"logged": true, "level": "INFO", "message": "Test message"}
    """
    action = data.get('action', 'status')

    if action == 'status':
        # Show current logging status
        current_level = logging.getLevelName(logger.getEffectiveLevel())
        return {
            "action": "status",
            "current_level": current_level,
            "available_levels": ["DEBUG", "INFO", "WARNING", "ERROR"]
        }

    elif action == 'set_level':
        # Change log level
        level = data.get('level', 'INFO').upper()
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            return {"error": f"Invalid level: {level}"}, 400
        old_level = logging.getLevelName(logger.getEffectiveLevel())
        set_level(level)
        return {
            "action": "set_level",
            "old_level": old_level,
            "new_level": level
        }

    elif action == 'log':
        # Log a message at specified level
        level = data.get('level', 'INFO').upper()
        message = data.get('message', 'Demo log message')

        if level == 'DEBUG':
            logger.debug(message)
        elif level == 'INFO':
            logger.info(message)
        elif level == 'WARNING':
            logger.warning(message)
        elif level == 'ERROR':
            logger.error(message)
        else:
            return {"error": f"Invalid level: {level}"}, 400

        return {
            "action": "log",
            "logged": True,
            "level": level,
            "message": message,
            "note": "Check terminal output to see the log entry"
        }

    return {"error": f"Unknown action: {action}"}, 400
