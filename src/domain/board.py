import numpy as np


class Board:

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
        self.turn = "tigers"

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

    def terminal_test(self):
        """
        defines if the board position (or state) reached the end of the game.

        :return:
            True if the game is over

        :rtype:boolean
        """
        pass

    def utility_function(self, p):
        """
        defines the final numeric value for a game that ends in a terminal state s for player p.

        :param p:
            player for which the board position (or state) s is evaluated
        :return:
            utility of a given state for a player

        :rtype:float
        """
        if self.terminal_test():
            pass
        else:
            pass
