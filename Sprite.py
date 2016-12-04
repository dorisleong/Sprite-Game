"""
Author:  Doris Leong
CWID:  894269018
E-Mail:  dleong@csu.fullerton.edu
File Description:  Sprite.py contains all the code necessary for a
                   top down 2D shooter type game.
Credits:  Code is built upon examples from
          http://programarcadegames.com/
"""
import random
from math import sin, cos, pi, atan2, sqrt
import pygame
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self, x, y):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def getPlayerPos(self):
        return (self.rect.x, self.rect.y)

    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x = x
        self.change_y = y

    def update(self):
        """ Find a new position for the player"""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 20:
            self.rect.top = 20
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

        self.rect.x += self.change_x
        self.rect.y += self.change_y


class Enemy(pygame.sprite.Sprite):
    """ This class represents the Enemy. """

    def __init__(self, pos, target_pos):
        """ Place the enemy on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.angle = get_angle(self.pos, target_pos)

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.speed = 2.75

    def update(self, target_pos):
        """ Follow the player"""
        self.angle = get_angle(self.pos, target_pos)
        self.pos = project(self.pos, self.angle, self.speed)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set up the image for the bullet
        self.image = pygame.Surface([4, 4])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 7
        self.change_x = cos(angle) * velocity
        self.change_y = sin(angle) * velocity

    def update(self):
        """ Move the bullet. """

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Define some functions
def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)


def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))

# --- Create the window

# Initialize Pygame
pygame.init()

# Set the height and width of the screen

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# List of each enemy
enemy_list = pygame.sprite.Group()

# --- Create the sprites

for i in range(50):
    # This represents a block
    block = Block(GREEN)

    # Set a random location for the block
    block.rect.x = random.randrange(SCREEN_WIDTH)
    block.rect.y = random.randrange(SCREEN_HEIGHT - 50)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
all_sprites_list.add(player)

# Create enemy
enemy = Enemy((200, 200), player.getPlayerPos())
enemy.rect.x = 200
enemy.rect.y = 200
enemy_list.add(enemy)


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

player.rect.x = SCREEN_WIDTH / 2
player.rect.y = SCREEN_HEIGHT / 2

SHOOT_EVENT = pygame.USEREVENT + 1
x, y = 0, 0

moveLeft = False
moveRight = False
moveUp = False
moveDown = False


def shoot(pos):
    # Get the mouse position
    mouse_x = pos[0]
    mouse_y = pos[1]

    # Create the bullet based on where we are, and where we want to
    # go.
    bullet = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)

    # Add the bullet to the lists
    all_sprites_list.add(bullet)
    bullet_list.add(bullet)

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            done = True

        # Fire a bullet if the user clicks the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            shoot(m_pos)
            pygame.time.set_timer(pygame.USEREVENT + 1, 100)

        if event.type == SHOOT_EVENT:
            m_pos = pygame.mouse.get_pos()
            shoot(m_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)

        if event.type == KEYDOWN:
            if event.key in (K_UP, K_w):
                moveUp = True
            elif event.key in (K_DOWN, K_s):
                moveDown = True
            elif event.key in (K_LEFT, K_a):
                moveLeft = True
            elif event.key in (K_RIGHT, K_d):
                moveRight = True

        elif event.type == KEYUP:
            if event.key in (K_LEFT, K_a):
                moveLeft = False
            elif event.key in (K_RIGHT, K_d):
                moveRight = False
            elif event.key in (K_UP, K_w):
                moveUp = False
            elif event.key in (K_DOWN, K_s):
                moveDown = False

        if moveUp and moveLeft:
            player.changespeed(-2, -2)
        elif moveUp and moveRight:
            player.changespeed(2, -2)
        elif moveDown and moveLeft:
            player.changespeed(-2, 2)
        elif moveDown and moveRight:
            player.changespeed(2, 2)
        elif moveUp:
            player.changespeed(0, -3)
        elif moveDown:
            player.changespeed(0, 3)
        elif moveLeft:
            player.changespeed(-3, 0)
        elif moveRight:
            player.changespeed(3, 0)
        else:
            player.changespeed(0, 0)

    # --- Game logic

    # Call the update() method on all the sprites
    all_sprites_list.update()
    enemy_list.update(player.getPlayerPos())
    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        # Remove the bullet if it flies off the screen
        if bullet.rect.y < -10 or bullet.rect.y > SCREEN_HEIGHT + 10 or bullet.rect.x < -10 or bullet.rect.x > SCREEN_WIDTH + 10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # --- Draw a frame

    # Clear the screen
    screen.fill(WHITE)

    # Draw all the spites
    all_sprites_list.draw(screen)
    enemy_list.draw(screen)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
