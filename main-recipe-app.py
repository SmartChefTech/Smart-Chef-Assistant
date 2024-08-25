import logging
import sys
import sqlite3
from recipe import connector

_TABLE_NAME = 'recipes.db'

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s  - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
    handler.setFormatter(formatter)
    
    root_logger.addHandler(handler)

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create a database connection
    conn = sqlite3.connect(_TABLE_NAME)
    try:
        connector.create_database(conn)
    except Exception as e:
        logger.error(f"An error occurred while creating the database: {e}")
        return
    
    try:
        logger.info("Welcome to the Recipe Ingredient Generator!")
        while True:
            try:
                recipe_id = connector.select_recipe(conn)
            except ValueError as e:
                logger.error(f"Error selecting recipe: {e}")
                continue
            
            try:
                connector.display_ingredient_list(conn, recipe_id)
            except Exception as e:
                logger.error(f"Error displaying ingredient list: {e}")
                continue
            
            again = input("Would you like to select another recipe? (y/n): ")
            if again.lower() != 'y':
                break
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        conn.close()

    logger.info("Thank you for using the Recipe Ingredient Generator!")

if __name__ == "__main__":
    main()