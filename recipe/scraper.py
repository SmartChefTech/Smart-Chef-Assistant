def scrape_recipe(dish_name):
    # This is a mock function. In a real scenario, you would scrape an actual recipe website.
    # For demonstration purposes, we'll return mock data.
    
    mock_data = {
        "name": dish_name,
        "description": f"A delicious {dish_name} recipe.",
        "instructions": f"1. Prepare ingredients for {dish_name}. 2. Cook {dish_name}. 3. Serve and enjoy!",
        "ingredients": [
            {"name": "Ingredient 1", "quantity": 100, "unit": "g"},
            {"name": "Ingredient 2", "quantity": 2, "unit": "tbsp"},
            {"name": "Ingredient 3", "quantity": 1, "unit": "piece"}
        ]
    }
    
    return mock_data

# Example usage:
# recipe = scrape_recipe("Coq au Vin")
# print(recipe)
