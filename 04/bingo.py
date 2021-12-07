#!/usr/bin/env python3

import math
import sys

class Bingo:
    """
    Stores the loaded state of a sequence of called numbers and a collection
    of bingo boards and supports checking for multiple win conditions for
    this game of bingo.
    """

    def __init__(self, input_file):
        # Read the called numbers, comma-separated on the first line
        input_lines = [l.strip() for l in input_file]
        self._called = [int(n) for n in input_lines[0].split(",")]

        # Read the boards, separated by empty lines
        self._boards = []
        board_lines = []
        for input_line in input_lines[1:]:
            if not input_line:
                if board_lines:
                    self._boards.append(Board(board_lines))
                board_lines = []
            else:
                board_lines.append(input_line)

    def __str__(self):
        # Reverse the read and format the called numbers and then the boards
        output = []
        output.append(",".join([str(n) for n in self._called]))
        output.append("\n\n")
        for board in self._boards:
            output.append(str(board))
            output.append("\n")
        return "".join(output)

    def reset(self):
        """
        Reset the state of all of the boards in this game.
        """

        for board in self._boards:
            board.reset()

    def find_winning_board(self):
        """
        Find the first board to win after a called number.
        """

        # Reset the board state in case we're running this game multiple times
        self.reset()

        # Call each number in turn, updating each board in turn
        for number in self._called:
            for board in self._boards:
                win = board.call(number)
                if win:
                    # This board just won, so we can stop playing
                    return board

        # We called all the numbers but no board won
        return None

    def find_last_winning_board(self):
        """
        Find the last board that will win.
        """

        # Reset the board state in case we're running this game multiple times
        self.reset()

        # Track whether a board has won
        winning_boards = set([])

        # Call each number in turn, updating each board in turn
        for number in self._called:
            for board in self._boards:
                win = board.call(number)
                if win:
                    winning_boards.add(board)
                    if len(winning_boards) == len(self._boards):
                        # All of the boards are winners and this was the last winner, so we can stop playing
                        return board

        # We called all the numbers but either the last winner wasn't the last board or no board won
        return None

class Board:
    """
    Stores the loaded state of one bingo card and tracks matching number state
    as numbers as called.
    """

    def __init__(self, board_lines):
        # Parse the board grid of N values per N lines
        self._board = [[int(n) for n in l.split()] for l in board_lines]
        self._size = len(self._board)

        # Create a fast reverse lookup dictionary from values to board
        # coordinates indexed at (0,0) in the upper left
        self._lookup_by_number = {}
        for i, row in enumerate(self._board):
            for j, number in enumerate(row):
                self._lookup_by_number[number] = (i, j)

        # Initialize the marked state tracking
        self.reset()

    def __str__(self):
        # Determine padding based on largest possible value
        padding = int(math.ceil(math.log(self._size**2, 10))) + 1
        print(padding)

        # Reverse the read format and space out the boards
        output = []
        for i, row in enumerate(self._board):
            for j, number in enumerate(row):
                if self._marked[i][j]:
                    # Use ANSI bold escape
                    output.append('\033[1m')
                output.append(str(number).rjust(padding, " "))
                if self._marked[i][j]:
                    # End ANSI escape
                    output.append('\033[0m')
            output.append("\n")
        return "".join(output)

    def reset(self):
        """
        Reset the board state by clearing marked and streak trackers.
        """

        # Create a grid of equal size as the board holding booleans to track called numbers
        self._marked = []
        for i in range(self._size):
            self._marked.append([False]*self._size)

        # Cache streak counters by row, column, and diagonal so we don't have to loop to check for wins
        self._streaks = {
            "rows": [0]*self._size,
            "columns": [0]*self._size,
            "diagonals": [0]*2
        }

        # Track the last number called; used as part of scoring
        self._last_call = None

    def call(self, number):
        """
        Update the marked/streaks state when a number is called
        """

        self._last_call = number
        if number in self._lookup_by_number:
            # Get the coordinates holding this value from our reverse lookup dictionary and update state
            (i, j) = self._lookup_by_number[number]
            self._marked[i][j] = True
            self._streaks["rows"][i] += 1
            self._streaks["columns"][j] += 1
            if i == j:
                # Update the upper left to lower right diagonal
                self._streaks["diagonals"][0] += 1
            elif i + j == self._size:
                # Update the lower left to upper right diagonal
                self._streaks["diagonals"][1] += 1

        # Check if this board has won
        return self.is_winner()

    def is_winner(self, use_diagonals=False):
        """
        Helper method for more efficient win condition checking.

        By default only vertical and horizontal completed streaks are winners.
        """

        # Loop over the streak counters, checking for any that have hit the board size
        for category, streaks in self._streaks.items():
            # Only consider diagonals winners if specified.
            if category != "diagonals" or use_diagonals == True:
                for streak in streaks:
                    if streak == self._size:
                        return True

        # No streak at size, no winner
        return False

    def get_score(self):
        """
        Calculate a board's score based on the rules where it's the product of
        the last number called and the sum of any unmarked entries on the board
        """

        unmarked_sum = 0
        for i, row in enumerate(self._board):
            for j, number in enumerate(row):
                if not self._marked[i][j]:
                    unmarked_sum += number
        return (unmarked_sum, self._last_call, unmarked_sum*self._last_call)

def main(input_path):
    """
    Entry point for puzzle day 2021.12.04
    """

    # Open the provided input
    with open(input_path) as input_file:
        # Initialize the game state from the input
        bingo = Bingo(input_file)

        # Calculate and print results
        winner = bingo.find_winning_board()
        print("Winning board:")
        print(winner)
        print("Final score: %d * %d = %d" % winner.get_score())
        last_winner = bingo.find_last_winning_board()
        print("Last winning board:")
        print(last_winner)
        print("Final score: %d * %d = %d" % last_winner.get_score())

if __name__ == "__main__":
    main(sys.argv[1])
