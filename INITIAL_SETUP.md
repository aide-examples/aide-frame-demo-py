# Initial Setup Instructions for Claude

This document tells Claude how to set up a new aide-frame Python application.

## Prerequisites

- The user has created DESCRIPTION.md with their app configuration
- The aide-frame-demo-py template is available (typically at ../aide-frame-demo-py)

## Setup Process

When asked to set up this project, follow these steps:

### 1. Read DESCRIPTION.md

Extract the configuration values:
- APP_NAME (e.g., "My LAN")
- APP_NAME_LOWER (e.g., "mylan")
- APP_DESCRIPTION
- PORT

### 2. Use aide-frame-demo-py as Reference

The template at ../aide-frame-demo-py shows the complete structure. Study:
- `run` - adapt to call your app's entry point
- `app/demo.py` - simplify to create your `app/{APP_NAME_LOWER}.py`
- `app/static/demo/` - simplify to create `app/static/{APP_NAME_LOWER}/`
- `app/static/locales/` - simplify, keeping only app_title and hello

### 3. Key Differences from Demo

When creating the new app:
- **Remove** the demos/ directory and all demo imports
- **Keep** docs_config with app_name, but remove custom_roots (no sample_docs)
- **Keep** update_config with github_repo and service_name (adapt for your app)
- **Note**: HttpServer auto-registers http_routes and update_routes when configs are provided
- **Remove** /api/demos and /api/demo/:name routes
- **Keep** app/docs/ and app/help/ directories - adapt content for new app
- **Simplify** HTML to just header, "Hello" content, and footer area with status information
- **Simplify** client JS to just widget initialization (i18n, HeaderWidget, StatusWidget)
- **Simplify** locales to just app_title and hello translations

### 4. Setup Steps

1. Initialize git: `git init`
2. Add aide-frame submodule: `git submodule add /home/gero/aide-examples/aide-frame aide-frame`
   - Check .gitmodules in demo for the exact source path if different
   - If git blocks file:// protocol: `git config --global protocol.file.allow always`
3. Create directory structure: `mkdir -p app/static/{APP_NAME_LOWER} app/static/locales app/static/icons app/docs app/help`
4. Create `.gitignore` with:
   ```
   __pycache__/
   *.pyc
   *.pyo
   .DS_Store
   deploy/

   # User config (not tracked, copy from config_sample.json)
   app/config.json
   releases/
   ```
5. Create files by adapting from demo:
   - `run` (change script name, make executable with `chmod +x run`)
   - `app/config.json` (set port and PWA settings - see aide-frame/python/aide_frame/config_sample.json)
   - `app/config_sample.json` (copy of config.json for version control)
   - `app/VERSION` (start at 0.1)
   - `app/{APP_NAME_LOWER}.py` (simplified server)
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.html` (minimal page with header, content, footer area with status information, include manifest link and PWA.init())
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.js` (widget init only)
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.css` (minimal styles)
   - `app/static/icons/icon-192.svg` and `icon-512.svg` (app-specific PWA icons)
   - `app/static/locales/en.json`, `de.json`, `es.json` (app_title and hello only)
   - `app/docs/index.md` (adapt from demo, describe your app)
   - `app/help/index.md` (adapt from demo, describe your app)
6. Test with `./run`

### 5. Verification

After setup, verify at http://localhost:{PORT}:
- Header shows APP_NAME with language selector
- Body shows "Hello"
- Footer area shows version/platform status information
- PWA: Check browser DevTools → Application → Manifest (should show app name and icons)
- PWA: Check browser DevTools → Application → Service Workers (should be registered)

### 6. Final Message to User

After successful setup, tell the user:

> Setup complete! Please test the application by running `./run` and opening
> http://localhost:{PORT} in your browser. Verify that header, content, and
> footer area display correctly. When satisfied, make an initial git commit:
> ```
> git add .
> git commit -m "Initial project setup"
> ```

## Common Issues

- **Port in use**: Use `--port XXXX` or change app/config.json
- **Git submodule file protocol error**: Run `git config --global protocol.file.allow always`
- **"No config file found"**: Normal when running from project root; DEFAULT_CONFIG in server handles this

## Code Structure Patterns

All aide-frame applications should follow a consistent code structure for maintainability. The main entry file should be organized with numbered section headers in this order:

1. **PATH SETUP** - Define SCRIPT_DIR, PROJECT_DIR, add aide-frame to path
2. **AIDE-FRAME INIT** - Import paths module and call paths.init(SCRIPT_DIR)
3. **AIDE-FRAME IMPORTS** - Import framework modules (http_server, http_routes, args, etc.)
4. **APP IMPORTS** - Import application-specific modules
5. **CONFIGURATION** - Define DEFAULT_CONFIG with sensible defaults
6. **HTTP HANDLER** (Python) or skip (JS uses inline routes) - Define request handler class
7. **ARGUMENT PARSING** - Use framework's args module (add_common_args, apply_common_args)
8. **SERVER SETUP** - Create HttpServer with docsConfig and updateConfig
9. **START SERVER** - Call server.run()

Key patterns to follow:
- Use the framework's args module for command-line parsing (--config, --log-level, --regenerate-icons are provided by add_common_args)
- Let HttpServer auto-register docs/help and update routes when configs are provided
- Pass PWA config to docsConfig for manifest.json serving
- Keep DEFAULT_CONFIG inline for simple apps; use a separate config module only for complex apps
- Don't mutate framework globals; pass configuration through constructors instead
- Resolve config path relative to SCRIPT_DIR before calling apply_common_args

## Important Notes

**Locale files:** Translate `app_title` appropriately for each language, don't just copy the English name.
