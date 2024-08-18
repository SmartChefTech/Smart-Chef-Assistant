import connector
import crawler
import scraper

def main():
    countries = ["France", "China", "Spain", "Japan", "Italy", "Mexico"]
    
    for country in countries:
        print(f"Processing dishes from {country}...")
        dishes = crawler.crawl_wikipedia_dishes(country)
        
        for dish in dishes:
            print(f"Scraping recipe for {dish}...")
            recipe_data = scraper.scrape_recipe(dish)
            connector.insert_recipe_to_db(recipe_data)
            print(f"Recipe for {dish} has been added to the database.")
        
        print(f"Finished processing dishes from {country}.")
    
    print("All recipes have been added to the database.")

if __name__ == "__main__":
    main()
