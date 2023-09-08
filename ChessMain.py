# John (Jack) Mismash
# 3/14/23

import pygame as p
import ChessEngine
import ChessAI

# Width/Height of the chess board.
WIDTH = HEIGHT = 512

# Dimensions of a chess board are 8x8.
DIMENSION = 8

# Each individual Square size with floor division.
SQUARE_SIZE = HEIGHT // DIMENSION

# Maximum FPS for animation of the pieces.
MAX_FPS = 15

# Dictionary of Images for the Chess game.
IMAGES = {}

# Initialize our pyGame globally, so no methods will rely on this anywhere else in the program.
p.init()

piece_images = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK', 'BP', 'BR', 'BN', 'BB', 'BQ', 'BK']

global squareColors


def loadPieceImages():
    """
    Initializes the Chess piece images, and scales each image to the respective square size of the Chess board.
    """

    for piece in piece_images:
        path = "Chess/Pieces/" + piece + ".png"
        IMAGES[piece] = p.transform.scale(p.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))


def drawGame(console, gameState, validMoves, highlightedSquare):
    """
    Draws the board squares, pieces and square highlighting to the console.

    :param console: The current game console.
    :param gameState: The current game state.
    :param validMoves: The current list of valid moves.
    :param highlightedSquare:
    :return: None
    """

    drawBoard(console)
    highlightSquares(console, gameState, validMoves, highlightedSquare)
    drawPieces(console, gameState.ChessBoard)


# This will draw the squares of the Chess Board.
def drawBoard(console):
    """
    Draws the board squares to the console.

    :param console: The current game console.
    :return: None
    """

    # These colors may be changed to be any color scheme of the users choice.
    global squareColors
    squareColors = [p.Color("white"), p.Color("gray")]

    # We know that every board setup will always have a "light" square in the top left corner,
    # regardless of the perspective of white/black.
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            squareColor = squareColors[(row + column) % 2]

            # Draw the square given the respective square position and square color.
            p.draw.rect(console, squareColor, (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# This will draw the initial setup of the pieces on the board.
def drawPieces(console, ChessBoard):
    """
    Draws the chess pieces to the console.

    :param console: The current game console.
    :param ChessBoard: The current representation of the Chess board.
    :return: None
    """

    # Since we know the initial setup of the board, we can access each piece on the board, and draw the
    # respective piece image.
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = ChessBoard[row][column]

            if piece != "--":
                piece_image = IMAGES[piece]
                console.blit(piece_image, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def animateMove(console, move, gameState, clock):
    """
    Draws the animation of moving a piece.

    :param console: The current game console.
    :param move:
    :param gameState:
    :param clock:
    :return: None
    """

    global squareColors

    deltaRow = move.endRow - move.startRow
    deltaColumn = move.endColumn - move.startColumn

    # Frames to move one square.
    framesPerSquare = 10
    frameCount = framesPerSquare * (abs(deltaRow) + abs(deltaColumn))

    for frame in range(frameCount + 1):
        row, column = (move.startRow + deltaRow * frame / frameCount,
                       move.startColumn + deltaColumn * frame / frameCount)

        drawBoard(console)
        drawPieces(console, gameState.ChessBoard)
        color = squareColors[((move.endRow + move.endColumn) % 2)]
        endSquare = p.Rect(move.endColumn * SQUARE_SIZE, move.endRow * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(console, color, endSquare)

        if move.capturedPiece != "--":
            console.blit(IMAGES[move.capturedPiece], endSquare)

        # Draw moving piece.
        console.blit(IMAGES[move.movedPiece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(console, message):
    """
    Draws the end-game text to the console.

    :param console: The current game console.
    :param message: The specific end-game message to draw (Checkmate, Stalemate or a Draw).
    :return: None
    """

    font = p.font.SysFont("Helvetica", 32, True, False)
    textObj = font.render(message, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObj.get_width() / 2,
                                                    HEIGHT / 2 - textObj.get_height() / 2)
    console.blit(textObj, textLocation)

    textObj = font.render(message, 0, p.Color("Red"))
    console.blit(textObj, textLocation.move(2, 2))


def highlightSquares(console, gameState, validMoves, sqSelected):
    """
    Highlights a selected piece square blue, and its available move square(s) yellow.
    Assumes that the square selected is occupied by a piece.

    :param console: The current game console.
    :param gameState: The current game state.
    :param validMoves: The current list of valid moves.
    :param sqSelected: The user selected square.
    """

    if sqSelected != ():
        row, column = sqSelected

        # Check if the square selected is the correct colored piece based on the current players turn.
        if gameState.ChessBoard[row][column][0] == ('W' if gameState.whiteToMove else 'B'):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))

            # Set transparency value.
            s.set_alpha(100)

            # Set square color.
            s.fill(p.Color('blue'))
            console.blit(s, (column * SQUARE_SIZE, row * SQUARE_SIZE))

            # Highlight all available moves from that square.
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startColumn == column:
                    console.blit(s, (move.endColumn * SQUARE_SIZE, move.endRow * SQUARE_SIZE))


def main():
    """
    Main driver method for the Chess game.
    Handles user input, display updating, and respective graphics.
    """

    # Creates a console with the specific width and height.
    console = p.display.set_mode((WIDTH, HEIGHT))
    console.fill(p.Color("white"))

    # Create a clock that will run to check for events.
    gameClock = p.time.Clock()

    gameState = ChessEngine.ChessGame()

    # Returns a list of valid moves at the beginning of the game.
    validMoves = gameState.getValidMovesAdvanced()

    # Flag variable for when a move is made.
    moveMade = False

    # Flag variable for when a animation is needed.
    animate = False

    # Load the images into the global variable so they are accessible. This is only called once
    # in the program.
    loadPieceImages()

    # Checks if the console has been closed.
    gameIsRunning = True

    currentSquare = ()
    selectedSquares = []

    # Draw the initial game board and pieces.
    drawGame(console, gameState, validMoves, currentSquare)

    gameOver = False

    # True if a human is playing white, False if AI is playing white.
    playerOne = False

    # True is a human is playing black, False if AI is playing black.
    playerTwo = True

    while gameIsRunning:
        # Determine if it is a player's turn or the AI's turn
        isHumanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)

        for event in p.event.get():
            if event.type == p.QUIT:
                gameIsRunning = False

            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver and isHumanTurn:
                    # If the mouse is clicked, we can capture the (x, y) coordinates of where was clicked.
                    clickLocation = p.mouse.get_pos()

                    # NOTE: Each row and column will start at zero, unlike a representation of an actual chess board.
                    click_column = clickLocation[0] // SQUARE_SIZE
                    click_row = clickLocation[1] // SQUARE_SIZE

                    # Check if the square has been selected.
                    if currentSquare != (click_row, click_column):
                        currentSquare = (click_row, click_column)

                        # Keeps track of the first and second clicks that a player makes.
                        selectedSquares.append(currentSquare)

                    else:
                        # Empty values represent a non-selection.
                        currentSquare = ()
                        selectedSquares = []

                    # If the user has made a valid second click to a new square, we want to now
                    # perform this valid move within the Chess game.
                    if len(selectedSquares) == 2:
                        move = ChessEngine.Move(selectedSquares[0], selectedSquares[1], gameState)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                # Allows the game to process the move generated by the engine, not the player.
                                gameState.processMove(validMoves[i])

                                print("Move Made: ")

                                for move in gameState.moveLog:
                                    print(move.getChessNotation())

                                currentSquare = ()
                                selectedSquares = []

                                moveMade = True
                                animate = True

                        # Assumes that a second selection of a piece is a deselection, or if a invalid move is made,
                        # the second square selected becomes the first.
                        if not moveMade:
                            selectedSquares = [currentSquare]

            elif event.type == p.KEYDOWN:
                # When the 'z' key is pressed, undo the move.
                if event.key == p.K_z:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                # When the 'r' key is pressed, reset the game.
                if event.key == p.K_r:
                    gameState = ChessEngine.ChessGame()
                    validMoves = gameState.getValidMovesAdvanced()

                    currentSquare = ()
                    selectedSquares = []

                    moveMade = False
                    animate = False
                    gameOver = False

        # Let the AI find next move if it is not a humans turn.
        if not gameOver and not isHumanTurn:
            move = ChessAI.findBestMove(gameState, validMoves)

            if move is None:
                move = ChessAI.findRandomMove(validMoves)

            gameState.processMove(move)
            moveMade = True
            animate = True

        # If a move was just made, we now want to update the list of possible valid moves.
        if moveMade:
            if animate:
                animateMove(console, gameState.moveLog[-1], gameState, gameClock)

            validMoves = gameState.getValidMovesAdvanced()
            moveMade = False

        drawGame(console, gameState, validMoves, currentSquare)

        if gameState.checkmate:
            gameOver = True

            if gameState.whiteToMove:
                drawText(console, "Black wins by checkmate!")

            else:
                drawText(console, "White wins by checkmate!")

        elif gameState.stalemate:
            gameOver = True
            drawText(console, "Draw by stalemate!")

        gameClock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
