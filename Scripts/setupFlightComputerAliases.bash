set -x
set -v 

#Add comment to .bashrc
echo "# SUAV Aliases and Functions" >> "$HOME/.bashrc"

# Add alias to cd to ~/SUAV
echo "alias cdSuav='cd ~/SUAV'" >> "$HOME/.bashrc"

# Add alias to cd to ~/SUAV/2025Electronics
echo "alias cdElec='cd ~/SUAV/2025Electronics'" >> "$HOME/.bashrc"

# Add alias to run server.py
echo "alias runServer='python3 ~/SUAV/2025Electronics/server.py'" >> "$HOME/.bashrc"

# Add alias to source venv
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

echo "Applying new aliases and functions..."
source "$HOME/.bashrc"

