import json


def load_posts(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_posts(file_path, posts):
    with open(file_path, 'w') as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)
