#!/usr/bin/env bash

set -e

echo "========================================"
echo "Installing Python dependencies..."
echo "========================================"

pip install -r requirements.txt

echo "========================================"
echo "Installing Deno..."
echo "========================================"

curl -fsSL https://deno.land/install.sh | sh

echo "========================================"
echo "Checking Deno..."
echo "========================================"

export PATH="$HOME/.deno/bin:$PATH"

deno --version

echo "========================================"
echo "Build completed"
echo "========================================"
