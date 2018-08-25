import random
import pygame
from globals import *

"""
    helper function to move particles on the board (swaps the two spots)
    p_to_move is the particle to be moved
    d_x is the change in the particle's x position
    d_y is the change in the particle's y position
"""
def move(p_to_move, d_x, d_y):
    global board
    x_0, y_0 = p_to_move.pos[0], p_to_move.pos[1] # get starting positions
    #print("particle at ", x_0, y_0, " moving by ", d_x, d_y)
    board[x_0][y_0], board[x_0+d_x][y_0+d_y] = board[x_0+d_x][y_0+d_y], board[x_0][y_0] # in-place swap
    if isinstance(board[x_0][y_0], Particle): # if the other spot swapped is a particle
        board[x_0][y_0].set_pos((x_0, y_0)) # update that particle's position
    p_to_move.set_pos((x_0+d_x, y_0+d_y))


class Particle:
    def __init__(self, p_pos, image_name):
        self.image = pygame.image.load(image_name)
        self.pos = (p_pos[0], p_pos[1])

    def set_pos(self, new_pos):
        self.pos = new_pos

    def update(self):
        return

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0]*TILE_SIZE,self.pos[1]*TILE_SIZE))


class Solid (Particle):
    def __init__(self, p_pos, image_name):
        Particle.__init__(self, p_pos, image_name)
    
    """
        updates the particle's position on the board
        pile_angle determines how steep the particles can pile up
        fluid_drift determines how likely the particle is to drift when falling through liquids
    """
    def update_solid(self, pile_angle=1, fluid_drift=5):
        xPos, yPos = self.pos[0], self.pos[1]
        # check the lower bounds for falling downwards
        if yPos == Y_MAX:
            return
        # particle can fall straight down
        if board[xPos][yPos+1] == None:
            move(self, 0, 1)
            return
        # particle is on a solid
        if isinstance(board[xPos][yPos+1], Solid):
            # whether or not moving to either side is valid (in bounds and not walled off)
            l_empty = xPos > 0 and not isinstance(board[xPos-1][yPos], Solid)
            r_empty = xPos < X_MAX and not isinstance(board[xPos+1][yPos], Solid)
            # now check for each side being submerged
            l_sub = xPos > 0 and isinstance(board[xPos-1][yPos], Liquid)
            r_sub = xPos < X_MAX and isinstance(board[xPos+1][yPos], Liquid)
            # now set the pile angle for each side. if that side is submerged, the pile angle is doubled
            l_pile = pile_angle * 2 if l_sub else pile_angle
            r_pile = pile_angle * 2 if r_sub else pile_angle
            # now we check for what sides the particle may fall to
            fall_choice = [-1, 1] # list for possible fall directions. start by assuming both sides are valid
            if l_empty == False: # first check left side
                fall_choice.remove(-1) # if the left side isn't empty, remove the option to fall left
            else: # if it is empty, check the pile angle on the left side
                for i in range(1, l_pile + 1): # go down the left side searching for a solid
                    if yPos+i > Y_MAX: # if we reach this, we've passed the bottom of the board and no solids have been found
                        fall_choice.remove(-1)
                        break
                    if isinstance(board[xPos-1][yPos+i], Solid): # if a solid is found, add -1 to possible fall directions
                        fall_choice.remove(-1)
                        break
            if r_empty == False: # same logic as falling to the left
                fall_choice.remove(1)
            else:
                for i in range(1, r_pile + 1):
                    if yPos+i > Y_MAX:
                        fall_choice.remove(1)
                        break
                    if isinstance(board[xPos+1][yPos+i], Solid):
                        fall_choice.remove(1)
                        break
            # if fall_choice is still empty, then the particle can't fall to either side
            if len(fall_choice) == 0:
                return
            # else, we need to choose a direction to fall
            move(self, random.choice(fall_choice), 1)
            return
        # particle is falling through a liquid
        if isinstance(board[xPos][yPos+1], Liquid):
            # roll for fluid drift
            if random.choice(range(fluid_drift + 1)) == 0: # particle drifts
                drift_choice = [] # possible drift directions. start by assuming the particle can't drift
                # check for walls on either side one block down
                if xPos > 0 and isinstance(board[xPos-1][yPos+1], Liquid):
                    drift_choice.append(-1)
                if xPos < X_MAX and isinstance(board[xPos+1][yPos+1], Liquid):
                    drift_choice.append(1)
                # now move the particle
                if len(drift_choice) == 0: # can't drift
                    move(self, 0, 1)
                else: # can drift
                    move(self, random.choice(drift_choice), 1)
            else: # particle doesn't drift
                move(self, 0, 1)
                return
            

class Liquid (Particle):
    def __init__(self, p_pos, image_name):
        Particle.__init__(self, p_pos, image_name)

    """
        update this particle's position on the board
        visc_timer
        visc_rand
        returns True if particle's timer should reset, False if time should only decrement
    """
    def update_liquid(self, visc_timer=0, visc_rand=0):
        xPos, yPos = self.pos[0], self.pos[1]
        if yPos < Y_MAX and board[xPos][yPos+1] == None: # particle can fall straight down
            move(self, 0, 1)
            return True # reset visc_timer
        else: # liquid is on top of another particle or at bottom of screen
            # whether or not moving to either side is valid (in bounds and empty)
            l_empty = xPos > 0 and board[xPos-1][yPos] == None
            r_empty = xPos < X_MAX and board[xPos+1][yPos] == None
            # whether or not falling to either side is valid
            l_fall = l_empty and yPos < Y_MAX and board[xPos-1][yPos+1] == None
            r_fall = r_empty and yPos < Y_MAX and board[xPos+1][yPos+1] == None
            # create list of possible ways liquid can move
            move_choice = []
            if l_fall == True:
                move_choice.append((-1, 1))
            elif l_empty == True:
                move_choice.append((-1, 0))
            if r_fall == True:
                move_choice.append((1, 1))
            elif r_empty == True:
                move_choice.append((1, 0))
            # choose which way the particle moves
            if len(move_choice) == 0: # no ways for particle to move
                return True
            if random.choice(range(visc_timer + visc_rand + 1)) == 0: # roll for movement. add 1 to range because of how range works
                movement = random.choice(move_choice) # temp variable for movement choice
                move(self, movement[0], movement[1])
                return True
            else:
                return False

        
class Dirt (Solid):
    def __init__(self, p_pos):
        Solid.__init__(self, p_pos, "images/dirt.png")
    
    def update(self):
        self.update_solid(pile_angle=1, fluid_drift=3)


class Stone (Solid):
    def __init__(self, p_pos):
        Solid.__init__(self, p_pos, "images/stone.png")
    
    def update(self):
        self.update_solid(pile_angle=3, fluid_drift=10)


class Metal (Solid):
    def __init__(self, p_pos):
        Solid.__init__(self, p_pos, "images/metal.png")
    
    def update(self):
        # metal doesn't do anything (yet)
        return


class Water (Liquid):
    def __init__(self, p_pos):
        Liquid.__init__(self, p_pos, "images/water.png")
        self.max_timer = 2 # value to reset timer to
        self.timer = self.max_timer # timer that works with viscosity

    def update(self):
        if self.update_liquid(visc_timer=self.timer, visc_rand=0) == True:
            self.timer = self.max_timer
        elif self.timer > 0:
            self.timer -= 1


class Slime (Liquid):
    def __init__(self, p_pos):
        Liquid.__init__(self, p_pos, "images/slime.png")
        self.max_timer = 0 # value to reset timer to
        self.timer = self.max_timer # timer that works with viscosity

    def update(self):
        if self.update_liquid(visc_timer=self.timer, visc_rand=7) == True:
            self.timer = self.max_timer
        elif self.timer > 0:
            self.timer -= 1
