import smtplib
import requests
from twilio.rest import Client
import data_manager
import os


class NotificationManager:
    def __init__(self):
        """Twilio"""
        self.twilio_sid = os.environ.get('TWILIO_SID')
        self.twilio_auth = os.environ.get('TWILIO_AUTH_TOKEN')
        """tinyurl"""
        self.tinyurl_endpoint = "http://api.tinyurl.com"
        self.tinyurl_auth = os.environ.get('TINYURL_AUTH')
        self.tinyurl_apikey = os.environ.get('TINYURL_API_KEY')
        self.tiny_url_links = []
        """Data Manager"""
        self.data_manager = data_manager.DataManager()
        """Emails"""
        self.MY_EMAIL = os.environ.get('MY_EMAIL')
        self.MY_PASSWORD = os.environ.get('EMAIL_PASS')

    def get_tinyurl(self):
        flight_data = self.data_manager.load_json("flight_info.json")
        for key in flight_data:
            headers = {
                "bearerAuth": self.tinyurl_auth
            }
            tinyurl_params = {
                "url": f"{flight_data[key]['deep_link']}",
                "domain": "tinyurl.com",
                "description": f"{key} flight URL",
                "api_token": self.tinyurl_apikey
            }
            tinyurl_response = requests.post(f"{self.tinyurl_endpoint}/create", json=tinyurl_params)
            tinyurl_data = tinyurl_response.json()
            self.tiny_url_links.append(tinyurl_data["data"]["tiny_url"])

    def send_notifications(self):
        flight_data = self.data_manager.load_json("flight_info.json")
        self.get_tinyurl()
        link_num = 0
        for key in flight_data:
            account_sid = self.twilio_sid
            auth_token = self.twilio_auth
            price = flight_data[key]["price"]
            city_from = flight_data[key]["cityFrom"]
            city_code_from = flight_data[key]["cityCodeFrom"]
            city_to = flight_data[key]["cityTo"]
            city_code_to = flight_data[key]["cityCodeTo"]
            date_from = flight_data[key]["local_departure"][:10]
            date_to = flight_data[key]["local_departure"][:10]

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=os.environ.get('MY_NUM'),
                from_=os.environ.get('TWILIO_NUM'),
                body=f"Low price alert! Only £{price} to fly from {city_from}-{city_code_from}"
                     f" to {city_to}-{city_code_to} from {date_from} to {date_to}. "
                     f"Click here to book: {self.tiny_url_links}"
            )
            link_num += 1
            print(message.status)

    def send_email(self, flight_data, members):
        self.get_tinyurl()
        print(f'tinyurl links: {self.tiny_url_links}')
        link_num = 0
        user_num = 0
        user_emails = members["flightClubMembers"]
        for user in user_emails:
            for key in flight_data:
                price = flight_data[key]["price"]
                city_from = flight_data[key]["cityFrom"]
                city_code_from = flight_data[key]["cityCodeFrom"]
                city_to = flight_data[key]["cityTo"]
                city_code_to = flight_data[key]["cityCodeTo"]
                date_from = flight_data[key]["local_departure"][:10]
                date_to = flight_data[key]["local_departure"][:10]
                email = user["email"]
                print(email)
                print(self.MY_EMAIL)
                message = f"""Subject: Low Price Alert!\n\n
                Only £{price} to fly from {city_from}-{city_code_from}
                to {city_to}-{city_code_to} from {date_from} to {date_to}.
                Click here to book: {self.tiny_url_links[link_num]}"""
                msg = message.encode('utf-8')
                with smtplib.SMTP('smtp.gmail.com', 587, timeout=120) as connection:
                    connection.starttls()
                    connection.login(self.MY_EMAIL, self.MY_PASSWORD)
                    connection.sendmail(
                        from_addr=self.MY_EMAIL,
                        to_addrs=email,
                        msg=msg
                        )
                print(f'link num: {link_num}')
                link_num += 1
            user_num += 1
