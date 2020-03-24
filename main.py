import numpy as np


class Board():

    # possible connections from one point to another
    _move_connections = {
        0: [1, 5, 6], 1: [2, 0, 6], 2: [3, 1, 7, 6, 8], 3: [4, 2, 8], 4: [3, 9, 8],
        5: [6, 10, 0], 6: [7, 5, 11, 1, 10, 2, 12, 0], 7: [8, 6, 12, 2], 8: [9, 7, 13, 3, 12, 4, 14, 2], 9: [8, 14, 4],
        10: [11, 15, 5, 6, 16], 11: [12, 10, 16, 6], 12: [13, 11, 17, 7, 16, 8, 18, 6], 13: [14, 12, 18, 8],
        14: [13, 19, 9, 18, 8],
        15: [16, 20, 10], 16: [17, 15, 21, 11, 20, 12, 22, 10], 17: [18, 16, 22, 12],
        18: [19, 17, 23, 13, 22, 14, 24, 12], 19: [18, 24, 14],
        20: [21, 15, 16], 21: [22, 20, 16], 22: [23, 21, 17, 18, 16], 23: [24, 22, 18], 24: [23, 19, 18]
    }

    _capture_connections = {
        0: [2, 10, 12], 1: [3, 11], 2: [4, 0, 12, 10, 14], 3: [1, 13], 4: [2, 14, 12],
        5: [7, 15], 6: [8, 16, 18], 7: [9, 5, 17], 8: [6, 18, 16], 9: [7, 19],
        10: [12, 20, 0, 2, 22], 11: [13, 21, 1], 12: [14, 10, 22, 2, 20, 4, 24, 0],
        13: [11, 23, 3], 14: [12, 24, 4, 22, 2],
        15: [17, 5], 16: [18, 6, 8], 17: [19, 15, 7], 18: [16, 8, 6], 19: [17, 9],
        20: [22, 10, 12], 21: [23, 11], 22: [24, 20, 12, 14, 10], 23: [21, 13], 24: [22, 14, 12]
    }

    def __init__(self):
        self.tigerPositions = [8, 17]
        self.goatsPositions = [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 11, 11, 11, 11, 11, 13, 13, 13, 13, 13]
        self.dead_goats = 0

    def get_tigers_available_moves(self):
        available_moves = {}
        for tigerFrom in self.tigerPositions:
            for tigerDestination in self._move_connections[tigerFrom]:
                # If tiger destination is not busy
                if tigerDestination not in self.tigerPositions and tigerDestination not in self.goatsPositions:
                    if tigerFrom in available_moves:
                        available_moves[tigerFrom].append(tigerDestination)
                    else:
                        available_moves[tigerFrom] = [tigerDestination]
        return available_moves
    
    def get_tigers_available_captures(self):
        available_captures = {}
        for tigerFrom in self.tigerPositions:
            for tigerDestination in self._capture_connections[tigerFrom]:
                # If tiger destination is not busy
                if tigerDestination not in self.tigerPositions and tigerDestination not in self.goatsPositions:
                    if tigerFrom in available_captures:
                        available_captures[tigerFrom].append(tigerDestination)
                    else:
                        available_captures[tigerFrom] = [tigerDestination]
        return available_captures
    
    def get_goats_available_moves(self):
        available_moves = {}
        for goatFrom in np.unique(self.goatsPositions):
            for goatDestination in self._move_connections[goatFrom]:
                # If goat destination is not busy
                if goatDestination not in self.tigerPositions and goatDestination not in self.goatsPositions:
                    if goatFrom in available_moves:
                        available_moves[goatFrom].append(goatDestination)
                    else:
                        available_moves[goatFrom] = [goatDestination]
        return available_moves



class Action:
    def __init__(self):
        self.destination = None
        self.departure = None
        self.is_a_capture = False

    def set_destination(self, destination):
        self.destination = destination
        
    def set_departure(self, departure):
        self.departure = departure

    def set_is_a_capture(self):
        self.is_a_capture = True

    def get_is_a_capture(self):
        return self.is_a_capture


class Engine:

    def __init__(self):
        self.board = Board()
        self.turn = "tigers"

    def take_action(self, action):
        if self.turn == "goats":
            self.turn = "tigers"
            departureIndex = self.board.goatsPositions.index(action.departure)
            self.board.goatsPositions[departureIndex] = action.destination
        else:
            self.turn = "goats"
            departureIndex = self.board.tigerPositions.index(action.departure)
            self.board.tigerPositions[departureIndex] = action.destination
            if action.get_is_a_capture():
                self.turn = "tigers"
                self.a_aptured_occured = True
                position = self.get_capture_position(action.departure, action.destination)
                self.kill_goat_by_position(position)

    def get_capture_position(self, departure, destination):
            return departure + ((destination - departure) >> 1)

    def kill_goat_by_position(self, position):
        self.board.goatsPositions.remove(position)
        self.board.dead_goats += 1 

    
class UserInterface():
    
    def __init__(self):
        self.engine = Engine()

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
            self.move(departure, destination)

    def move(self, departure, destination):
        if not self.is_valid_move(departure, destination):
            raise(ValueError)

        action = Action()
        action.set_destination(destination)
        action.set_departure(departure)

        if self.engine.turn == "tigers":
            if(self.is_move_a_capture(departure, destination)):
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
            raise(ValueError)
        
        if row > 5 or row <= 0: 
            print("row is not valid")
            raise(ValueError)

        return (ord(column.upper()) - ord('A')) + ((row - 1) * 5)


ui = UserInterface()

while True:
    ui.ask_user_action()
