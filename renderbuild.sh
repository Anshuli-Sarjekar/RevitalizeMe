#!/bin/bash
#!/bin/bash

# Upgrade Python
sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update
sudo apt install python3.11=3.11.5*

# Upgrade pip and install requirements
# /opt/render/project/src/.venv/bin/python -m pip install --upgrade pip && /opt/render/project/src/.venv/bin/python -m pip install -r /opt/render/project/src/requirements.txt

echo "Updating pip..."
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
echo "Pip updated successfully!"

echo "Installing requirements..."
/opt/render/project/src/.venv/bin/python -m pip install -r /opt/render/project/src/requirements.txt
echo "Requirements installed successfully!"
