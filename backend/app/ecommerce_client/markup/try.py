

import json
from ecommerce_client.models import Category  # Replace 'myapp' with the name of your Django app
# Load the JSON data from the file
with open('ecommerce_client/markup/categories.json', 'r') as file:
    categories_data = json.load(file)


# A dictionary to keep track of created categories by their id
categories_dict = {}
# Iterate over the JSON data and create Category objects
for category_data in categories_data:
    # Extract data
    category_id = category_data['id']
    name = category_data['name']
    emoji = category_data['emoji']
    parent_id = category_data['parent'] 
    # Handle parent category
    if parent_id == 0:
        parent_category = None
    else:
        parent_category_in_json = categories_dict.get(parent_id)
    
    # Create and save the Category object
    category = Category(id=category_id, name=name, emoji=emoji, parent=parent_category)
    category.save()  
    # Store the created category in the dictionary
    categories_dict[category_id] = category


print("Categories imported successfully!")
