import json
import requests
import logging
from typing import List, Dict, Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_wikipedia_dishes(llm_retrieve: Callable[[str, str], str]) -> List[Dict]:
    try:
        web_response = requests.get("https://en.wikipedia.org/wiki/List_of_national_dishes")
        web_response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching Wikipedia page: {e}")
        return []
    
    dishes_raw = web_response.text
    prompt = """
    Convert the dishes to JSON format:

    There are over hundreds dishes.
    Try to return as many dishes as possible.

    Json format:
    ```json
    {
        'dishes': [
            {
                'dish_name': ...,
                'nation': ...,
            },
            ...
        ]
    }
    ```
    """
    
    try:
        json_response = llm_retrieve(prompt, dishes_raw)
        parsed_json = json.loads(json_response)
        dishes = parsed_json.get('dishes', [])  # Extract the 'dishes' list from the response
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error processing LLM response: {e}")
        return []
    
    logger.info(f"Successfully fetched {len(dishes)} dishes from Wikipedia")
    return dishes

def fetch_recipe(dish_name: str, llm_request: Callable[[str], str]) -> Dict:
    prompt = f"""
    Fetch the recipe for the dish: {dish_name}

    Json format:
    ```json
    {{
        'dish_name': ...,
        'description': ...,
        'instructions': ...,
        'ingredients': [
            {{
                "ingredient_name": ...,
                "quantity": ...,
                "unit": ...
            }},
            ...
        ]
    }}
    ```
    """
    
    try:
        json_response = llm_request(prompt)
        recipe = json.loads(json_response)
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error fetching or parsing recipe for {dish_name}: {e}")
        return {}
    
    logger.info(f"Successfully fetched recipe for {dish_name}")
    return recipe

# Example usage:
# dishes = fetch_wikipedia_dishes(llm_request)
# print(dishes)
# recipe = fetch_recipe("Baguette", llm_request)
# print(recipe)