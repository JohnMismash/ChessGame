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
class ChessGame:
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

        self.whiteToMove = True
        self.moveLog = []
        self.WK_moved = False
        self.BK_moved = False

        self.WK_Location = (7, 4)
        self.BK_Location = (0, 4)

    def processMove(self, move):
        if move.movedPiece == "WK":
            self.WK_Location = (move.endRow, move.endColumn)
        elif move.movedPiece == "BK":
            self.BK_Location = (move.endRow, move.endColumn)

        self.ChessBoard[move.startRow][move.startColumn] = "--"
        self.ChessBoard[move.endRow][move.endColumn] = move.movedPiece
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        return True

    # This function will undo a previous move when the 'z' button is pressed.
    # Functionality is set to do nothing if there are no previous moves.
    def undoMove(self):
        if len(self.moveLog) != 0:
            previousMove = self.moveLog.pop()

            if previousMove.movedPiece == "WK":
                self.WK_Location = (previousMove.startRow, previousMove.startColumn)
            elif previousMove.movedPiece == "BK":
                self.BK_Location = (previousMove.startRow, previousMove.startColumn)

            self.ChessBoard[previousMove.startRow][previousMove.startColumn] = previousMove.movedPiece
            self.ChessBoard[previousMove.endRow][previousMove.endColumn] = previousMove.capturedPiece
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        # Generate all possible moves.
        allPossibleMoves = self.getAllPossibleMoves()

        # Individually make each move, although traverse backwards to avoid skipping elements as some are removed.
        for i in range(len(allPossibleMoves) - 1, -1, -1):
            move = allPossibleMoves[i]
            self.processMove(move)
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                allPossibleMoves.remove(move)

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        return allPossibleMoves

    # Determine if the current player is in check.
    def inCheck(self):
        if self.whiteToMove:
            row = self.WK_Location[0]
            column = self.WK_Location[1]
            return self.squareUnderAttack(row, column)

        else:
            row = self.BK_Location[0]
            column = self.BK_Location[1]
            return self.squareUnderAttack(row, column)

    # Determine if the enemy can attack the square (row, column).
    def squareUnderAttack(self, row, column):
        # Switch view to opponent.
        self.whiteToMove = not self.whiteToMove

        # Generate all possible moves for the opponent.
        opponentMoves = self.getAllPossibleMoves()

        # Restore previous turn.
        self.whiteToMove = not self.whiteToMove

        for move in opponentMoves:
            if move.endRow == row and move.endColumn == column:
                return True

        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.ChessBoard)):
            for column in range(len(self.ChessBoard[row])):
                turn = self.ChessBoard[row][column][0]  # 'W' or 'B'

                if (turn == 'W' and self.whiteToMove) or (turn == 'B' and not self.whiteToMove):
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

        return moves

    def getPawnMoves(self, row, column, moves):

        # White Pawn Moves
        if self.whiteToMove:
            # One or two spaces ahead.
            if self.ChessBoard[row - 1][column] == "--":
                moves.append(Move((row, column), (row - 1, column), self))
                if row == 6 and self.ChessBoard[row - 2][column] == "--":
                    moves.append(Move((row, column), (row - 2, column), self))

            # Diagonal Left
            if row > 0 and column > 0 and self.ChessBoard[row - 1][column - 1][0] == 'B':
                moves.append(Move((row, column), (row - 1, column - 1), self))

            # Diagonal Right
            if row > 0 and column < 7 and self.ChessBoard[row - 1][column + 1][0] == 'B':
                moves.append(Move((row, column), (row - 1, column + 1), self))

        # Black Pawn Moves
        else:
            # One or two spaces ahead.
            if self.ChessBoard[row + 1][column] == "--":
                moves.append(Move((row, column), (row + 1, column), self))
                if row == 1 and self.ChessBoard[row + 2][column] == "--":
                    moves.append(Move((row, column), (row + 2, column), self))

            # Diagonal Left
            if row < 7 and column > 0 and self.ChessBoard[row + 1][column - 1][0] == 'W':
                moves.append(Move((row, column), (row + 1, column - 1), self))

            # Diagonal Right
            if row < 7 and column < 7 and self.ChessBoard[row + 1][column + 1][0] == 'W':
                moves.append(Move((row, column), (row + 1, column + 1), self))

        return moves

    def getRookMoves(self, row, column, moves):
        directions = [
            (-1, 0),  # Up
            (0, -1),  # Left
            (1, 0),   # Down
            (0, 1)    # Right
        ]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for direction in directions:
            for row_count in range(1, 8):
                endRow = row + direction[0] * row_count
                endColumn = column + direction[1] * row_count

                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.ChessBoard[endRow][endColumn]

                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endColumn), self))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self))
                        break

                    # Cannot capture friendly pieces.
                    else:
                        break

                # Move does not exist within the ChessBoard boundary.
                else:
                    break

    def getKnightMoves(self, row, column, moves):
        directions = [
            (-1, 2),   # Up one, right two
            (-2, 1),   # Up two, right one
            (-1, -2),  # Up one, left two
            (-2, -1),  # Up two, left one
            (1, 2),    # Down one, right two
            (2, 1),    # Down two, right one
            (1, -2),   # Down one, left two
            (2, -1)    # Down two, left one
        ]

        allyColor = 'W' if self.whiteToMove else 'B'

        for direction in directions:
            endRow = row + direction[0]
            endColumn = column + direction[1]

            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.ChessBoard[endRow][endColumn]

                if endPiece[0] != allyColor:
                    moves.append(Move((row, column), (endRow, endColumn), self))

    def getBishopMoves(self, row, column, moves):
        directions = [
            (-1, -1),  # Up one, left one (Northwest)
            (-1, 1),   # Up one, right one (Northeast)
            (1, -1),   # Down one, left one (Southwest)
            (1, 1)     # Down one, right one (Southeast)
        ]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for direction in directions:
            for row_count in range(1, 8):
                endRow = row + direction[0] * row_count
                endColumn = column + direction[1] * row_count

                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.ChessBoard[endRow][endColumn]

                    if endPiece == "--":
                        moves.append(Move((row, column), (endRow, endColumn), self))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self))
                        break

                    # Cannot capture friendly pieces.
                    else:
                        break

                # Move does not exist within the ChessBoard boundary.
                else:
                    break

    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        directions = [
            (-1, 0),   # Up one
            (1, 0),    # Down one
            (0, -1),   # Left one
            (0, 1),   # Right one
            (-1, 1),   # Up one, right one
            (-1, -1),  # Up one, left one
            (1, 1),    # Down one, right one
            (1, -1)    # Down one, left one
        ]

        allyColor = 'W' if self.whiteToMove else 'B'

        for direction in directions:
            endRow = row + direction[0]
            endColumn = column + direction[1]

            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.ChessBoard[endRow][endColumn]

                if endPiece[0] != allyColor:
                    moves.append(Move((row, column), (endRow, endColumn), self))


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

        # Unique ID for each move.
        self.moveID = self.startRow * 1000 + self.endRow * 100 + self.startColumn * 10 + self.endColumn

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True

        return False

    # Produces the necessary chess notation for the move log.
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    # Chess notation specifies that the column/file comes before the row/rank.
    def getRankFile(self, row, column):
        return self.column_to_files[column] + self.rows_to_ranks[row]

