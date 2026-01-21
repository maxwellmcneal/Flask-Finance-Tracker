#!/bin/bash

# Flask Finance Tracker - LXC Deployment Script
# Run this script on your LXC container as root

set -e

echo "=========================================="
echo "Flask Finance Tracker Deployment Script"
echo "=========================================="

# Configuration
GIT_REPO="https://github.com/maxwellmcneal/Flask-Finance-Tracker.git"
GIT_BRANCH="main"
APP_DIR="/opt/flask-finance-tracker"
APP_USER="www-data"
DOMAIN="192.168.8.188"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

echo ""
echo "[1/8] Updating system packages..."
apt-get update
apt-get upgrade -y

echo ""
echo "[2/8] Installing required packages..."
apt-get install -y python3 python3-pip python3-venv nginx git

echo ""
echo "[3/8] Cloning repository from GitHub..."
if [ -d "$APP_DIR" ]; then
    echo "Application directory already exists. Removing old installation..."
    rm -rf $APP_DIR
fi

git clone --branch $GIT_BRANCH $GIT_REPO $APP_DIR
echo "Repository cloned successfully!"

echo ""
echo "[4/8] Creating data directory..."
mkdir -p $APP_DIR/data

echo ""
echo "[5/8] Setting up Python virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

echo ""
echo "[6/8] Installing Python dependencies..."
# Install gunicorn for production
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo ""
echo "[7/8] Setting up .env file..."
if [ ! -f "$APP_DIR/.env" ]; then
    echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > $APP_DIR/.env
    echo ".env file created with random SECRET_KEY"
else
    echo ".env file already exists, skipping..."
fi

echo ""
echo "[8/8] Setting permissions..."
chown -R $APP_USER:$APP_USER $APP_DIR
chmod -R 755 $APP_DIR
chmod 640 $APP_DIR/.env

echo ""
echo "[9/10] Installing systemd service..."
cp $APP_DIR/flask-finance-tracker.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable flask-finance-tracker
systemctl start flask-finance-tracker

echo ""
echo "[10/10] Configuring Nginx..."
cp $APP_DIR/nginx-config /etc/nginx/sites-available/flask-finance-tracker
ln -sf /etc/nginx/sites-available/flask-finance-tracker /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Flask Finance Tracker is now running!"
echo ""
echo "Access it at: http://$DOMAIN"
echo ""
echo "Useful commands:"
echo "  - Check app status: systemctl status flask-finance-tracker"
echo "  - View app logs: journalctl -u flask-finance-tracker -f"
echo "  - Restart app: systemctl restart flask-finance-tracker"
echo "  - Check Nginx status: systemctl status nginx"
echo "  - View Nginx logs: tail -f /var/log/nginx/error.log"
echo ""
echo "Next steps:"
echo "  1. Update DOMAIN in /etc/nginx/sites-available/flask-finance-tracker"
echo "  2. Configure your SECRET_KEY in $APP_DIR/.env if needed"
echo "  3. Set up SSL certificate (optional but recommended)"
echo ""
