import requests
import json

# Unsplash API
UNSPLASH_ACCESS_KEY = "nXB_3vDv6TCaj3coCQ7qEuitCR-ILA9g-5-9A_yfknE"  # Replace with your Unsplash Access Key
UNSPLASH_API_URL = "https://api.unsplash.com/photos/random"

# Number of image sets to generate
NUM_SETS = 10

# Function to fetch images from Unsplash API
def fetch_images(query, count):
    params = {
        "query": query,
        "count": count,
        "client_id": UNSPLASH_ACCESS_KEY,
    }
    response = requests.get(UNSPLASH_API_URL, params=params)
    return [img["urls"]["regular"] for img in response.json()]

# Generate image sets
image_sets = []
for _ in range(NUM_SETS):
    exterior_urls = fetch_images("house exterior", 1)
    interior_urls = fetch_images("house interior", 3)
    image_set = {
        "exterior": exterior_urls,
        "interior": interior_urls,
    }
    image_sets.append(image_set)

# Save image sets to a JSON file
with open("image_sets.json", "w") as f:
    json.dump(image_sets, f, indent=2)

print("Image sets saved to image_sets.json")