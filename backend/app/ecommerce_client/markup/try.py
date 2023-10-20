import json


def find_base_categories(categories):
    base_categories = []
    category_ids_with_children = set()

    # Create a set of category IDs that have children
    for category in categories:
        category_ids_with_children.update(
            child["parent"] for child in category["children"]
        )

    # Find categories with no children
    for category in categories:
        if category["id"] not in category_ids_with_children:
            base_categories.append(category)

    return base_categories


# Usage example:
with open("categories.json", "r") as j:
    flat_categories = json.load(j)

base_categories = find_base_categories(flat_categories)

print(base_categories)
