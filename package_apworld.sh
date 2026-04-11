#!/bin/bash
# Script to package the Metroid Dread apworld for Archipelago

# Ensure we are in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Clean up old apworld if it exists
if [ -f "metroid_dread.apworld" ]; then
    rm "metroid_dread.apworld"
fi

# Package the world
# We cd into the apworld directory so the zip contains the 'metroid_dread' folder
cd apworld
zip -r ../metroid_dread.apworld metroid_dread -x "*.DS_Store" "*__pycache__*" "*.pyc"

echo "Successfully created metroid_dread.apworld"
