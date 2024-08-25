# Smart-Chef-Assistant

Welcome to the Smart-Chef-Assistant project! A world of smart Grocery & Cooking assistant! This app helps users purchase unfamiliar ingredients and cook unfamiliar dishes with ease.

## Features
0. Recommend dishes based on current weather, your mood, location, and time of day.
1. Generate ingredient lists with quantities based on chosen dishes.
2. Scan the kitchen to determine existing and missing ingredients.
3. Find nearby stores to buy missing ingredients, optimizing routes for efficiency.
4. Guide users within stores to find ingredients based on store layout.
5. Assist in selecting the best ingredients based on various criteria.
6. Arrange the order of ingredient preparation considering factors like oxidation, soaking, and marinating times.
7. Provide suggestions for ingredient preparation with video tutorials or detailed instructions.
8. Real-time cooking assistance with photo analysis every second to guide users on oil temperature, heat levels, and ingredient timing.

## Installation

Follow the [Setup Guide](docs/SetupGuide.md) to install and configure the project.

## Usage

Refer to the [User Guide](docs/UserGuide.md) for detailed instructions on how to use the app.

## Feature 1: Generate ingredient lists with quantities based on chosen dishes.

### Usage Example
Here's an example of how to get the national dishes from wikipedia:
```
(recipe-app) Smart-Chef-Assistant>python main-recipe-init.py   
```

Here's an example of how to use the Recipe Ingredient Generator:
```
(recipe-app) Smart-Chef-Assistant>python main-recipe-app.py   
INFO:__main__:Welcome to the Recipe Ingredient Generator!
2024-08-25 16:19:14,767 - INFO  - main-recipe-app - main - 32 - Welcome to the Recipe Ingredient Generator!
Available Recipes:
1: Spaghetti
2: Pizza
3: Croissant
...
Enter the ID of the recipe you want to select: 2
Ingredient List:
1.0 ball Pizza dough
0.5 cup Tomato sauce
1.0 cup Mozzarella cheese
as desired Toppings (optional)
1.0 tablespoon Olive oil
Would you like to select another recipe? (y/n): y
Enter the ID of the recipe you want to select: 3
Ingredient List:
4.0 cups all-purpose flour
1.0 cup unsalted butter
1.0 cup milk
2.25 teaspoons active dry yeast
0.25 cup granulated sugar
2.0 teaspoons salt
0.25 cup warm water
1.0 large egg
...
```

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.