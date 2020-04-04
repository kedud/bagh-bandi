import requests
import json

from src.app.user_interface import UserInterface


class NetworkUserInterface(UserInterface):

    def __init__(self):
        self.turn = "goats"
        self.url = "http://192.168.1.13:5000"
        self.goatPositions = []
        self.tigerPositions = []
        self.is_recapture_allowed = False
        self.game_type = ''
        self.player_type = ''

    def define_type_of_game(self):
        game_type = input("Do you want to play :\nA) user vs user\nB) user vs ai\n[A/B]? : ")
        if game_type.lower().strip() == 'a':
            self.game_type = 'uvu'
        elif game_type.lower().strip() == 'b':
            self.game_type = 'uva'

    def play(self):
        self.define_type_of_game()
        self.player_type = self.ask_user_what_he_wants_to_play()
        self.url = self.ask_user_server_url()
        if self.game_type == 'uva':
            self.send_agent_setup_request()
        self.update_state()
        while True:
            self.ask_user_action()

    def ask_user_action(self):
        ask = "[s]how [m]ove"
        if self.is_recapture_allowed:
            ask += " s[k]ip (give turn to goats)"
        a = input(ask)

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
        elif a == "k" and self.is_recapture_allowed:
            self.send_skip_turn_request()

    def send_skip_turn_request(self):
        url = f"{self.url}/skip/{self.player_type}"
        print(f"Url : {url}")
        r = requests.get(url)
        print(r.text)

    def send_move_request(self, departure, destination):
        url = self.url + "/move/" + self.player_type + "/" + str(departure) + "/" + str(destination)
        print(f"Url : {url}")
        r = requests.get(url)
        print(r.text)

    def send_agent_setup_request(self):
        if self.player_type == 'tigers':
            agent_type = 'goats'
        else:
            agent_type = 'tigers'
        url = f"{self.url}/setup_agent/{agent_type}"
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
        self.is_recapture_allowed = data["re_capture_allowed"]

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
