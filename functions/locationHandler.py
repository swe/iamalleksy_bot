import json
import requests

def getlocationdata(lat, lon):

    api_url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={openCageAPI}"

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            json_data = response.json()
            results = json_data.get("results", [])

            geodata = None
            for item in results:
                components = item.get("components", {})
                location_types = ["hamlet", "village", "town", "city"]
                for location_type in location_types:
                    if location_type in components:
                        geodata = [components[location_type], components["country"], components["continent"]]
                        break

            if geodata:
                print(geodata)
            else:
                print("Location not found.")
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")

    return(geodata)
