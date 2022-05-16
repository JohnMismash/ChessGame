# John (Jack) Mismash
# 5/7/2021

"""
This ChessEngine will maintain and support the current state of the game. It will provide
the ability to check for the validity of moves, as well as track the moves that have been made by players
in the current game.
"""


# This chess board is represented as a 8x8 two dimensional (2D) list.
# Each element of this list has two characters:
# The first character represents whether the piece in the game is White/Black.
# The second character represents the type of piece.
# If an element contains "--", then this represents a empty space on the board.
# The empty space square with "--" can still be processed as a string with two characters.

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
        self.WK_moved = False
        self.BK_moved = False

    def processMove(self, starting_square, ending_square):
        move = Move(starting_square, ending_square, self)
        print(move.getChessNotation())

        if move.isValidMove():
            self.ChessBoard[move.startRow][move.startColumn] = "--"
            self.ChessBoard[move.endRow][move.endColumn] = move.movedPiece
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move
            return True

        return True

    # This function will undo a previous move when the 'z' button is pressed.
    # Functionality is set to do nothing if there are no previous moves.
    def undoMove(self):
        print(self.move_log)
        if len(self.move_log) != 0:
            previous_move = self.move_log.pop()
            self.ChessBoard[previous_move.startRow][previous_move.startColumn] = previous_move.movedPiece
            self.ChessBoard[previous_move.endRow][previous_move.endColumn] = previous_move.capturedPiece
            self.white_to_move = not self.white_to_move

    def getValidMoves(self):
        pass

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.ChessBoard)):
            for column in range(len(self.ChessBoard[row])):
                turn = self.ChessBoard[row][column][0]  # 'W' or 'B'
                if (turn == 'W' and self.white_to_move) and (turn == 'B' and not self.white_to_move):
                    current_piece = self.ChessBoard[row][column][1]  # Any given piece.
                    if current_piece == 'P':  # Pawn
                        self.getPawnMoves(row, column, moves)
                    elif current_piece == 'R':  # Rook
                        self.getRookMoves(row, column, moves)
                    elif current_piece == 'N':  # Knight
                        self.getKnightMoves(row, column, moves)
                    elif current_piece == 'B':  # Bishop
                        self.getBishopMoves(row, column, moves)
                    elif current_piece == 'Q':  # Queen
                        self.getQueenMoves(row, column, moves)
                    elif current_piece == 'K':  # King
                        self.getKingMoves(row, column, moves)

    def getPawnMoves(self, row, column, moves):
        pass

    def getRookMoves(self, row, column, moves):
        pass

    def getKnightMoves(self, row, column, moves):
        pass

    def getBishopMoves(self, row, column, moves):
        pass

    def getQueenMoves(self, row, column, moves):
        pass

    def getKingMoves(self, row, column, moves):
        pass


# This class represents a single move within the game. It includes representation for rank/file, tracking to which
# piece recently moved, as well as which piece was recently captured (or a piece moves to an empty square).
class Move:
    # This will allow us to represent our rows and columns in rank/file notation.
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}

    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column_to_files = {value: key for key, value in files_to_columns.items()}

    def __init__(self, starting_square, ending_square, game_state):
        self.startRow = starting_square[0]
        self.startColumn = starting_square[1]

        self.endRow = ending_square[0]
        self.endColumn = ending_square[1]

        self.movedPiece = game_state.ChessBoard[self.startRow][self.startColumn]
        self.capturedPiece = game_state.ChessBoard[self.endRow][self.endColumn]

    # Produces the necessary chess notation for the move log.
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    # Chess notation specifies that the column/file comes before the row/rank.
    def getRankFile(self, row, column):
        return self.column_to_files[column] + self.rows_to_ranks[row]

    # Determines if a move is valid, and is controlled by the Game state.
    def isValidMove(self):
        return True

