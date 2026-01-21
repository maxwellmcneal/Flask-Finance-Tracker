#!/bin/bash

# Flask Finance Tracker - Update Script
# Run this script on your LXC container as root to update the app

set -e

echo "=========================================="
echo "Flask Finance Tracker Update Script"
echo "=========================================="

APP_DIR="/opt/flask-finance-tracker"
GIT_BRANCH="main"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "ERROR: Application directory not found at $APP_DIR"
    echo "Please run the initial deployment script first (deploy.sh)"
    exit 1
fi

echo ""
echo "[1/5] Stopping the application..."
systemctl stop flask-finance-tracker

echo ""
echo "[2/5] Pulling latest changes from GitHub..."
cd $APP_DIR
git fetch origin
git reset --hard origin/$GIT_BRANCH
echo "Latest changes pulled successfully!"

echo ""
echo "[3/5] Updating Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
deactivate

echo ""
echo "[4/5] Setting proper permissions..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR
if [ -f "$APP_DIR/.env" ]; then
    chmod 640 $APP_DIR/.env
fi

echo ""
echo "[5/5] Starting the application..."
systemctl start flask-finance-tracker

echo ""
echo "=========================================="
echo "Update Complete!"
echo "=========================================="
echo ""
echo "Application has been updated and restarted."
echo ""
echo "Check status with: systemctl status flask-finance-tracker"
echo "View logs with: journalctl -u flask-finance-tracker -f"
echo ""
