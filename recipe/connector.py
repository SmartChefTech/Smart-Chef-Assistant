import logging
import sqlite3
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database(conn: sqlite3.Connection) -> None:
    """
    Create the database tables if they do not exist.

    Args:
        conn (sqlite3.Connection): The database connection.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    cursor = conn.cursor()

    # Create Recipes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        instructions TEXT
    )
    ''')

    # Create Ingredients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    # Create RecipeIngredients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RecipeIngredients (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        quantity REAL,
        unit TEXT,
        PRIMARY KEY (recipe_id, ingredient_id),
        FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
    )
    ''')

    conn.commit()

def insert_recipe_to_db(conn: sqlite3.Connection, recipe_data: Dict[str, Any]) -> None:
    """
    Insert a new recipe into the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        recipe_data (Dict[str, Any]): The recipe data to insert.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    cursor = conn.cursor()

    try:
        # Insert recipe
        cursor.execute('''
        INSERT INTO Recipes (name, description, instructions)
        VALUES (?, ?, ?)
        ''', (recipe_data['dish_name'], recipe_data.get('description', ''), recipe_data.get('instructions', '')))
        recipe_id = cursor.lastrowid
        
        # Insert ingredients and recipe_ingredients
        for ingredient in recipe_data['ingredients']:
            # Insert or get ingredient
            cursor.execute('''
            INSERT OR IGNORE INTO Ingredients (name)
            VALUES (?)
            ''', (ingredient['ingredient_name'],))
            cursor.execute('SELECT id FROM Ingredients WHERE name = ?', (ingredient['ingredient_name'],))
            ingredient_id = cursor.fetchone()[0]
            
            # Insert recipe_ingredient
            cursor.execute('''
            INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit)
            VALUES (?, ?, ?, ?)
            ''', (recipe_id, ingredient_id, ingredient['quantity'], ingredient['unit']))
        
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred: {e}")
        conn.rollback()
    except KeyError as e:
        logger.error(f"Missing key in recipe data: {e}")
        conn.rollback()

def get_recipes(conn: sqlite3.Connection) -> List[tuple]:
    """
    Retrieve all recipes from the database.

    Args:
        conn (sqlite3.Connection): The database connection.

    Returns:
        List[tuple]: A list of recipes with their IDs and names.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    return recipes

def display_recipes(conn: sqlite3.Connection) -> None:
    """
    Display all recipes in the database.

    Args:
        conn (sqlite3.Connection): The database connection.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    recipes = get_recipes(conn)
    print("Available Recipes:")
    for id, name in recipes:
        print(f"{id}: {name}")

def select_recipe(conn: sqlite3.Connection) -> int:
    """
    Prompt the user to select a recipe by ID.

    Args:
        conn (sqlite3.Connection): The database connection.

    Returns:
        int: The selected recipe ID.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    display_recipes(conn)
    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe you want to select: "))
            return recipe_id
        except ValueError:
            print("Please enter a valid number.")

def generate_ingredient_list(conn: sqlite3.Connection, recipe_id: int) -> List[str]:
    """
    Generate a list of ingredients for a specific recipe.

    Args:
        conn (sqlite3.Connection): The database connection.
        recipe_id (int): The ID of the recipe.

    Returns:
        List[str]: A list of formatted ingredient strings.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    cursor = conn.cursor()
    
    # Query to get ingredients for a specific recipe
    query = """
    SELECT i.name, ri.quantity, ri.unit
    FROM RecipeIngredients ri
    JOIN Ingredients i ON ri.ingredient_id = i.id
    WHERE ri.recipe_id = ?
    """
    
    cursor.execute(query, (recipe_id,))
    ingredients = cursor.fetchall()
    
    # Format the ingredients
    ingredient_list = [
        f"{ingredient[1]} {ingredient[2]} {ingredient[0]}"
        for ingredient in ingredients
    ]
    
    return ingredient_list

def display_ingredient_list(conn: sqlite3.Connection, recipe_id: int) -> None:
    """
    Display the ingredient list for a specific recipe.

    Args:
        conn (sqlite3.Connection): The database connection.
        recipe_id (int): The ID of the recipe.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    ingredients = generate_ingredient_list(conn, recipe_id)
    print("Ingredient List:")
    for ingredient in ingredients:
        print(f"- {ingredient}")

# Example usage:
# conn = sqlite3.connect('recipes.db')
# recipe_data = scrape_recipe("Coq au Vin")
# insert_recipe_to_db(conn, recipe_data)
# conn.close()