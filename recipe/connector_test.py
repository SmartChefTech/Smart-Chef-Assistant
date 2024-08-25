import unittest
import sqlite3
import connector

def insert_sample_data(conn: sqlite3.Connection) -> None:
    """
    Insert sample data into the database.

    Args:
        conn (sqlite3.Connection): The database connection.

    Raises:
        ValueError: If the connection is None.
    """
    if conn is None:
        raise ValueError("A database connection must be provided.")
    
    cursor = conn.cursor()

    # Insert a sample recipe
    cursor.execute("INSERT INTO Recipes (name, description, instructions) VALUES (?, ?, ?)",
                   ("Spaghetti Carbonara", "A classic Italian pasta dish", "1. Cook pasta. 2. Fry bacon. 3. Mix eggs and cheese. 4. Combine all ingredients."))
    recipe_id = cursor.lastrowid

    # Insert sample ingredients
    ingredients = [("Spaghetti",), ("Eggs",), ("Bacon",), ("Parmesan Cheese",)]
    cursor.executemany("INSERT OR IGNORE INTO Ingredients (name) VALUES (?)", ingredients)

    # Get ingredient IDs
    cursor.execute("SELECT id, name FROM Ingredients WHERE name IN (?, ?, ?, ?)", 
                   ("Spaghetti", "Eggs", "Bacon", "Parmesan Cheese"))
    ingredient_ids = {name: id for id, name in cursor.fetchall()}

    # Insert recipe ingredients
    recipe_ingredients = [
        (recipe_id, ingredient_ids["Spaghetti"], 400, "g"),
        (recipe_id, ingredient_ids["Eggs"], 4, "pieces"),
        (recipe_id, ingredient_ids["Bacon"], 200, "g"),
        (recipe_id, ingredient_ids["Parmesan Cheese"], 100, "g")
    ]
    cursor.executemany("INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit) VALUES (?, ?, ?, ?)", 
                       recipe_ingredients)

    conn.commit()

class TestConnector(unittest.TestCase):

    def setUp(self):
        # Set up test database in memory
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        connector.create_database(self.conn)
        # Ensure the connection is still open after create_database
        self.conn.commit()

    def tearDown(self):
        self.conn.commit()
        self.conn.close()

    def test_insert_sample_data(self):
        connector.insert_sample_data(self.conn)
        
        # Verify sample recipe was inserted
        self.cursor.execute("SELECT * FROM Recipes WHERE name=?", ("Spaghetti Carbonara",))
        recipe = self.cursor.fetchone()
        self.assertIsNotNone(recipe)
        
        # Verify sample ingredients were inserted
        ingredients = ["Spaghetti", "Eggs", "Bacon", "Parmesan Cheese"]
        for ingredient in ingredients:
            self.cursor.execute("SELECT * FROM Ingredients WHERE name=?", (ingredient,))
            self.assertIsNotNone(self.cursor.fetchone())

    def test_insert_recipe_to_db(self):
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)
        
        # Verify recipe was inserted
        self.cursor.execute("SELECT * FROM Recipes WHERE name=?", ("Test Recipe",))
        recipe = self.cursor.fetchone()
        self.assertIsNotNone(recipe)
        
        # Verify ingredient was inserted
        self.cursor.execute("SELECT * FROM Ingredients WHERE name=?", ("Test Ingredient",))
        ingredient = self.cursor.fetchone()
        self.assertIsNotNone(ingredient)
        
        # Verify recipe_ingredient was inserted
        self.cursor.execute("SELECT * FROM RecipeIngredients WHERE recipe_id=? AND ingredient_id=?", (recipe[0], ingredient[0]))
        recipe_ingredient = self.cursor.fetchone()
        self.assertIsNotNone(recipe_ingredient)

    def test_get_recipes(self):
        # Insert a test recipe
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)

        # Get recipes
        recipes = connector.get_recipes(self.conn)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0][1], "Test Recipe")

    def test_generate_ingredient_list(self):
        # Insert a test recipe
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)

        # Get the recipe ID
        self.cursor.execute("SELECT id FROM Recipes WHERE name=?", ("Test Recipe",))
        recipe_id = self.cursor.fetchone()[0]

        # Generate ingredient list
        ingredients = connector.generate_ingredient_list(self.conn, recipe_id)
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0], "1.0 piece Test Ingredient")

    def test_display_recipes(self):
        # Insert a test recipe
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)

        # Capture the output of display_recipes
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        connector.display_recipes(self.conn)
        sys.stdout = sys.__stdout__

        # Verify the output
        self.assertIn("Available Recipes:", captured_output.getvalue())
        self.assertIn("Test Recipe", captured_output.getvalue())

    def test_select_recipe(self):
        # Insert a test recipe
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)

        # Mock user input
        import builtins
        input_values = iter(["1"])
        builtins.input = lambda _: next(input_values)

        # Select recipe
        recipe_id = connector.select_recipe(self.conn)
        self.assertEqual(recipe_id, 1)

    def test_display_ingredient_list(self):
        # Insert a test recipe
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        connector.insert_recipe_to_db(self.conn, recipe_data)

        # Get the recipe ID
        self.cursor.execute("SELECT id FROM Recipes WHERE name=?", ("Test Recipe",))
        recipe_id = self.cursor.fetchone()[0]

        # Capture the output of display_ingredient_list
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        connector.display_ingredient_list(self.conn, recipe_id)
        sys.stdout = sys.__stdout__

        # Verify the output
        self.assertIn("Ingredient List:", captured_output.getvalue())
        self.assertIn("1.0 piece Test Ingredient", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()