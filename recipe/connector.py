import sqlite3

def create_database():
    conn = sqlite3.connect('recipes.db')
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
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect('recipes.db')
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
    conn.close()

def insert_recipe_to_db(recipe_data):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    # Insert recipe
    cursor.execute('''
    INSERT INTO Recipes (name, description, instructions)
    VALUES (?, ?, ?)
    ''', (recipe_data['name'], recipe_data['description'], recipe_data['instructions']))
    recipe_id = cursor.lastrowid
    
    # Insert ingredients and recipe_ingredients
    for ingredient in recipe_data['ingredients']:
        # Insert or get ingredient
        cursor.execute('''
        INSERT OR IGNORE INTO Ingredients (name)
        VALUES (?)
        ''', (ingredient['name'],))
        cursor.execute('SELECT id FROM Ingredients WHERE name = ?', (ingredient['name'],))
        ingredient_id = cursor.fetchone()[0]
        
        # Insert recipe_ingredient
        cursor.execute('''
        INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit)
        VALUES (?, ?, ?, ?)
        ''', (recipe_id, ingredient_id, ingredient['quantity'], ingredient['unit']))
    
    conn.commit()
    conn.close()

def get_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def display_recipes():
    recipes = get_recipes()
    print("Available Recipes:")
    for id, name in recipes:
        print(f"{id}: {name}")

def select_recipe():
    display_recipes()
    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe you want to select: "))
            return recipe_id
        except ValueError:
            print("Please enter a valid number.")

def generate_ingredient_list(recipe_id):
    conn = sqlite3.connect('recipes.db')
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
    
    conn.close()
    
    # Format the ingredients
    ingredient_list = [
        f"{ingredient[1]} {ingredient[2]} {ingredient[0]}"
        for ingredient in ingredients
    ]
    
    return ingredient_list

def display_ingredient_list(recipe_id):
    ingredients = generate_ingredient_list(recipe_id)
    print("Ingredient List:")
    for ingredient in ingredients:
        print(f"- {ingredient}")

# Example usage:
# recipe_data = scrape_recipe("Coq au Vin")
# insert_recipe_to_db(recipe_data)

if __name__ == "__main__":
    create_database()
    insert_sample_data()
    insert_recipe_to_db({})
    print("Database created and sample data inserted.")
