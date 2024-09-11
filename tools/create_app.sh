#!/bin/bash
# © 2024 Tekyonix. All rights reserved.
# This script is used to create a new application directory within the 'apps' directory.
# Usage: ./create_app.sh <app_name>
# Ensure that the 'apps' directory exists before running this script.

# check user input
if [ $# -ne 1 ]; then
    echo "Usage: ./create_app.sh <app_name>"
    exit 1
fi

# check if apps directory exists
if [ ! -d "apps" ]; then
    echo "Error: apps directory not found!"
    exit 1
fi

app_name=$1

# Check if app already exists
if [ -d "apps/$app_name" ]; then
    echo "Error: App $app_name already exists!"
    exit 1
fi

# create app directory
mkdir -p apps/$app_name/api/v1

# create app files
touch apps/$app_name/{__init__.py,admin.py,apps.py,models.py,tests.py}
touch apps/$app_name/api/__init__.py
touch apps/$app_name/api/v1/{__init__.py,serializers.py,tests.py,urls.py,views.py}

echo "App $app_name created successfully!"
