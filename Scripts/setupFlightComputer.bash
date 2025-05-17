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

# Setup .bashrc file
echo "Setting up .bashrc..."

#Add comment to .bashrc
echo -e "\n# SUAV Aliases and Functions" >> "$HOME/.bashrc"

# Add alias to cd to ~/SUAV
echo "alias cdSuav='cd ~/SUAV'" >> "$HOME/.bashrc"

# Add alias to cd to ~/SUAV/2025Electronics
echo "alias cdElec='cd ~/SUAV/2025Electronics'" >> "$HOME/.bashrc"

# Add alias to run server.py
echo "alias runServer='python3 ~/SUAV/2025Electronics/server.py'" >> "$HOME/.bashrc"

# Add alias to run source venv
echo "alias sourceVenv='source ~/SUAV/venv/bin/activate'" >> "$HOME/.bashrc"

# Add bash function to run the mavproxy.py
echo "function runMavMod() {
    mavproxy_path=\"SUAV/venv/lib/python3.11/site-packages/MAVProxy/mavproxy.py\"
    if [ ! -f \"\$mavproxy_path\" ]; then
        echo \"Error: Module \$1 not found in MAVProxy modules directory.\"
        return 1
    fi
    python3 mavproxy.py --out=udp:127.0.0.1:5005\"
}" >> "$HOME/.bashrc"

echo -e "\nSetup complete!"
