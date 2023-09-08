# John (Jack) Mismash
# 3/15/23

"""
This ChessEngine will maintain and support the current state of the game. It will provide
the ability to check for the validity of moves, as well as track the moves that have been made by players
in the current game.
"""


class CastleRights:
    """
    This class represents the Castling rights for the White and Black pieces.
    """

    def __init__(self, WKs: bool, BKs: bool, WQs: bool, BQs: bool):
        self.WKs: bool = WKs
        self.BKs: bool = BKs
        self.WQs: bool = WQs
        self.BQs: bool = BQs


class Move:
    """
    This class represents a single move within the game.
    It includes representation for rank/file, which piece was recently moved, and which piece was recently captured.
    """

    # This will allow us to represent our rows and columns in rank/file notation.
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}

    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    column_to_files = {value: key for key, value in files_to_columns.items()}

    def __init__(self, starting_square, ending_square, game_state,
                 isPawnPromotion=False,
                 isEnPassantMove=False,
                 isCastleMove=False):

        self.startRow = starting_square[0]
        self.startColumn = starting_square[1]

        self.endRow = ending_square[0]
        self.endColumn = ending_square[1]

        self.movedPiece = game_state.ChessBoard[self.startRow][self.startColumn]
        self.capturedPiece = game_state.ChessBoard[self.endRow][self.endColumn]

        # Unique ID for each move.
        self.moveID = self.startRow * 1000 + self.endRow * 100 + self.startColumn * 10 + self.endColumn

        # Check for pawn promotion.
        self.isPawnPromotion = isPawnPromotion

        # Check for En Passant.
        self.isEnPassant = isEnPassantMove

        if self.isEnPassant:
            self.capturedPiece = 'BP' if self.movedPiece == 'WP' else 'WP'

        # Check for Castling.
        self.isCastleMove = isCastleMove

    def __eq__(self, other):
        """
        Checks if this move is equivalent to another move based on its uniquely generated ID.

        :param other: The other move to compare against.
        :type other: Move
        :returns:
            True: Returns True if the move is equivalent to another move.
            False: Returns False if the move is nonequivalent to another move.
        :rtype: bool
        """

        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True

        return False

    # Produces the necessary chess notation for the move log.
    def getChessNotation(self):
        """
        Generates the necessary chess notation for the move log.

        :return: The generated chess notation of a move.
        :rtype: str
        """

        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    # Chess notation specifies that the column/file comes before the row/rank.
    def getRankFile(self, row: int, column: int):
        """
        Generates the rank/file notation given a single row and column.

        :param row: The current row of the move.
        :type row: int
        :param column: The current column of the move.
        :type column: int
        :return: The generated chess notation of a row and column.
        :rtype: str
        """

        return self.column_to_files[column] + self.rows_to_ranks[row]


class ChessGame:
    """
    This class represents a single Chess game.
    """

    def __init__(self):

        # The ChessBoard is represented as a 8x8 two dimensional (2D) list with two-character string elements.
        # Elements with "--" represent an empty space on the board with no piece.

        # The first char is the piece color in the game:
        # 'W' - White or 'B' - Black.

        # The second char is the piece type:
        # 'R' - Rook, 'N' - Knight, 'Q' - Queen, 'K' - King, 'B' - Bishop, and 'P' - Pawn

        # self.ChessBoard = [
        #     ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
        #     ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
        #     ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]
        # ]

        self.ChessBoard = [
            ["--", "--", "--", "BK", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "WK", "--", "--", "--", "WQ"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]

        self.whiteToMove = True

        self.moveLog = []

        self.WK_Location = (7, 4)
        self.BK_Location = (0, 4)

        # Variables for the naive and advanced algorithm.
        self.checkmate = False
        self.stalemate = False

        # Variables for advanced algorithm.
        self.pins = []
        self.checks = []
        self.inCheckByPiece = False

        # Coordinates for a possible en-passant capture square.
        self.enPassantPossible = ()

        self.currentCastleRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastleRight.WKs, self.currentCastleRight.BKs,
                                             self.currentCastleRight.WQs, self.currentCastleRight.BQs)]

    def processMove(self, move: Move):
        """
        Processes a single move, including player turn, castling rights, and updating the move log.

        :param move: The user selected move.
        :return: None
        """

        if move.movedPiece == "WK":
            self.WK_Location = (move.endRow, move.endColumn)

        elif move.movedPiece == "BK":
            self.BK_Location = (move.endRow, move.endColumn)

        # Remove the piece from its starting location.
        self.ChessBoard[move.startRow][move.startColumn] = "--"
        self.ChessBoard[move.endRow][move.endColumn] = move.movedPiece

        self.moveLog.append(move)

        self.whiteToMove = not self.whiteToMove

        # Check if the move made creates an En Passant situation.
        if move.movedPiece[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.endColumn)

        else:
            self.enPassantPossible = ()

        # If the move is an EnPassant move, update the board to represent the correct pieces.
        if move.isEnPassant:
            self.ChessBoard[move.startRow][move.endColumn] = "--"

        # If the move is a pawn promotion, default the piece to be a queen.
        # TODO: Update pawn promotion to include Knight, Bishop and Rook.
        if move.isPawnPromotion:
            self.ChessBoard[move.endRow][move.endColumn] = move.movedPiece[0] + 'Q'

        if move.isCastleMove:
            # Check if the move is a King or Queen side Castle.
            if move.endColumn - move.startColumn == 2:
                self.ChessBoard[move.endRow][move.endColumn - 1] = self.ChessBoard[move.endRow][move.endColumn + 1]
                self.ChessBoard[move.endRow][move.endColumn + 1] = "--"

            else:
                self.ChessBoard[move.endRow][move.endColumn + 1] = self.ChessBoard[move.endRow][move.endColumn - 2]
                self.ChessBoard[move.endRow][move.endColumn - 2] = "--"

        # Update castle rights when a rook or king makes a move.
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRight.WKs, self.currentCastleRight.BKs,
                                                 self.currentCastleRight.WQs, self.currentCastleRight.BQs))

    def undoMove(self):
        """
        Undoes a single previously processed move when the 'z' key is pressed.
        Assumes that there is a previous processed move to undo.
        """

        if len(self.moveLog) != 0:
            previousMove = self.moveLog.pop()

            if previousMove.movedPiece == "WK":
                self.WK_Location = (previousMove.startRow, previousMove.startColumn)

            elif previousMove.movedPiece == "BK":
                self.BK_Location = (previousMove.startRow, previousMove.startColumn)

            self.ChessBoard[previousMove.startRow][previousMove.startColumn] = previousMove.movedPiece
            self.ChessBoard[previousMove.endRow][previousMove.endColumn] = previousMove.capturedPiece
            self.whiteToMove = not self.whiteToMove

            # If an EnPassant move, we must update the board accordingly, and restore the possible move.
            if previousMove.isEnPassant:
                self.ChessBoard[previousMove.endRow][previousMove.endColumn] = "--"
                self.ChessBoard[previousMove.startRow][previousMove.endColumn] = previousMove.capturedPiece
                self.enPassantPossible = (previousMove.endRow, previousMove.endColumn)

            # If a two pawn advance move was undone, then the possible enPassant move must be cleared.
            if previousMove.movedPiece[1] == 'P' and abs(previousMove.startRow - previousMove.endRow) == 2:
                self.enPassantPossible = ()

            # Undo Castle move.
            self.castleRightsLog.pop()

            # Get the last item in the log and set the current Castle Rights.
            newCastleRights = self.castleRightsLog[-1]
            self.currentCastleRight = CastleRights(newCastleRights.WKs, newCastleRights.BKs,
                                                   newCastleRights.WQs, newCastleRights.BQs)

            # Undo the Castle Move
            if previousMove.isCastleMove:
                # King Side Castle
                if previousMove.endColumn - previousMove.startColumn == 2:
                    # Fix Rook placement.
                    self.ChessBoard[previousMove.endRow][previousMove.endColumn + 1] = \
                        self.ChessBoard[previousMove.endRow][previousMove.endColumn - 1]

                    # Remove Rook.
                    self.ChessBoard[previousMove.endRow][previousMove.endColumn - 1] = "--"

                # Queen Side Castle
                else:
                    # Fix Rook placement.
                    self.ChessBoard[previousMove.endRow][previousMove.endColumn - 2] = \
                        self.ChessBoard[previousMove.endRow][previousMove.endColumn + 1]

                    # Remove Rook.
                    self.ChessBoard[previousMove.endRow][previousMove.endColumn + 1] = "--"

        self.checkmate = False
        self.stalemate = False

    def getValidMovesNaive(self):
        """
        Generates all valid moves by processing each move and identifying which moves result in check, checkmate, or
        stalemate.

        :return:
        """

        # Save the previous information about EnPassant and Castling Rights.
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastleRight.WKs, self.currentCastleRight.BKs,
                                        self.currentCastleRight.WQs, self.currentCastleRight.BQs)

        # Generate all possible moves.
        allPossibleMoves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.WK_Location[0], self.WK_Location[1], allPossibleMoves, not self.whiteToMove)

        else:
            self.getCastleMoves(self.BK_Location[0], self.BK_Location[1], allPossibleMoves, not self.whiteToMove)

        # Individually make each move, although traverse backwards to avoid skipping elements as some are removed.
        for i in range(len(allPossibleMoves) - 1, -1, -1):
            move = allPossibleMoves[i]
            self.processMove(move)
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                allPossibleMoves.remove(move)

            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        # Check for checkmate and stalemate.
        if len(allPossibleMoves) == 0:
            if self.inCheck():
                self.checkmate = True
                self.stalemate = False
            else:
                self.stalemate = True
                self.checkmate = False

        else:
            self.checkmate = False
            self.stalemate = False

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastleRight = tempCastleRights

        return allPossibleMoves

    # Advanced solution to generating valid moves.
    def getValidMovesAdvanced(self):
        """
        Generates a list of valid moves based on the current ChessBoard by identifying all possible moves,
        then removing moves that are invalid based on checks or multi-checks.

        :return validMoves: The list of valid moves.
        :rtype: list
        """

        validMoves: list = []
        self.inCheckByPiece, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            kingRow = self.WK_Location[0]
            kingColumn = self.WK_Location[1]

        else:
            kingRow = self.BK_Location[0]
            kingColumn = self.BK_Location[1]

        if self.inCheckByPiece:
            # Check is a single check, user can only block check or move the king.
            if len(self.checks) == 1:
                validMoves = self.getAllPossibleMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkColumn = check[1]
                pieceCreatingCheck = self.ChessBoard[checkRow][checkColumn]

                validSquaresToBlockOrCapture = []

                # If the Knight is forcing check, the user can only capture the knight or move the king.
                if pieceCreatingCheck[1] == 'N':
                    validSquaresToBlockOrCapture = [(checkRow, checkColumn)]

                # Otherwise, other pieces may block for the king.
                else:
                    for i in range(1, 8):
                        # check[2] and check[3] are the check directions.
                        validSquare = (kingRow + check[2] * i, kingColumn + check[3] * i)
                        validSquaresToBlockOrCapture.append(validSquare)

                        if validSquare[0] == checkRow and validSquare[1] == checkColumn:
                            break

                for i in range(len(validMoves) - 1, -1, -1):
                    if validMoves[i].movedPiece[1] != 'K':
                        if not (validMoves[i].endRow, validMoves[i].endColumn) in validSquaresToBlockOrCapture:
                            validMoves.remove(validMoves[i])

            # Check is a double (or more) check, so the checked user must move its king.
            else:
                self.getKingMoves(kingRow, kingColumn, validMoves)

        else:
            validMoves = self.getAllPossibleMoves()

        return validMoves

    def checkForPinsAndChecks(self):
        """
        Identifies any pins or checks based on the current piece color.

        :return
            inCheck:
            pins:
            checks:

        :rtype
            inCheck: bool
            pins: list
            checks: list
        """

        inCheck = False
        pins = []
        checks = []

        if self.whiteToMove:
            enemyColor = 'B'
            allyColor = 'W'
            startRow = self.WK_Location[0]
            startColumn = self.WK_Location[1]

        else:
            enemyColor = 'W'
            allyColor = 'B'
            startRow = self.BK_Location[0]
            startColumn = self.BK_Location[1]

        # Directions are based on a 8 x 8 board, with (0, 0) starting in the top left corner of the board.
        directions = [
            (-1, 0),  # Up one
            (0, -1),  # Left one
            (1, 0),  # Down one
            (0, 1),  # Right one
            (-1, -1),  # Up one, left one
            (-1, 1),  # Up one, right one
            (1, -1),  # Down one, left one
            (1, 1),  # Down one, right one
        ]

        # For each possible direction for the king:
        for i in range(len(directions)):
            direction = directions[i]
            possiblePin = ()

            # For each possible length of squares in that direction:
            for j in range(1, 8):
                endRow = startRow + direction[0] * j
                endColumn = startColumn + direction[1] * j

                # If the ending square exists on the board:
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.ChessBoard[endRow][endColumn]

                    # If the piece is an ally, it may exist as a pinned piece.
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endColumn, direction[0], direction[1])

                        # Not in check.
                        else:
                            break

                    # Otherwise, this opposing piece may be putting the king in a pin or check
                    elif endPiece[0] == enemyColor:
                        piece = endPiece[1]

                        # Types of pins/checks:
                        # 1. Orthogonally away from king and piece is a rook.
                        # 2. Diagonally away from king and piece is a bishop.
                        # 3. One square away from king diagonally, and piece is a pawn.
                        # 4. Any direction and piece is a queen.
                        # 5. Any direction one square away and piece is a king.
                        # 6. Piece is a knight (see code after the first 5 conditions).
                        if (0 <= i <= 3 and piece == 'R') \
                                or (4 <= i <= 7 and piece == 'B') \
                                or (j == 1 and piece == 'P' and ((enemyColor == 'W' and 6 <= i <= 7)
                                                                 or (enemyColor == 'B' and 4 <= i <= 5))) \
                                or (piece == 'Q') \
                                or (j == 1 and piece == 'K'):

                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endColumn, direction[0], direction[1]))
                                break

                            else:
                                pins.append(possiblePin)

                        # Piece is not applying check.
                        else:
                            break

                else:
                    break

        knightMoves = [
            (-2, -1),  # Up two, left one
            (-2, 1),  # Up two, right one
            (-1, -2),  # Up one, left two
            (-1, 2),  # Up one, right two
            (1, -2),  # Down one, left two
            (1, 2),  # Down one, right two
            (2, -1),  # Down two, left one
            (2, 1)  # Down two, right one
        ]

        # Generate knight check conditions.
        for move in knightMoves:
            endRow = startRow + move[0]
            endColumn = startColumn + move[1]

            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.ChessBoard[endRow][endColumn]

                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endColumn, move[0], move[1]))

        return inCheck, pins, checks

    def inCheck(self):
        """
        Determine if the current player is in check.
        :return:
        """

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
        """

        :param row:
        :param column:
        :return:
        """

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
        """

        :return:
        """

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
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'B'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'W'

        pawnPromotion = False

        # One or two spaces ahead.
        if self.ChessBoard[row + moveAmount][column] == "--":
            # Pin direction is the same direction as where pawn wants to go, and pawn is not pinned.
            if not piecePinned or pinDirection == (moveAmount, 0):
                if row + moveAmount == backRow:
                    pawnPromotion = True

                moves.append(Move((row, column), (row + moveAmount, column), self,
                                  isPawnPromotion=pawnPromotion))

                if row == startRow and self.ChessBoard[row + 2 * moveAmount][column] == "--":
                    moves.append(Move((row, column), (row + 2 * moveAmount, column), self))

        # Diagonal Left
        if column > 0:
            # Pin direction is the same direction as where pawn wants to go, and pawn is not pinned.
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.ChessBoard[row + moveAmount][column - 1][0] == enemyColor:
                    if row + moveAmount == backRow:
                        pawnPromotion = True

                    moves.append(Move((row, column), (row + moveAmount, column - 1), self,
                                      isPawnPromotion=pawnPromotion))

                if (row + moveAmount, column - 1) == self.enPassantPossible:
                    moves.append(
                        Move((row, column), (row + moveAmount, column - 1), self,
                             isEnPassantMove=True))

        # Diagonal Right
        if column < 7:
            # Pin direction is the same direction as where pawn wants to go, and pawn is not pinned.
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.ChessBoard[row + moveAmount][column + 1][0] == enemyColor:
                    if row + moveAmount == backRow:
                        pawnPromotion = True

                    moves.append(Move((row, column), (row + moveAmount, column + 1), self,
                                      isPawnPromotion=pawnPromotion))

                if (row + moveAmount, column + 1) == self.enPassantPossible:
                    moves.append(Move((row, column), (row + moveAmount, column + 1), self,
                                      isEnPassantMove=True))

        return moves

    def getRookMoves(self, row, column, moves):
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.ChessBoard[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                    break

        directions = [
            (-1, 0),  # Up
            (0, -1),  # Left
            (1, 0),  # Down
            (0, 1)  # Right
        ]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for direction in directions:
            for i in range(1, 8):
                endRow = row + direction[0] * i
                endColumn = column + direction[1] * i

                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.ChessBoard[endRow][endColumn]

                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
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
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        piecePinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = [
            (-1, 2),  # Up one, right two
            (-2, 1),  # Up two, right one
            (-1, -2),  # Up one, left two
            (-2, -1),  # Up two, left one
            (1, 2),  # Down one, right two
            (2, 1),  # Down two, right one
            (1, -2),  # Down one, left two
            (2, -1)  # Down two, left one
        ]

        allyColor = 'W' if self.whiteToMove else 'B'

        for direction in directions:
            endRow = row + direction[0]
            endColumn = column + direction[1]

            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                if not piecePinned:
                    endPiece = self.ChessBoard[endRow][endColumn]

                    if endPiece[0] != allyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self))

    def getBishopMoves(self, row, column, moves):
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.ChessBoard[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                    break

        directions = [
            (-1, -1),  # Up one, left one (Northwest)
            (-1, 1),  # Up one, right one (Northeast)
            (1, -1),  # Down one, left one (Southwest)
            (1, 1)  # Down one, right one (Southeast)
        ]

        enemyColor = 'B' if self.whiteToMove else 'W'

        for direction in directions:
            for row_count in range(1, 8):
                endRow = row + direction[0] * row_count
                endColumn = column + direction[1] * row_count

                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
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
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    def getKingMoves(self, row, column, moves):
        """

        :param row:
        :param column:
        :param moves:
        :return:
        """

        directions = [
            (-1, 0),  # Up one
            (1, 0),  # Down one
            (0, -1),  # Left one
            (0, 1),  # Right one
            (-1, 1),  # Up one, right one
            (-1, -1),  # Up one, left one
            (1, 1),  # Down one, right one
            (1, -1)  # Down one, left one
        ]

        allyColor = 'W' if self.whiteToMove else 'B'

        for direction in directions:
            endRow = row + direction[0]
            endColumn = column + direction[1]

            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.ChessBoard[endRow][endColumn]

                if endPiece[0] != allyColor:
                    if allyColor == 'W':
                        self.WK_Location = (endRow, endColumn)
                    else:
                        self.BK_Location = (endRow, endColumn)

                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((row, column), (endRow, endColumn), self))

                    if allyColor == 'W':
                        self.WK_Location = (row, column)
                    else:
                        self.BK_Location = (row, column)

    def getCastleMoves(self, row, column, moves, allyColor):
        """

        :param row:
        :param column:
        :param moves:
        :param allyColor:
        :return:
        """

        if self.squareUnderAttack(row, column):
            return

        if (self.currentCastleRight.WKs and self.whiteToMove) \
                or (self.currentCastleRight.BKs and not self.whiteToMove):
            self.getKingSideCastleMoves(row, column, moves, allyColor)

        if (self.currentCastleRight.WQs and self.whiteToMove) \
                or (self.currentCastleRight.BQs and not self.whiteToMove):
            self.getQueenSideCastleMoves(row, column, moves, allyColor)

    def getKingSideCastleMoves(self, row, column, moves, allyColor):
        """

        :param row:
        :param column:
        :param moves:
        :param allyColor:
        :return:
        """

        if self.ChessBoard[row][column + 1] == "--" and self.ChessBoard[row][column + 2] == "--":
            if not self.squareUnderAttack(row, column + 1) and not self.squareUnderAttack(row, column + 2):
                moves.append(Move((row, column), (row, column + 2), self, isCastleMove=True))

    def getQueenSideCastleMoves(self, row, column, moves, allyColor):
        """

        :param row:
        :param column:
        :param moves:
        :param allyColor:
        :return:
        """

        if self.ChessBoard[row][column - 1] == "--" and self.ChessBoard[row][column - 2] == "--" \
                and self.ChessBoard[row][column - 3]:
            if not self.squareUnderAttack(row, column - 1) and not self.squareUnderAttack(row, column - 2):
                moves.append(Move((row, column), (row, column - 2), self, isCastleMove=True))

    def updateCastleRights(self, move: Move):
        """
        Updates castling rights after a user selected move.

        :param move: The user selected move.
        :return: None
        """

        # Check if the moved piece is a White or Black King or Rook.
        if move.movedPiece == "WR":
            if move.startRow == 7:
                # Check if the moved piece is on the King or Queen side.
                if move.startColumn == 0:
                    self.currentCastleRight.WQs = False

                elif move.startColumn == 7:
                    self.currentCastleRight.WKs = False

        elif move.movedPiece == "BR":
            if move.startRow == 0:
                # Check if the moved piece is on the King or Queen side.
                if move.startColumn == 0:
                    self.currentCastleRight.BQs = False

                elif move.startColumn == 7:
                    self.currentCastleRight.BKs = False

        elif move.movedPiece == "WK":
            self.currentCastleRight.WKs = False
            self.currentCastleRight.WQs = False

        elif move.movedPiece == "BK":
            self.currentCastleRight.BKs = False
            self.currentCastleRight.BQs = False
