# Initial Setup Instructions for Claude

> **DISCLAIMER**: These instructions are currently copied from the Node.js demo and must be adapted for Python before use. Key differences include:
> - Python uses `requirements.txt` instead of `package.json`
> - Python uses `config.yaml` instead of `config.json`
> - Python uses virtual environments instead of node_modules
> - Server code structure differs (Flask-based vs Express-based)
> - File extensions are `.py` instead of `.js`

This document tells Claude how to set up a new aide-frame application.

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
- `requirements.txt` - adapt dependencies
- `run` - adapt to call your app's entry point
- `app/demo.py` - simplify to create your `app/{APP_NAME_LOWER}.py`
- `app/static/demo/` - simplify to create `app/static/{APP_NAME_LOWER}/`
- `app/static/locales/` - simplify, keeping only app_title

### 3. Key Differences from Demo

When creating the new app:
- **Remove** the demos/ directory and all demo imports
- **Keep** docsConfig with appName, but remove customRoots (no sample_docs)
- **Keep** updateConfig with githubRepo and serviceName (adapt for your app)
- **Note**: HttpServer auto-registers httpRoutes and updateRoutes when configs are provided
- **Remove** /api/demos and /api/demo/:name routes
- **Keep** app/docs/ and app/help/ directories - adapt content for new app
- **Simplify** HTML to just header, "Hello" content, and footer
- **Simplify** client JS to just widget initialization
- **Simplify** locales to just app_title translation

### 4. Setup Steps

1. Initialize git: `git init`
2. Add aide-frame submodule (check .gitmodules in demo for source path)
   - If git blocks file:// protocol: `git config --global protocol.file.allow always`
3. Create directory structure: `mkdir -p app/static/{APP_NAME_LOWER} app/static/locales app/docs app/help`
4. Create `.gitignore` with:
   ```
   venv/
   __pycache__/
   *.pyc
   ```
5. Create files by adapting from demo:
   - `requirements.txt` (adapt dependencies)
   - `run` (change script name)
   - `app/config.yaml` (set PORT)
   - `app/VERSION` (copy as-is)
   - `app/{APP_NAME_LOWER}.py` (simplified server)
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.html` (minimal page)
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.js` (widget init only)
   - `app/static/{APP_NAME_LOWER}/{APP_NAME_LOWER}.css` (minimal styles)
   - `app/static/locales/en.json`, `de.json`, `es.json` (app_title only)
   - `app/docs/index.md` (adapt from demo, describe your app)
   - `app/help/index.md` (adapt from demo, describe your app)
6. Create virtual environment: `python -m venv venv`
7. Install dependencies: `./venv/bin/pip install -r requirements.txt`
8. Test with `./run` or `./venv/bin/python app/{APP_NAME_LOWER}.py`

### 5. Verification

After setup, verify at http://localhost:{PORT}:
- Header shows APP_NAME with language selector
- Body shows "Hello"
- Footer shows version/platform info

### 6. Final Message to User

After successful setup, tell the user:

> Setup complete! Please test the application by running `./run` and opening
> http://localhost:{PORT} in your browser. Verify that header, content, and
> footer display correctly. When satisfied, make an initial git commit:
> ```
> git add .
> git commit -m "Initial project setup"
> ```

## Common Issues

- **Port in use**: Use `--port XXXX` or change config.yaml
- **Git submodule file protocol error**: Run `git config --global protocol.file.allow always`
- **"No config file found"**: Normal when running from project root; DEFAULT_CONFIG in server handles this
