import logging
import sys
import sqlite3
from recipe import connector
from recipe import searcher
from llm import openai

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
        logger.info("Processing dishes from Wikipedia...")
        try:
            dishes = searcher.fetch_wikipedia_dishes(openai.request)
        except Exception as e:
            logger.error(f"An error occurred while fetching dishes: {e}")
            return
        
        for dish in dishes:
            logger.info(f"Scraping recipe for {dish}...")
            try:
                recipe_data = searcher.fetch_recipe(dish, openai.request)
            except Exception as e:
                logger.error(f"An error occurred while fetching recipe for {dish}: {e}")
                continue
            
            try:
                connector.insert_recipe_to_db(conn, recipe_data)
            except Exception as e:
                logger.error(f"An error occurred while inserting recipe for {dish} to the database: {e}")
                continue
            
            logger.info(f"Recipe for {dish} has been added to the database.")
        
        logger.info("All recipes have been added to the database.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()