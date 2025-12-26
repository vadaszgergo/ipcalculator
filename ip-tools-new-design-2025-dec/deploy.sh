#!/bin/bash

# Simple deployment script for VPS/Server
# Run this script on your server after uploading the files

echo "Setting up IP Tools Suite deployment..."

# Create application directory
sudo mkdir -p /opt/ip-tools-suite
sudo chown $USER:$USER /opt/ip-tools-suite

# Copy files (run this from your project directory)
cp -r . /opt/ip-tools-suite/

cd /opt/ip-tools-suite

# Install Python 3.11 if not present
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
fi

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/ip-tools.service > /dev/null <<EOF
[Unit]
Description=IP Tools Suite
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/opt/ip-tools-suite
Environment=PATH=/opt/ip-tools-suite/venv/bin
ExecStart=/opt/ip-tools-suite/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ip-tools
sudo systemctl start ip-tools

echo "Deployment complete! Service is running on port 5000"
echo "Check status with: sudo systemctl status ip-tools"
echo "View logs with: sudo journalctl -u ip-tools -f"