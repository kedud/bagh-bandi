from src.domain.board import Board


class Engine:

    def __init__(self):
        self.board = Board()

    def take_action(self, action):
        if self.board.turn == "goats":
            self.board.turn = "tigers"
            departureIndex = self.board.goatsPositions.index(action.departure)
            self.board.goatsPositions[departureIndex] = action.destination
        else:
            self.board.turn = "goats"
            departureIndex = self.board.tigerPositions.index(action.departure)
            self.board.tigerPositions[departureIndex] = action.destination
            if action.get_is_a_capture():
                self.board.turn = "tigers"
                position = self.get_capture_position(action.departure, action.destination)
                self.kill_goat_by_position(position)

    def get_capture_position(self, departure, destination):
        return departure + ((destination - departure) >> 1)

    def kill_goat_by_position(self, position):
        self.board.goatsPositions.remove(position)
        self.board.dead_goats += 1

    def move(self, departure, destination):
        action = Action()
        action.set_destination(destination)
        action.set_departure(departure)

        if self.board.turn == "tigers":
            if self.is_move_a_capture(departure, destination):
                action.set_is_a_capture()

        self.take_action(action)

    def is_move_a_capture(self, departure, destination):
        if departure in self.board._capture_connections:
            if destination in self.board._capture_connections[departure]:
                return True
        return False

    def is_valid_move(self, departure, destination):

        if self.board.turn == "goats":
            goat_moves = self.board.get_goats_available_moves()
            if departure in goat_moves.keys():
                if destination in goat_moves[departure]:
                    return True

        elif self.board.turn == "tigers":
            tiger_moves = self.board.get_tigers_available_moves()
            print(tiger_moves)
            print(departure)
            if departure in tiger_moves.keys():
                if destination in tiger_moves[departure]:
                    return True

            tiger_captures = self.board.get_tigers_available_captures()
            print(tiger_captures)
            print(departure)
            if departure in tiger_captures.keys():
                if destination in tiger_captures[departure]:
                    return True

        print("Move is not valid")
        return False


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
