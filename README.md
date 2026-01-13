# aide-hello

A minimal example application using the aide-frame framework.

## What it does

- Serves a simple web UI
- Asks for a name
- Returns the etymology (meaning and origin) of the name
- Uses Behind The Name API (with demo fallback)

## Quick Start

```bash
# Clone with submodule
git clone --recursive https://github.com/aide-examples/aide-hello.git
cd aide-hello

# Run
python3 app/hello.py

# Open browser
# http://localhost:8082
```

## Configuration

Edit `hello_config.json`:

```json
{
    "port": 8082,
    "btn_api_key": "YOUR_API_KEY"
}
```

To get an API key, register at [Behind The Name](https://www.behindthename.com/api/).

Without an API key, the app uses demo data for common names.

## Project Structure

```
aide-hello/
├── aide-frame/          # Git submodule (framework)
├── app/
│   ├── hello.py         # Main application
│   └── static/          # Static files (optional)
├── hello_config.json    # Configuration
└── README.md
```

## How it uses aide-frame

```python
# Path setup for submodule
AIDE_FRAME_PATH = os.path.join(PROJECT_DIR, 'aide-frame', 'python')
sys.path.insert(0, AIDE_FRAME_PATH)

# Import framework modules
from aide_frame import paths
from aide_frame.log import logger
from aide_frame.config import load_config
from aide_frame.web_request import fetch_json

# Initialize
paths.init(SCRIPT_DIR)
config = load_config('hello_config.json', defaults=DEFAULT_CONFIG)

# Use web_request for external API calls
data = fetch_json(f"https://api.example.com/lookup?name={name}")
```

## License

MIT
