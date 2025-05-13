# Overview of SUAV Bash Scripts

### updateElectronicsRepo.bash

**Purpose:** A Script to copy the 2025 Electronics repo to a flight computer via SCP.

**Usage**: `bash updateElectronicsRepo.bash <flight_computer_username@flight_computer_hostname>`

---

### setupFlightComputer.bash

**Purpose:** A script to clone the electronics repo, create a python3 virtual environment, add aliases to the .`~/.bashrc` and install necessary python dependencies. 

**Note**: if you run into SSL certificate errors when installing python dependencies - make sure the time is date and time is set correctly on the flight computer

**Usage**: `bash setupFlightComputer.bash` **(To be scped to flight computer and ran there)**

---

### setupFlightComputerAliases.bash
**Purpose:** A script to setup handy bash aliases inside of the flight computer's .`~/.bashrc` file. 

**Note**: `setupFlightComputer.bash` will setup the exact same aliases that this script does, this script exists if a user just wants bash aliases setup on the flight computer. 

**Usage**: `bash setupFlightComputerAliases.bash` **(To be scped to flight computer and ran there)**

**List of bash aliases**:

<*Simply type any of the following aliases into the terminal and they will perform their respective actions*>

- `cdSuav` -> Changes to `~/SUAV` directory
- `cdElec` -> Changes to `~/SUAV/2025Electronics` directory
- `runServer` -> Runs `server.py`
- `runMavMod` -> Runs `mavproxy.py`

---
### setupMavProxyModule.bash
**Purpose:** A script to setup a custom mavproxy module. 

**Note:** This script expects that a python3 virtual environment called `"venv"` is located under `~/SUAV/`.

**Usage**: `bash setupMavProxyModule.bash <path to custom mavproxy module>`

---
