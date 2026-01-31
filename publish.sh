#!/bin/bash
# Whatnotica Publish Script
# -------------------------
# This script builds the site and deploys it.
# 
# Usage: Double-click this file (or run ./publish.sh in terminal)

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Whatnotica Publisher"
echo "========================================"
echo ""

# Check if zola is installed
if ! command -v zola &> /dev/null; then
    echo "Error: Zola is not installed."
    echo "Install it with: snap install zola"
    echo "Or from: https://www.getzola.org/documentation/getting-started/installation/"
    exit 1
fi

# Build the site
echo "Building site..."
zola build

echo ""
echo "Build complete! Output in 'public/' directory."
echo ""

# If using git for deployment, uncomment these lines:
# echo "Deploying to GitHub..."
# git add -A
# git commit -m "Update site $(date '+%Y-%m-%d %H:%M')"
# git push

echo "Done!"
echo ""
echo "To preview locally: zola serve"
echo ""
