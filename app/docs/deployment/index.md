# Deployment

Installation and service configuration.

## Quick Start

```bash
# Clone and run
git clone https://github.com/...
cd project
python3 app/main.py
```

## Service Installation

Create systemd service file at `/etc/systemd/system/myapp.service`:

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/project
ExecStart=/usr/bin/python3 app/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable myapp
sudo systemctl start myapp
```
