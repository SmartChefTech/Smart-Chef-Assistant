import unittest
from unittest.mock import patch, MagicMock
from recipe_crawler import crawl_wikipedia_dishes, scrape_recipe, insert_recipe_to_db

class TestRecipeCrawler(unittest.TestCase):

    def setUp(self):
        # Set up test database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        # Create tables (reuse your table creation code here)
        # ...

    def tearDown(self):
        self.conn.close()

    @patch('recipe_crawler.requests.get')
    def test_crawl_wikipedia_dishes(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '''
        <table class="wikitable">
        <tr><th>Country</th><th>Dish</th></tr>
        <tr><td>France</td><td>Ratatouille, Coq au Vin</td></tr>
        </table>
        '''
        mock_get.return_value = mock_response

        dishes = crawl_wikipedia_dishes("France")
        self.assertEqual(dishes, ['Ratatouille', 'Coq au Vin'])

    def test_scrape_recipe(self):
        recipe = scrape_recipe("Test Dish")
        self.assertEqual(recipe['name'], "Test Dish")
        self.assertTrue('description' in recipe)
        self.assertTrue('instructions' in recipe)
        self.assertTrue('ingredients' in recipe)

    def test_insert_recipe_to_db(self):
        recipe_data = {
            "name": "Test Recipe",
            "description": "A test recipe",
            "instructions": "Test instructions",
            "ingredients": [
                {"name": "Test Ingredient", "quantity": 1, "unit": "piece"}
            ]
        }
        insert_recipe_to_db(recipe_data)
        
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

if __name__ == '__main__':
    unittest.main()
