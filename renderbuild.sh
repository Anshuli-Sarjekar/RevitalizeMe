#!/bin/bash

echo "Updating pip..."
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
echo "Pip updated successfully!"

echo "Installing requirements..."
/opt/render/project/src/.venv/bin/python -m pip install -r /opt/render/project/src/requirements.txt
echo "Requirements installed successfully!"
