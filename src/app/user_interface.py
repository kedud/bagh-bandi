from src.domain.engine import Engine, Action


class UserInterface:

    @staticmethod
    def show():

        def show(self, tigerPositions, goatPositions, turn):
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

            for i in tigerPositions:
                t[i] = "T"

            for i in goatPositions:
                if t[i] == "G":
                    t[i] = 2
                elif t[i] == 'o':
                    t[i] = "G"
                elif isinstance(t[i], int):
                    t[i] += 1

            print(board % tuple(t))

            print(f"Its {turn} turn")
            print(f"There is {20 - len(goatPositions)} dead goats")

    @staticmethod
    def convert_user_input_to_position(row, column):
        if column not in ['A', 'B', 'C', 'D', 'E', 'a', 'b', 'c', 'd', 'e']:
            print("Column is not valid")
            raise (ValueError)

        if row > 5 or row <= 0:
            print("row is not valid")
            raise (ValueError)

        return (ord(column.upper()) - ord('A')) + ((row - 1) * 5)
