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
