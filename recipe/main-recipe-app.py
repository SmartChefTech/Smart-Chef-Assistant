import connector

def main():
    print("Welcome to the Recipe Ingredient Generator!")
    while True:
        recipe_id = connector.select_recipe()
        connector.display_ingredient_list(recipe_id)
        
        again = input("Would you like to select another recipe? (y/n): ")
        if again.lower() != 'y':
            break
    
    print("Thank you for using the Recipe Ingredient Generator!")

if __name__ == "__main__":
    main()
