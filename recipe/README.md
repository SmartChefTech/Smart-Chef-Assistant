# Recipe Ingredient Generator and Crawler

## Overview

This project includes a Recipe Ingredient Generator and a web crawler to find popular dishes from various countries. It uses a SQLite database to store recipe and ingredient information, providing a simple and efficient way to manage and retrieve recipe data.

## Features

- Browse available recipes
- Select a recipe and view its ingredient list
- Web crawler to find popular dishes from different countries
- Scrape recipe details (mock implementation)
- Store recipe data in SQLite database
- Unit tests for main functionalities

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), which will be used to manage the project's dependencies.

## Installation

To install the Recipe Ingredient Generator and Crawler, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/recipe-ingredient-generator.git
   cd recipe-ingredient-generator
   ```

2. Run the setup script:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```

   This script will:
   - Create a Conda environment named `recipe-app`
   - Install all necessary dependencies
   - Set up the SQLite database with sample data

## Usage

To use the Recipe Ingredient Generator and Crawler:

1. Activate the Conda environment:
   ```
   conda activate recipe-app
   ```

2. Run the main application:
   ```
   python main-recipe-app.py
   ```

3. To run the web crawler and populate the database:
   ```
   python recipe_crawler.py
   ```

4. To run the unit tests:
   ```
   python -m unittest test_recipe_crawler.py
   ```

## Project Structure

- `environment.yml`: Conda environment specification
- `setup.sh`: Setup script for creating the Conda environment and initializing the database
- `sqlite-database-setup.py`: Script to create and populate the SQLite database
- `main-recipe-app.py`: Main application script for the Recipe Ingredient Generator
- `recipe_crawler.py`: Web crawler and recipe scraper script
- `test_recipe_crawler.py`: Unit tests for the crawler and database functions
- `recipes.db`: SQLite database file (created after running the setup)

## Contributing

Contributions to the Recipe Ingredient Generator and Crawler are welcome. Please feel free to submit a Pull Request.

## License

This project uses the following license: [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you want to contact me, you can reach me at `your_email@example.com`.

## Acknowledgements

- [SQLite](https://www.sqlite.org/index.html) for the database engine
- [requests](https://docs.python-requests.org/en/master/) for HTTP requests
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for HTML parsing
- [tabulate](https://pypi.org/project/tabulate/) for formatting console output
