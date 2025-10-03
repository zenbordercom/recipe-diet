import json
import time
import os
import sys
import importlib.util

if importlib.util.find_spec("googlesearch") is None:
    print(
        "The 'googlesearch' package is required. Install it with 'pip install googlesearch-python'."
    )
    sys.exit(1)

from googlesearch import search

def update_cooking_links():
    # Get the absolute path to the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'recipes1219.json')
    
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the recipes table
    recipes = data.get('recipes', [])
    
    # Update each recipe
    for recipe in recipes:
        name = recipe.get('name', '')
        if name:
            # Create search query
            search_query = f"{name} 食谱 做法"
            
            try:
                # Get top 3 URLs
                urls = []
                for url in search(search_query, num_results=3):
                    urls.append(url)
                    time.sleep(2)  # Add delay to avoid hitting rate limits
                
                # Update cooking_link field
                recipe['cooking_link'] = ' | '.join(urls)
                print(f"Updated links for: {name}")
                
            except Exception as e:
                print(f"Error searching for {name}: {str(e)}")
                continue
            
            # Add a delay between recipes to avoid hitting rate limits
            time.sleep(5)
    
    # Save the updated data back to the JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Finished updating cooking links!")

if __name__ == '__main__':
    update_cooking_links()
