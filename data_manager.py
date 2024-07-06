import requests
import json
import os


class DataManager:
    def __init__(self):
        """API Data"""
        self.sheety_auth = os.environ.get('SHEETY_AUTH')
        self.sheety_endpoint = 'https://api.sheety.co/40b18875d50c2295c89a0e88376c5098/day39FlightDealFinder/'
        self.tequila_apikey = os.environ.get('TEQUILA_API_KEY')
        self.tequila_url = "http://api.tequila.kiwi.com/"
        """Response Data"""
        self.iata_data = []
        self.search_data = {}
        self.destination_data = {}
        """Imported Functions"""

    def return_destinations(self):
        headers = {
            "Authorization": self.sheety_auth,
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.sheety_endpoint}dealFinder", headers=headers)
        response.raise_for_status()
        destination_data = response.json()
        if destination_data["dealFinder"][0]["iataCode"] == "":
            self.get_iata(destination_data)
        return destination_data

    def get_iata(self, destinations):
        needed_key = 'city'
        destination_id = 0
        destinations_list = [list_item[needed_key] for list_item in destinations['dealFinder']]
        for city in destinations_list:
            headers = {
                "apikey": self.tequila_apikey
            }
            search_params = {
                "term": city,
                "location_types": "city"
            }
            response = requests.get(f"{self.tequila_url}locations/query", params=search_params, headers=headers)
            response_data = response.json()
            iata_code = response_data["locations"][0]["code"]
            self.send_iata_code(iata_code, destinations["dealFinder"][destination_id]["id"])
            destination_id += 1

    def send_iata_code(self, iata, city_id):
        iata_config = {
            "dealFinder":
                {
                    "iataCode": iata
                }
        }
        headers = {
            "Authorization": self.sheety_auth,
            "Content-Type": "application/json"
        }
        response = requests.put(
            f"{self.sheety_endpoint}/dealFinder/{city_id}",
            json=iata_config,
            headers=headers
        )

    def get_club_members(self):
        headers = {
            "Authorization": self.sheety_auth,
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.sheety_endpoint}flightClubMembers", headers=headers)
        return response.json()

    def dump_json(self, data, fp):
        with open(fp, 'w') as data_file:
            json.dump(data, data_file, indent=4)

    def load_json(self, fp):
        with open(fp, "r") as json_file:
            data = json.load(json_file)
        return data
