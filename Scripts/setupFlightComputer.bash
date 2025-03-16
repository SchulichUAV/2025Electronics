#!/bin/bash
set -x
set -v 

SUAV_DIR="$HOME/SUAV"
REPO_URL="https://github.com/SchulichUAV/2025Electronics.git" 
VENV_NAME="venv"

# Create SUAV directory 
if [ ! -d "$SUAV_DIR" ]; then
    echo "Creating directory: $SUAV_DIR"
    mkdir -p $SUAV_DIR
else
    echo "Directory $SUAV_DIR already exists."
fi

# Navigate to SUAV
cd $SUAV_DIR || { echo "Failed to access SUAV"; exit 1; }

# Clone Electronics2025 
if [ ! -d "2025Electronics" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
else
    echo "Repository already exists. Skipping clone."
fi

# Setup Python virtual environment
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating Python virtual environment ($VENV_NAME)..."
    python3 -m venv --system-site-packages "$VENV_NAME"
    echo "$(ls)" 
else
    echo "Virtual environment ($VENV_NAME) already exists."
fi

#Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install Flask
pip install flask_cors
pip install picamera2
pip install pymavlink
pip install MAVProxy

echo -e "\nSetup complete!"