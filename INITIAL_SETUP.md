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
2. Add aide-frame submodule from GitHub:
   ```bash
   git submodule add https://github.com/aide-examples/aide-frame.git aide-frame
   ```
3. For local development (optional), switch to symlink mode:
   ```bash
   ../aide-frame/dev-mode.sh
   ```
   See [aide-frame/docs/spec/app-structure.md](aide-frame/docs/spec/app-structure.md) for details on dev vs prod mode.
4. Create directory structure: `mkdir -p app/static/{APP_NAME_LOWER} app/static/locales app/static/icons app/docs app/help`
5. Create `.gitignore` with:
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
6. Create files by adapting from demo:
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
7. Test with `./run`

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

## Config File Structure

Both `config.json` and `config_sample.json` must include all framework settings. App-specific settings can be added after the framework settings.

**Required framework settings:**

```json
{
    "_comment": "Copy this file to config.json and customize for your app",
    "port": 8082,
    "log_level": "INFO",
    "pwa": {
        "enabled": true,
        "name": "Your App Name",
        "short_name": "AppName",
        "description": "Your app description",
        "theme_color": "#306998",
        "background_color": "#ffffff",
        "icon_192": "/static/icons/icon-192.svg",
        "icon_512": "/static/icons/icon-512.svg",
        "icon": {
            "background": "#306998",
            "line1_text": "aide",
            "line1_color": "#94a3b8",
            "line1_size": 0.25,
            "line2_text": "App",
            "line2_color": "#ffffff",
            "line2_size": 0.45
        }
    },
    "layout": {
        "default": "flow",
        "allow_toggle": true
    }
}
```

**Settings explained:**
- `port`: Server port number
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `pwa`: Progressive Web App configuration
  - `icon_192`, `icon_512`: Paths to PWA icons (auto-generated if icon config provided)
  - `icon`: Icon generation settings (background color, text lines with colors and sizes)
- `layout.default`: Default layout mode ("flow" or "page-fill")
- `layout.allow_toggle`: Allow user to switch between layout modes

**Note:** The `_comment` field is optional and only used in `config_sample.json` to remind users to copy the file.

## Common Issues

- **Port in use**: Use `--port XXXX` or change app/config.json
- **"No config file found"**: Ensure config path is resolved relative to SCRIPT_DIR before calling apply_common_args - this is critical for PM2/systemd

## Code Structure Patterns

**IMPORTANT:** Follow the standard code structure defined in the framework documentation:
[aide-frame/docs/spec/app-structure.md](aide-frame/docs/spec/app-structure.md)

This guide defines numbered section headers, key patterns for args handling, HttpServer setup, and PWA configuration.

## Important Notes

**Locale files:** Translate `app_title` appropriately for each language, don't just copy the English name.

## Client-Side Setup Requirements

These requirements apply to both Python and JavaScript apps - they use the same client-side framework.

### 1. Script Dependencies and Load Order

The HTML must include scripts in this exact order:

```html
<script src="/static/frame/vendor/polyglot/polyglot.min.js"></script>
<script src="/static/frame/js/i18n.js"></script>
<script src="/static/frame/js/header-widget.js"></script>
<script src="/static/frame/js/status-widget.js"></script>
<script src="/static/frame/js/pwa.js"></script>
<script src="/static/{app}/{app}.js"></script>
```

**Critical:** The `polyglot.min.js` script MUST be loaded before `i18n.js`. Missing this breaks all widget initialization because `i18n.init()` will fail silently.

### 2. Widget Container Pattern

Use empty divs with IDs - widgets render their own content:

```html
<div class="app-container page-fill">
    <div id="app-header"></div>     <!-- HeaderWidget fills this -->

    <main class="main-content">
        <div class="scroll-content">
            <!-- Your app content here -->
        </div>
    </main>

    <div id="status-widget"></div>  <!-- StatusWidget fills this -->
</div>
```

Do NOT create manual header/footer HTML - the widgets generate their structure.

### 3. JavaScript Initialization Sequence

In your app.js, initialize in this order:

```javascript
document.addEventListener('DOMContentLoaded', async () => {
    await i18n.init();  // Must complete before widgets
    HeaderWidget.init('#app-header', { appName: 'Your App Name' });
    StatusWidget.init('#status-widget');
    PWA.init();
});
```

### 4. Page-Fill Layout Structure

For page-fill layout (fixed viewport, internal scrolling):
- Add `page-fill` class to `.app-container`
- Wrap content in `<main class="main-content">` with `<div class="scroll-content">` inside
- The framework CSS handles the flex layout automatically

## Server-Side Setup Requirements (Python)

### 1. paths.init() Must Be Called Early

Call `paths.init(SCRIPT_DIR)` immediately after imports, **before** creating DocsConfig:

```python
from aide_frame import paths, config as config_module
from aide_frame import http_server, http_routes, update_routes

# Initialize paths early (before DocsConfig which needs APP_DIR)
paths.init(SCRIPT_DIR)
```

**Critical:** DocsConfig auto-registers DOCS_DIR and HELP_DIR based on `paths.APP_DIR`. If paths.init() isn't called first, these directories won't be found and /about and /help will fail.

### 2. Use python3 in run Script

The `run` script should use `python3` explicitly:

```bash
#!/bin/bash
cd "$(dirname "$0")/app"
python3 {app}.py "$@"
```

### 3. Use log.set_level() Not setup_logging()

The logging module provides `set_level()`, not `setup_logging()`:

```python
log.set_level(config.get('log_level', 'INFO'))
```
