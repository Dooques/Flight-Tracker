import requests
from flight_data import FlightData
from notification_manager import NotificationManager
import os


class FlightSearch:
    def __init__(self):
        """API Data"""
        self.tequila_apikey = os.environ.get('TEQUILA_API_KEY')
        self.tequila_url = "http://api.tequila.kiwi.com/v2"
        self.iata_data = []
        """Imports"""
        self.flight_data = FlightData()
        self.notification_manager = NotificationManager()

    def flight_search(self, destinations, members):
        flights_dict = {}
        for destination in destinations["dealFinder"]:
            city_code = destination["iataCode"]
            print(f'Searching for flights: {city_code}\n')
            headers = {
                "apikey": self.tequila_apikey
            }
            search_params = {
                "fly_from": self.flight_data.from_iata,
                "fly_to": city_code,
                "date_from": self.flight_data.date_from,
                "date_to": self.flight_data.date_to,
                "return_from": self.flight_data.return_from,
                "return_to": self.flight_data.return_to,
                "nights_in_dst_from": self.flight_data.nights_in_dst_from,
                "nights_in_dst_to": self.flight_data.nights_in_dst_to,
                "curr": self.flight_data.currency,
                "price_to": destination["lowestPrice"]
            }
            response = requests.get(f"{self.tequila_url}/search", params=search_params, headers=headers)
            flight_info = response.json()
            print(f'flight found: {flight_info}\n')
            if flight_info["data"]:
                flights_dict[city_code] = flight_info["data"][0]
        if len(flights_dict) > 0:
            self.notification_manager.send_email(flights_dict, members)
