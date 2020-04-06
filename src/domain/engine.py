from src.domain.board import Board


class Engine:

    def __init__(self):
        self.board = Board()
        self.action_history = []
        self.re_capture_allowed = False

    def take_action(self, action):
        self.re_capture_allowed = False

        if self.board.turn == "goats":
            self.board.turn = "tigers"
            departure_index = self.board.goatsPositions.index(action.departure)
            self.board.goatsPositions[departure_index] = action.destination
        else:
            self.board.turn = "goats"
            departure_index = self.board.tigerPositions.index(action.departure)
            self.board.tigerPositions[departure_index] = action.destination

            if action.get_is_a_capture():
                position = self.get_capture_position(action.departure, action.destination)
                self.kill_goat_by_position(position)

                # Tigers can keep playing if did not jump over a goat stack
                if position not in self.board.goatsPositions:
                    self.board.turn = "tigers"
                    self.re_capture_allowed = True
        self.action_history.append(action)

    @staticmethod
    def get_capture_position(departure, destination):
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

    def is_valid_goat_move(self, departure, destination):
        goat_moves = self.board.get_goats_available_moves()
        if departure in goat_moves.keys():
            if destination in goat_moves[departure]:
                return True
        return False

    def is_valid_tiger_move(self, departure, destination):
        tiger_moves = self.board.get_tigers_available_moves()
        if departure in tiger_moves.keys():
            if destination in tiger_moves[departure]:
                return True
        return False

    def is_valid_tiger_capture(self, departure, destination):
        tiger_captures = self.board.get_tigers_available_captures()
        if departure in tiger_captures.keys():
            if destination in tiger_captures[departure]:
                return True
        return False

    def is_valid_move(self, departure, destination):

        if self.board.turn == "goats" and self.is_valid_goat_move(departure, destination):
            return True

        elif self.board.turn == "tigers":
            if len(self.action_history) > 0 and self.action_history[-1].get_is_a_capture() and \
                self.is_valid_multi_capture(departure, destination):
                    return True
            elif self.is_valid_tiger_move(departure, destination):
                return True
            elif self.is_valid_tiger_capture(departure, destination):
                return True

        print("Move is not valid")
        return False

    def is_valid_multi_capture(self, departure, destination):
        if len(self.action_history) > 0 and self.action_history[-1].get_is_a_capture():
            if self.is_valid_tiger_capture(departure, destination):
                if self.action_history[-1].destination != departure:
                    print("Recapture must use same tiger")
                elif self.get_capture_position(departure, destination) == self.get_capture_position(
                        self.action_history[-1].departure, self.action_history[-1].destination):
                    print("Cannot capture back and forth")
                else:
                    return True
        return False

    def skip_tiger_recapture(self):
        if self.re_capture_allowed:
            self.re_capture_allowed = False
            self.board.turn = "goats"



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
