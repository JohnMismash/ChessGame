# John (Jack) Mismash
# 3/15/23

"""
This ChessAI file will control the AI moves made by the computer.
"""

import random
from ChessEngine import Move
from ChessEngine import ChessGame

materialValues = {"K": 0,  # King
                  "Q": 9,  # Queen
                  "R": 5,  # Rook
                  "N": 3,  # Knight
                  "B": 3,  # Bishop
                  "P": 1}  # Pawn

CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(validMoves):
    """
    Generates a random move by the computer.

    :param validMoves: The list of current valid moves by the computer.
    :return: The random move generated.
    """

    index = random.randint(0, len(validMoves) - 1)
    return validMoves[index]


def findBestMoveGreedy(gameState, validMoves):
    """
    Generates a move given that the computer is only interested in the move that gains the most materialistic value.

    :param gameState: The current game state.
    :param validMoves: The list of current valid moves by the computer.
    :return bestMove: The best (greedy) move generated.
    :rtype: Move
    """

    turnMultiplier = 1 if gameState.whiteToMove else -1

    # Set the MAX score to be negative, Black is attempting maximize their score,
    # while White is trying to minimize their score.
    maxScore = -CHECKMATE

    bestMove: Move = None

    # Process each move and identify the highest scoring move possible.
    for playerMove in validMoves:
        gameState.processMove(playerMove)

        if gameState.checkmate:
            score = CHECKMATE

        elif gameState.stalemate:
            score = STALEMATE

        else:
            score = turnMultiplier * scoreBoard(gameState.ChessBoard)

        if score > maxScore:
            maxScore = score
            bestMove = playerMove

        gameState.undoMove()

    return bestMove


def findBestMove(gameState: ChessGame, validMoves):
    """

    :param gameState:
    :type: ChessGame
    :param validMoves:
    :return:
    """

    turnMultiplier = 1 if gameState.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None

    random.shuffle(validMoves)

    # Process each move,
    for playerMove in validMoves:
        gameState.processMove(playerMove)
        opponentsMoves = gameState.getValidMovesAdvanced()

        if gameState.stalemate:
            opponentMaxScore = STALEMATE

        elif gameState.checkmate:
            opponentMaxScore = -CHECKMATE

        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentsMoves:
                gameState.processMove(opponentMove)
                gameState.getValidMovesAdvanced()
                if gameState.checkmate:
                    score = -turnMultiplier * CHECKMATE

                elif gameState.stalemate:
                    score = STALEMATE

                else:
                    score = -turnMultiplier * scoreBoard(gameState.ChessBoard)

                if score > opponentMaxScore:
                    opponentMaxScore = score

                gameState.undoMove()

        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove

        gameState.undoMove()

    return bestPlayerMove


def findBestMoveMinMax(gameState, validMoves):
    pass


def scoreBoard(board):
    """
    Returns the score based on the given board state, where White pieces count as positive materialistic
    value, and Black pieces count as negative materialistic value.
    Scoring is only based on materialistic values specified globally.

    :param board: The current board game state.
    :return: The current materialistic score of the game.
    """

    score = 0

    for row in board:
        for square in row:
            if square[0] == 'W':
                score += materialValues[square[1]]
            elif square[0] == 'B':
                score -= materialValues[square[1]]

    return score
