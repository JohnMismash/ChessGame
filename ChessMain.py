# John (Jack) Mismash
# 5/7/2021

# This ChessMain file will display the current game state and handle any user input.

import pygame as p
from ChessEngine import Game

# Width/Height of the chess board.
# Resolution can be set to higher with a Width/Height of 400.
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

# Initialize the dictionary of Images. We can now access any piece image with IMAGES['WP']
# for example and each string is represented as the key in our dictionary.
def loadPieceImages():
    piece_images = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK', 'BP', 'BR', 'BN', 'BB', 'BQ', 'BK']

    # Loads each piece image into our global dictionary of pieces. This will also scale each image to
    # the respective square size of our board.
    for piece in piece_images:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/Pieces/" + piece + ".png"),
                                          (SQUARE_SIZE, SQUARE_SIZE))


# This is the main driver for the Chess Game and handle any user input and updating the display of the game
# and its respective graphics.
def main():
    # Creates a console with the specific width and height.
    console = p.display.set_mode((WIDTH, HEIGHT))

    # Create a clock that will run to check for events.
    game_clock = p.time.Clock()

    console.fill(p.Color("white"))

    # Create a "blank" game state that will allow for all the pieces to be in their
    # respective starting position.
    game_state = Game()

    # Load the images into the global variable so they are accessible. This is only called once
    # in the program.
    loadPieceImages()

    # Draw the initial game board and pieces.
    drawGame(console, game_state, False, None, None)

    # Checks if the console has been closed.
    game_is_running = True

    current_square = ()  # Tuple -> (row, column)
    selected_squares = []  # List of player clicks -> [(row, column), (row, column)]
    isPieceSelected = False
    highlightedSquareRow = None
    highlightedSquareColumn = None

    while game_is_running:
        for event in p.event.get():

            if event.type == p.QUIT:
                game_is_running = False

            # If there is a event where a mouse is clicked, we can capture the (x, y)
            # coordinates of where the mouse was clicked.
            elif event.type == p.MOUSEBUTTONDOWN:

                click_location = p.mouse.get_pos()

                # Since our x,y coordinates are now stored in an array, we can access this array
                # and capture the row and column respective to where they clicked.
                # NOTE: Each row and column will start at zero, unlike a representation of an actual chess board.
                click_column = click_location[0] // SQUARE_SIZE
                click_row = click_location[1] // SQUARE_SIZE

                # If the piece has already been selected, we do not want to say this is a valid move,
                # so we can set our selected square variable to be empty to signify a deselection of the piece.
                # Otherwise, we can update the current square that has been selected as normal.
                if current_square != (click_row, click_column):
                    current_square = (click_row, click_column)
                    highlightedSquareRow = click_row
                    highlightedSquareColumn = click_column
                    isPieceSelected = True

                    # Keeps track of the first and second clicks that a player makes.
                    selected_squares.append(current_square)

                else:
                    current_square = ()
                    selected_squares = []
                    highlightedSquareRow = None
                    highlightedSquareColumn = None

                # If the user has made a valid second click to a new square, we want to now
                # perform this valid move within the Chess game.
                if len(selected_squares) == 2:
                    if game_state.processMove(selected_squares[0], selected_squares[1]):
                        current_square = ()
                        selected_squares = []
                        highlightedSquareRow = None
                        highlightedSquareColumn = None

                    else:
                        # Invalid Move: game_state and move_log is not updated.
                        pass

        if isPieceSelected:
            drawGame(console, game_state, True, highlightedSquareRow, highlightedSquareColumn)
            game_clock.tick(MAX_FPS)
            p.display.flip()

        else:
            drawGame(console, game_state, False, None, None)
            game_clock.tick(MAX_FPS)
            p.display.flip()


# This will draw everything to the console, including the squares and the pieces.
def drawGame(console, game_state, isSquareSelected, highlightedSquareRow, highlightedSquareColumn):

    if isSquareSelected:
        drawBoardHighlight(console, highlightedSquareRow, highlightedSquareColumn)

    else:
        drawBoard(console)

    drawPieces(console, game_state.ChessBoard)


# This will draw the squares of the Chess Board.
def drawBoard(console):
    # These colors may be changed to be any color scheme of the users choice.
    square_colors = [p.Color("white"), p.Color("dark orange")]

    # We know that every board setup will always have a "light" square in the top left corner,
    # regardless of the perspective of white/black.

    # We can also set up our square_colors to that the access to a light color is at the 0 index, and the access
    # to a dark color is the 1 index.
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            # When we add the row and column number and mod by 2, we will know whether that
            # position should be a light or dark square if there is a remainder or not, and we can use this
            # remainder of 0 or 1 to access our colors.
            square_color = square_colors[(row + column) % 2]

            # Draw the square given the respective position and color.
            p.draw.rect(console, square_color, (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# This will draw the squares of the Chess Board.
def drawBoardHighlight(console, highlightedSquareRow, highlightedSquareColumn):
    # These colors may be changed to be any color scheme of the users choice.
    square_colors = [p.Color("white"), p.Color("dark orange")]

    # We know that every board setup will always have a "light" square in the top left corner,
    # regardless of the perspective of white/black.

    # We can also set up our square_colors to that the access to a light color is at the 0 index, and the access
    # to a dark color is the 1 index.
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            # When we add the row and column number and mod by 2, we will know whether that
            # position should be a light or dark square if there is a remainder or not, and we can use this
            # remainder of 0 or 1 to access our colors.

            if row == highlightedSquareRow and column == highlightedSquareColumn:
                square_colors = [p.Color("red"), p.Color("red")]
                square_color = square_colors[(row + column) % 2]

                # Draw the square given the respective position and color.
                p.draw.rect(console, square_color, (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                square_colors = [p.Color("white"), p.Color("dark orange")]

            else:
                square_color = square_colors[(row + column) % 2]

                # Draw the square given the respective position and color.
                p.draw.rect(console, square_color, (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# This will draw the initial setup of the pieces on the board.
def drawPieces(console, ChessBoard):
    # Since we know the initial setup of the board, we can access each piece on the board, and draw the
    # respective piece image.
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = ChessBoard[row][column]

            if piece != "--":
                piece_image = IMAGES[piece]
                console.blit(piece_image, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# This will flip the view of the board to represent the switching of turns.
def flipBoard(game_state):
    pass


if __name__ == "__main__":
    main()
