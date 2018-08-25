import math

# window size stuff
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700
# how big the tiles are. ideally matches the image size
TILE_SIZE = 20
# FPS limit
FPS_LIMIT = 30
# create a 2D array; X_MAX and Y_MAX values are altered to account for indices starting at 0
# this way the X_MAX and Y_MAX values are the maximum values in range for the board
X_MAX, Y_MAX = math.floor(WINDOW_WIDTH/TILE_SIZE) - 1, math.floor(WINDOW_HEIGHT/TILE_SIZE) - 1
board = [[None for i in range(Y_MAX + 1)] for j in range(X_MAX + 1)]
# the list of all particles currently on the board
particles = []
# how many frames until the selection menu starts to fade
MENU_DUR = FPS_LIMIT * 1
# how fast the selection menu fades (alpha / frame)
FADE_SPEED = 5