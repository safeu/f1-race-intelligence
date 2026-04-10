import requests

def get_driver_photo(driver_name):
    try:
        headers = {
            "User-Agent": "F1RaceIntelligence/1.0 (portfolio project; educational use)"
        }

        search_url = "https://en.wikipedia.org/w/api.php"
        
        
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{driver_name} racing driver",
            "format": "json",
            "srlimit": 1
        }
        search_response = requests.get(search_url, params=search_params, headers=headers)
        search_data = search_response.json()

        if not search_data["query"]["search"]:
            return None

        page_title = search_data["query"]["search"][0]["title"]

        
        image_params = {
            "action": "query",
            "titles": page_title,
            "prop": "pageimages",
            "format": "json",
            "pithumbsize": 300
        }
        image_response = requests.get(search_url, params=image_params, headers=headers)
        image_data = image_response.json()

        pages = image_data["query"]["pages"]
        page = next(iter(pages.values()))

        if "thumbnail" in page:
            return page["thumbnail"]["source"]
        return None

    except Exception as e:
        print(f"Error fetching photo for {driver_name}: {e}")
        return None