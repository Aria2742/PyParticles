import pygame
from globals import *
from particles import *

# list of all images used for drawing the menu
images = [
    pygame.image.load('images/dirt.png'),
    pygame.image.load('images/stone.png'),
    pygame.image.load('images/metal.png'),
    pygame.image.load('images/water.png'),
    pygame.image.load('images/slime.png')
]
# selected particle and values for menu fade
selected = 0
timer = 0
alpha = 0


# convert all the images to surfaces to allow for changing the alpha
def convert_images():
    global images
    temp = []
    for img in images:
        temp.append(img.convert())
    images = temp


# draws the menu showing what particle is currently selected
def draw_menu(screen):
    global timer
    global alpha
    # set the positions of the images
    base_x, base_y = pygame.mouse.get_pos()
    pos = [
        (base_x - (2.5 * TILE_SIZE) - 20, base_y - (2 * TILE_SIZE)),
        (base_x - (1.5 * TILE_SIZE) - 10, base_y - (2 * TILE_SIZE)),
        (base_x - (0.5 * TILE_SIZE), base_y - (2 * TILE_SIZE)),
        (base_x + (0.5 * TILE_SIZE) + 10, base_y - (2 * TILE_SIZE)),
        (base_x + (1.5 * TILE_SIZE) + 20, base_y - (2 * TILE_SIZE))
    ]
    # select the images to draw
    to_draw = []
    for i in range(5):
        to_draw.append(images[(selected - 2 + i) % len(images)])
    # set the alpha then check the alpha timer
    for image in to_draw:
        image.set_alpha(alpha)
    if timer > 0:
        timer -= 1
    if timer == 0:
        alpha -= FADE_SPEED
        # set the timer lower than zero (to stop reducing the alpha), and make sure the alpha isn't less than zero
        if alpha <= 0:
            alpha = 0
            timer = -1
    # draw the images for the menu
    for i in range(5):
        screen.blit(to_draw[i], pos[i])


# select the particle to the left of the currently selected particle
def shift_left():
    shift_selected(-1)


# select the particle to the right of the currently selected particle
def shift_right():
    shift_selected(1)


# select the particle x positions from the currently selected particle
def shift_selected(x):
    global selected
    selected += x
    selected = selected % len(images)
    # reset the timer and the alpha value
    global timer
    timer = MENU_DUR
    global alpha
    alpha = 255


# create a new particle on the board and append it to the global list of particles
def new_particle(pos):
    # check that the spot is empty
    if board[pos[0]][pos[1]] != None:
        return
    # create the particle
    p = None
    if selected == 0:
        p = Dirt(pos)
    elif selected == 1:
        p = Stone(pos)
    elif selected == 2:
        p = Metal(pos)
    elif selected == 3:
        p = Water(pos)
    elif selected == 4:
        p = Slime(pos)
    else: # should never happen
        print('ERROR: Selected particle value out of range!')
    board[pos[0]][pos[1]] = p
    particles.append(p)