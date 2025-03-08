# Check if flight computer username and hostname is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <Flight Computer Username and Hostname>"
    exit 1
fi

FLIGHT_COMPUTER_USERNAME_AND_HOST="$1"
SUAV_DIR="~/SUAV"
REPO_URL="https://github.com/SchulichUAV/2025Electronics.git" 
VENV_NAME="venv"

# Create temporary SUAV directory 
if [ ! -d "$SUAV_DIR" ]; then
    echo "Creating directory: $SUAV_DIR"
    mkdir -p $SUAV_DIR
else
    echo "Directory $SUAV_DIR already exists."
fi

# Navigate to SUAV
cd $SUAV_DIR || { echo "Failed to access SUAV"; exit 1; }
echo "Current directory: $(pwd)"

# Clone the temp Electronics2025 
if [ ! -d "Electronics2025" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
else
    echo "Repository already exists. Skipping clone."
fi

cd "2025Electronics" || { echo "Failed to access 2025Electronics directory"; exit 1; }

# Setup Python virtual environment
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating Python virtual environment ($VENV_NAME)..."
    python3 -m venv --system-site-packages "$VENV_NAME"
    echo "$(ls)" 
else
    echo "Virtual environment ($VENV_NAME) already exists."
fi

Activate virtual environment
echo "Activating virtual environment..."
if [ -f "$VENV_NAME/scripts/activate" ]; then
    # Windows (WSL or Git Bash)
    echo "Activating virtual environment from Scripts/activate..."
    source "$VENV_NAME/scripts/activate"
elif [ -f "$VENV_NAME/bin/activate" ]; then
    # Linux/macOS
    echo "Activating virtual environment from bin/activate..."
    source "$VENV_NAME/bin/activate"
else
    echo "Error: Virtual environment activation script not found!"
    exit 1
fi
# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# cd ../../

# Move setup SUAV directory to flight computer
# scp -r SUAV $FLIGHT_COMPUTER_USERNAME_AND_HOST:$SUAV_DIR

# Cleanup 
# rm -rf SUAV

echo "\nSetup complete!"
