import unittest
from unittest.mock import patch, Mock
import searcher
import json

class Testsearcher(unittest.TestCase):

    @patch('searcher.requests.get')
    def test_fetch_wikipedia_dishes(self, mock_get):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.content = '''
        <html>
        <body>
            <table class="wikitable">
                <tr>
                    <th>Country</th>
                    <th>Dish</th>
                </tr>
                <tr>
                    <td>France</td>
                    <td>Baguette, Croissant</td>
                </tr>
                <tr>
                    <td>Italy</td>
                    <td>Pizza, Pasta</td>
                </tr>
            </table>
        </body>
        </html>
        '''
        mock_get.return_value = mock_response

        # Mock the response from llm.request
        mock_llm_request = Mock()
        mock_llm_request.return_value = json.dumps([
            {
                'dish_name': 'Baguette',
                'nation': 'France'
            },
            {
                'dish_name': 'Croissant',
                'nation': 'France'
            }
        ])

        # Call the function
        dishes = searcher.fetch_wikipedia_dishes(mock_llm_request)

        # Assert the results
        dish_names = [dish['dish_name'] for dish in dishes]
        self.assertIn("Baguette", dish_names)
        self.assertIn("Croissant", dish_names)
        self.assertNotIn("Pizza", dish_names)

    def test_fetch_recipe(self):
        # Mock the response from llm.request
        mock_llm_request = Mock()
        mock_llm_request.return_value = json.dumps({
            'dish_name': 'Baguette',
            'description': 'A delicious French bread',
            'instructions': 'Instructions for making Baguette',
            'ingredients': [
                {
                    "ingredient_name": "Flour",
                    "quantity": "500",
                    "unit": "g"
                }
            ]
        })

        # Call the function
        recipe = searcher.fetch_recipe("Baguette", mock_llm_request)

        # Assert the results
        self.assertEqual(recipe['dish_name'], "Baguette")
        self.assertIn("delicious French bread", recipe['description'])
        self.assertIn("Instructions for making Baguette", recipe['instructions'])
        self.assertEqual(recipe['ingredients'][0]['ingredient_name'], "Flour")

if __name__ == '__main__':
    unittest.main()