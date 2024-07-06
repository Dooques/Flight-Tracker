import data_manager
import flight_search
import notification_manager

data_manager = data_manager.DataManager()
flight_search = flight_search.FlightSearch()
notification_manager = notification_manager.NotificationManager()

destination_data = data_manager.return_destinations()
club_members = data_manager.get_club_members()
# club_members = data_manager.load_json("club_members.json")
# destination_data = data_manager.load_json("destination_data.json")
flight_search.flight_search(data_manager.load_json("destination_data.json"), club_members)
notification_manager.send_email(data_manager.load_json("flight_info.json"), data_manager.load_json("club_members.json"))
