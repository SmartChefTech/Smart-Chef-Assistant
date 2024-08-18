#!/bin/bash

# Check if Conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Please install Conda and try again."
    exit 1
fi

# Create the Conda environment
conda env create -f environment.yml

# Activate the environment
conda activate recipe-app

# Install additional dependencies
pip install requests beautifulsoup4

# Run the database setup script
python sqlite-database-setup.py

# Run the web crawler to populate the database
python recipe_crawler.py

# Run the unit tests
python -m unittest test_recipe_crawler.py

echo "Setup complete. You can now run the main application with: python main-recipe-app.py"
