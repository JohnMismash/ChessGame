# John (Jack) Mismash
# 5/7/2021

"""
This ChessEngine will maintain and support the current state of the game. It will provide
the ability to check for the validity of moves, as well as track the moves that have been made by players
in the current game.
"""


# This chess board is represented as a 8x8 two dimensional (2D) list. Each element of this list
# has two characters: The first character represents whether the piece in the game is White/Black,
# and the second character represents the type of piece. If an element contains "--", then this
# represents a empty space on the board.

# First Character: W - White, B - Black
# Second Character: R - Rook, N - Knight, Q - Queen, K - King, B - Bishop, P - Pawn

# This class also maintains a record of who's turn it is to move, as well as a move log to track all of
# the moved within the game.
class Game:
    def __init__(self):
        self.ChessBoard = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]
        ]

        self.white_to_move = True
        self.move_log = []


# This class represents a single move within the game. It includes representation for rank/file, as well as
# tracking which piece recently moved, as well as which piece was recently captured (or a piece moves to an
# empty square).
class Move:
    # This will allow us to represent our rows and columns in rank/file notation.
    RanktoRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    RowstoRanks = {value: key for key, value in RanktoRows.items()}

    FilestoColumns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    ColumntoFiles = {value: key for key, value in FilestoColumns.items()}

    def __init__(self, startingSq, endingSq, ChessBoard):
        self.startRow = startingSq[0]
        self.startColumn = startingSq[1]

        self.endRow = endingSq[0]
        self.endColumn = endingSq[1]

        self.movedPiece = ChessBoard[self.startRow][self.startColumn]
        self.capturedPiece = ChessBoard[self.endRow][self.endColumn]

    def GetChessNotation(self):
        pass

    # Chess notation specifies that the column/file comes before the row/rank.
    def GetRankFile(self, row, column):
        return self.ColumntoFiles[column] + self.RowstoRanks[row]
