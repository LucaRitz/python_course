from enum import Enum

class Player(Enum):
    A = 0,
    B = 1


class GameOfNim:

    def __init__(self):
        self.current_player = Player.A
        self.matches = []
        self.previous_bits = []
        self.winning_games = {}
        self.loosing_games = {}

    def start_game(self):
        self.matches = [1, 3, 5, 7]
        self.current_player = Player.A
        self.winning_games = GameOfNim.__init_zero()
        self.loosing_games = GameOfNim.__init_zero()
        self.next_round()

    def next_round(self):
        GameOfNim.print_field(self.matches)
        print('Current Player: ' + str(self.current_player))
        row, amount_of_matches = GameOfNim.get_move(self.matches)
        self.matches[row] -= amount_of_matches
        other_player = GameOfNim.other_player(self.current_player)
        won_rows = GameOfNim.column_won(self.matches)

        if won_rows:
            GameOfNim.increment(self.loosing_games, other_player)
        else:
            GameOfNim.increment(self.winning_games, other_player)

        if GameOfNim.finish(self.matches):
            print('Finished game')
        else:
            self.current_player = other_player
            self.next_round()


    @staticmethod
    def __init_zero():
        return {
            Player.A: 0,
            Player.B: 0
        }

    @staticmethod
    def print_field(matches):
        for inx, match_in_row in enumerate(matches):
            print(str(inx) + ':  ', end='')
            for _ in match_in_row:
                print('| ', end='')
            print('')

    @staticmethod
    def get_move(state):
        row = 0
        amount_of_matches = 0
        while not GameOfNim.valid_move(state, row, amount_of_matches):
            print('Row: ', end='')
            row = int(input())
            print('Matches', end='')
            amount_of_matches = int(input())
        return row, amount_of_matches

    @staticmethod
    def valid_move(state, row, amount_of_matches):
        return 0 <= row <= 3 and state[row] >= amount_of_matches > 0

    @staticmethod
    def other_player(player):
        return Player.A if player == Player.B else Player.B

    @staticmethod
    def column_won(state):
        won_column = []
        for column in range(0,3):
            moved = []
            for amount_of_matches in state:
                moved.append(amount_of_matches >> column)
            prev_bit = moved.pop(0)
            for bit in moved:
                prev_bit = prev_bit ^ bit

            if prev_bit == 0:
                won_column.append(column)
        return won_column

    @staticmethod
    def increment(games, player):
        games[player] = games[player] + 1

    @staticmethod
    def finish(state):
        is_finished = True
        for amount_of_matches in state:
            is_finished &= amount_of_matches == 0

        return is_finished
