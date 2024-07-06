from datetime import datetime
import os


class FlightData:
    def __init__(self):
        self.tequila_apikey = os.environ.get('TEQUILA_API_KEY')
        self.tequila_url = "http://api.tequila.kiwi.com/"
        self.location_search_url = "https://api.tequila.kiwi.com/locations/query"
        """Time Data"""
        self.today = datetime.now()
        self.date_from = self.today.strftime("%d/%m/%Y")
        self.date_to = f"0{self.today.day}/0{self.today.month}/{self.today.year + 1}"
        self.return_from = f"{self.today.day + 7}/{self.today.month}/{self.today.year}"
        self.return_to = f"{self.today.day + 7}/{self.today.month}/{self.today.year + 1}"
        """Data Manager"""
        # if len(self.data_manager.destination_data) == 0:
        #     self.destination_data = self.data_manager.get_destinations()
        #     self.destination_data = self.data_manager.load_json("destination_data.json")
        # else:
        #     self.destination_data = self.data_manager.load_json("destination_data.json")
        """Trip Data"""
        self.from_iata = "LON"
        self.nights_in_dst_from = "2"
        self.nights_in_dst_to = "7"
        """Currency"""
        self.currency = "GBP"
