#!/bin/bash

# Check if Conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Conda and try again."
    exit 1
fi

# Check if the environment already exists
if conda env list | grep -q "recipe-app"; then
    echo "Updating existing recipe-app environment..."
    conda env update -f conda-environment.yml
else
    echo "Creating new recipe-app environment..."
    conda env create -f conda-environment.yml
fi

# Activate the environment
conda activate recipe-app

# Run the database setup script
python sqlite-database-setup.py

# Run the web crawler to populate the database
python crawler.py

# Run the unit tests
python -m unittest connector_test.py
python -m unittest searcher_test.py

echo "Setup complete. You can now run the main application with: python main-recipe-app.py"
