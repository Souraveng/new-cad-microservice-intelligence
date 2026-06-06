#!/bin/bash
set -e

# Detect directory path and active user dynamically
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
USER=$(whoami)

echo "=================================================="
echo " Installing Aegis Intelligence Gateway Service     "
echo "=================================================="
echo "Target Directory: $DIR"
echo "Active User:      $USER"

# Resolve python interpreter path (checking/creating local venv)
PYTHON_PATH="$DIR/venv/bin/python"
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Creating python virtual environment (venv) at $DIR/venv..."
    python3 -m venv "$DIR/venv" || { echo "Failed to create venv. Make sure python3-venv is installed."; exit 1; }
fi

echo "Installing/verifying python microservice dependencies..."
"$DIR/venv/bin/pip" install --upgrade pip
"$DIR/venv/bin/pip" install fastapi uvicorn pydantic python-multipart httpx

echo "Creating systemd unit: aegis-intelligence.service"

cat <<EOF | sudo tee /etc/systemd/system/aegis-intelligence.service > /dev/null
[Unit]
Description=Aegis Intelligence Gateway Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$DIR
ExecStart=$PYTHON_PATH main.py
Restart=always
RestartSec=5
Environment=PORT=8080

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service to run on boot/startup
sudo systemctl enable aegis-intelligence.service

# Start the service immediately
sudo systemctl restart aegis-intelligence.service

echo "=================================================="
echo "  Installation Complete!                         "
echo "  The service will start automatically on boot.  "
echo "  Port: 8080                                      "
echo "=================================================="
