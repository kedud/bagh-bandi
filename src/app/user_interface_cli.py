from src.app.user_interface import UserInterface
from src.domain.engine import Engine


class UserInterfaceCli(UserInterface):

    def __init__(self):
        self.engine = Engine()

    def play(self):
        self.play_user_vs_user()

    def play_user_vs_user(self):
        while True:
            self.ask_user_action()

    def play_user_vs_ai(self):
        pass

    def ask_user_action(self):
        a = input("""
                [s]how [m]move
                """)
        if a == "s":
            UserInterface.show(self.engine.board.tigerPositions,
                               self.engine.board.goatsPositions,
                               self.engine.board.turn)
        elif a == "m":
            column = input("Let's choose departure: Select a column: ")
            row = int(input("Select a row: "))

            departure = UserInterface.convert_user_input_to_position(row, column)

            column = input("Let's choose destination: Select column of destination:")
            row = int(input("Select row of destination:"))

            destination = self.convert_user_input_to_position(row, column)

            print(f"from {departure} to {destination}")

            if self.engine.is_valid_move(departure, destination, self.engine.board):
                self.engine.board = self.engine.move(departure, destination, self.engine.board)
            else:
                print(f"/!\\ Invalid move : {departure} to {destination}")
                self.ask_user_action()



