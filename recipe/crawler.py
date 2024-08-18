import requests
import BeautifulSoup


def crawl_wikipedia_dishes(country):
    url = f"https://en.wikipedia.org/wiki/List_of_national_dishes"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    dishes = []
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')[1:]  # Skip header row
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            country_name = cols[0].text.strip()
            if country.lower() in country_name.lower():
                dish_names = cols[1].text.strip().split(',')
                dishes.extend([dish.strip() for dish in dish_names])
    
    return dishes

# Example usage:
# french_dishes = crawl_wikipedia_dishes("France")
# print(french_dishes)
