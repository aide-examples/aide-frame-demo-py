# AIDE - Frame Demo (Python)

An interactive demo application showcasing the features of the [aide-frame](https://github.com/aide-examples/aide-frame)framework.

This is the Python version. A JavaScript version (aide-frame-demo-js) will be available once aide-frame adds JavaScript support.

## Features

This demo showcases six core features of the aide-frame framework:

| Demo | Description | Framework Module |
|------|-------------|------------------|
| **HTTP API** | External API calls (Genderize.io) | `aide_frame.web_request` |
| **Config** | Configuration loading & path management | `aide_frame.config`, `aide_frame.paths` |
| **Logging** | Structured logging with log levels | `aide_frame.log` |
| **QR Code** | QR code generation as Base64 | `aide_frame.qrcode_utils` |
| **i18n** | Multi-language support (EN/DE) | `aide_frame` i18n.js |
| **Docs Viewer** | Markdown display with Mermaid diagrams | `aide_frame.docs_viewer` |

## Quick Start

```bash
# Clone with submodule
git clone --recursive https://github.com/aide-examples/aide-frame-demo-py.git
cd aide-frame-demo-py

# Run
./run
# or: python3 app/demo.py

# Open browser
# http://localhost:8082
```

## Project Structure

```
aide-frame-demo-py/
├── aide-frame/              # Git submodule (framework)
├── app/
│   ├── demo.py              # HTTP server & routing
│   ├── config.json          # App configuration
│   ├── VERSION              # Version (0.2)
│   ├── demos/               # Demo modules
│   │   ├── http_call.py
│   │   ├── config_demo.py
│   │   ├── logging_demo.py
│   │   ├── qrcode_demo.py
│   │   └── i18n_demo.py
│   ├── static/demo/         # Frontend (HTML, JS, CSS)
│   ├── docs/                # Documentation
│   ├── help/                # Help pages
│   └── sample_docs/         # Custom roots demo
├── run                      # Start script
└── README.md
```

## Configuration

`app/config.json`:

```json
{
    "port": 8082
}
```

## Internationalization

The app supports English and German. Language can be switched via:
- Header dropdown (provided by aide-frame)
- Flag buttons in the i18n demo panel

Language files:
- `app/static/locales/en.json`
- `app/static/locales/de.json`

## License

MIT
