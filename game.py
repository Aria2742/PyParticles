import math
import pygame
from globals import *
from particles import *
import selector

# define a main function
def main():
    global board
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Particle Sandbox") # set the window name
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # create a surface on screen
    selector.convert_images() # convert the selection menu images

    timer = pygame.time.Clock() # create a clock for limiting the FPS
    running = True # sentinel for main game loop
   
    """
    # fill the bottom of the screen with a certain particle (water in the case)
    for i in range(X_MAX+1):
        for j in range(Y_MAX-10, Y_MAX+1):
            new_particle('4', (i, j), particles)
    """

    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if window is closed, then end the main loop
                running = False
            if event.type == pygame.KEYDOWN: # if a key is pressed, figure out which key
                select(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN: # mouse scrolling handled here
                if event.button == 4:
                    selector.shift_right()
                elif event.button == 5:
                    selector.shift_left()
        m_press = pygame.mouse.get_pressed() # get the pressed mouse buttons
        if m_press[0] == True and m_press[2] == True:
            pass
        elif m_press[0] == True: # left click, place
            selector.new_particle(pos_to_grid(pygame.mouse.get_pos()))
        elif m_press[2] == True: # right click, remove
            rm_pos = pos_to_grid(pygame.mouse.get_pos())
            rm_part = board[rm_pos[0]][rm_pos[1]]
            if rm_part in particles: # if particle is in list, remove it
                particles.remove(rm_part)
                board[rm_pos[0]][rm_pos[1]] = None
        # image drawing
        screen.fill((0, 0, 0))
        # draw the particles
        for p in particles:
            p.draw(screen)
        # draw the selector menu
        selector.draw_menu(screen)
        # wait for the FPS timer, then flip the screen to update it
        timer.tick(FPS_LIMIT)
        pygame.display.flip()
        # after drawing, update the particles
        for p in particles:
            p.update()
            """
            # slow down time between each solid particle update in order to see whats happening
            if isinstance(p, Solid):
                screen.fill((0, 0, 0))
                for p in particles:
                    p.draw(screen)
                pygame.display.flip()
                timer.tick(10)
            """


def pos_to_grid(pos):
    return (math.floor(pos[0]/TILE_SIZE), math.floor(pos[1]/TILE_SIZE))


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()