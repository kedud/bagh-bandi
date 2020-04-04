import requests
import json

from src.app.user_interface import UserInterface


class NetworkUserInterface(UserInterface):

    def __init__(self):
        self.turn = "goats"
        self.url = "http://192.168.1.13:5000"
        self.goatPositions = []
        self.tigerPositions = []

    def play(self):
        self.player_type =  self.ask_user_what_he_wants_to_play()
        self.url =  self.ask_user_server_url()
        self.update_state()
        while True:
            self.ask_user_action()

    def ask_user_action(self):
        a = input("""[s]how [m]ove""")
        if a == "s":
            self.update_state()
            UserInterface.show(self.tigerPositions,
                               self.goatPositions,
                               self.turn)
        elif a == "m":
            column = input("Let's choose departure: Select a column: ")
            row = int(input("Select a row: "))

            departure = UserInterface.convert_user_input_to_position(row, column)

            column = input("Let's choose destination: Select column of destination:")
            row = int(input("Select row of destination:"))

            destination = UserInterface.convert_user_input_to_position(row, column)

            print(f"from {departure} to {destination}")

            self.send_move_request(departure, destination)

    def send_move_request(self, departure, destination):
        url = self.url + "/move/" + self.player_type + "/" + str(departure) + "/" + str(destination)
        print(f"Url : {url}")
        r = requests.get(url)
        print(r.text)

    def update_state(self):
        r = requests.get(self.url + "/state")
        ret = r.text
        data = json.loads(ret)
        self.turn = data["turn"]
        self.goatPositions = data["goat_positions"]
        self.tigerPositions = data["tigers_positions"]

    def ask_user_what_he_wants_to_play(self):
        while True:
            a = input("Do you want to play [G]oats ? or  [T]igers ?")
            if a in ["G", "g", "goats"]:
                return "goats"
            if a in ["T", "t", "tigers"]:
                return "tigers"

            else:
                print("Wrong entry, please type 't' or 'g'")

    def ask_user_server_url(self):
        url = input("Please enter server url: ").rstrip("/")
        if url == "":
            url = self.url
        print(f"Url \"{url}\"")
        return url
