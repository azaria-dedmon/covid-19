import os
import requests

def test_code(state, API_BASE_URL):

    key = os.environ.get('key')

    url = f'https://covid-19-testing.github.io/locations/{state.lower()}/complete.json'
    res = requests.get(url)
    testing_data = res.json()
    latsLngs = {}
    for obj in testing_data:
          if obj["physical_address"]:

            for o in obj["physical_address"]:
                    addy = o["address_1"]
                    city = o["city"]
                    phone = obj["phones"][0]["number"]

            location = f'{addy} {city}'
            location_coordinates = requests.get(API_BASE_URL,
                                params={'key': key, 'location': location}).json()

            lat = location_coordinates["results"][0]["locations"][0]["latLng"]["lat"]
            lng = location_coordinates["results"][0]["locations"][0]["latLng"]["lng"]
            latsLngs[location] = {'lat': lat, 'lng': lng, 'place': location, 'phone': phone}
    return latsLngs

    