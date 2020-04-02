from src.domain.engine import Engine, Action


class UserInterface:

    def __init__(self):
        self.engine = Engine()


    def play_user_vs_user(self):
        while True:
            self.ask_user_action()

    def play_user_vs_ai(self):
        pass


    def show(self):
        board = """
          A   B   C   D   E
        1 %s---%s---%s---%s---%s
          | \\ | / | \\ | / |
        2 %s---%s---%s---%s---%s
          | / | \\ | / | \\ |
        3 %s---%s---%s---%s---%s
          | \\ | / | \\ | / |
        4 %s---%s---%s---%s---%s
          | / | \\ | / | \\ |
        5 %s---%s---%s---%s---%s
"""

        t = ['o'] * 25

        for i in self.engine.board.tigerPositions:
            t[i] = "T"

        for i in self.engine.board.goatsPositions:
            if t[i] == "G":
                t[i] = 2
            elif t[i] == 'o':
                t[i] = "G"
            elif isinstance(t[i], int):
                t[i] += 1

        for i in range(len(t)):
            if t[i] == 'G' or t[i] in (2,3,4,5):
                t[i] = "\033[32m"+ str(t[i]) + "\033[0m"
            if t[i] == 'T':
                t[i] = "\033[31mT\033[0m"

        print(board % tuple(t))

        print(f"Its {self.engine.turn} turn")
        print(f"There is {20 - len(self.engine.board.goatsPositions)} dead goats")

    def ask_user_action(self):
        a = input("""
                [s]how [m]move
                """)
        if a == "s":
            self.show()
        elif a == "m":
            column = input("Let's choose departure: Select a column: ")
            row = int(input("Select a row: "))

            departure = self.convert_user_input_to_position(row, column)

            column = input("Let's choose destination: Select column of destination:")
            row = int(input("Select row of destination:"))

            destination = self.convert_user_input_to_position(row, column)

            print(f"from {departure} to {destination}")

            if self.is_valid_move(departure, destination):
                self.move(departure, destination)
            else:
                print(f"/!\\ Invalid move : {departure} to {destination}")
                self.ask_user_action()

    def move(self, departure, destination):
        action = Action()
        action.set_destination(destination)
        action.set_departure(departure)

        if self.engine.turn == "tigers":
            if self.is_move_a_capture(departure, destination):
                action.set_is_a_capture()

        self.engine.take_action(action)

    def is_move_a_capture(self, departure, destination):
        if departure in self.engine.board._capture_connections:
            if destination in self.engine.board._capture_connections[departure]:
                return True
        return False

    def is_valid_move(self, departure, destination):

        if self.engine.turn == "goats":
            goat_moves = self.engine.board.get_goats_available_moves()
            if departure in goat_moves:
                if destination in goat_moves[departure]:
                    return True

        elif self.engine.turn == "tigers":
            tiger_moves = self.engine.board.get_tigers_available_moves()
            print(tiger_moves)
            print(departure)
            if departure in tiger_moves:
                if destination in tiger_moves[departure]:
                    return True

            tiger_captures = self.engine.board.get_tigers_available_captures()
            print(tiger_captures)
            print(departure)
            if departure in tiger_captures:
                if destination in tiger_captures[departure]:
                    return True

        print("Move is not valid")
        return False

    def convert_user_input_to_position(self, row, column):
        if column not in ['A', 'B', 'C', 'D', 'E', 'a', 'b', 'c', 'd', 'e']:
            print("Column is not valid")
            raise (ValueError)

        if row > 5 or row <= 0:
            print("row is not valid")
            raise (ValueError)

        return (ord(column.upper()) - ord('A')) + ((row - 1) * 5)
