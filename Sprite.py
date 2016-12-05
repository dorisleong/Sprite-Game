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
from math import sin, cos, pi, atan2
import pygame
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
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

        self.image = pygame.Surface([15, 15])
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
        if self.rect.top <= 30:
            self.rect.top = 30
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

        self.rect.x += self.change_x
        self.rect.y += self.change_y

# referenced code: https://gist.github.com/iminurnamez/9abb72c3e43309cb6098


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

# for i in range(10):
#     # This represents a block
#     block = Block(D_RED)

#     # Set a random location for the block
#     block.rect.x = random.randrange(SCREEN_WIDTH)
#     block.rect.y = random.randrange(30, SCREEN_HEIGHT - 50)

#     # Add the block to the list of objects
#     block_list.add(block)
#     all_sprites_list.add(block)

# Create a red player block
player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
all_sprites_list.add(player)

# Create enemy
enemy = Enemy((200, 200), player.getPlayerPos())
enemy_list.add(enemy)


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
lives = 3

spawn_timer = 1000
max_followers = 5
max_blocks = 20

player.rect.x = SCREEN_WIDTH / 2
player.rect.y = SCREEN_HEIGHT / 2

SHOOT_EVENT = pygame.USEREVENT + 1
ENEMY_SPAWN_EVENT = pygame.USEREVENT + 2
STUCK_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(pygame.USEREVENT + 2, spawn_timer)
x, y = 0, 0

moveLeft = False
moveRight = False
moveUp = False
moveDown = False
game_over = False
stuck = False
font = pygame.font.Font(None, 20)
large_font = pygame.font.Font(None, 48)
display_instructions = True
instruction_page_image = pygame.image.load("Instructions.png").convert()
instruction_page = 1
level_2_reached = False
level_3_reached = False
level_4_reached = False
level_5_reached = False


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

while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            instruction_page += 1
            if instruction_page == 2:
                display_instructions = False

    # Set the screen background
    screen.blit(instruction_page_image, [0, 0])

    if instruction_page == 1:
        # Draw instructions, page 1
        # This could also load an image created in another program.
        # That could be both easier and more flexible.

        text = font.render("Instructions", True, WHITE)
        screen.blit(text, [10, 10])

        text = font.render("Page 1", True, WHITE)
        screen.blit(text, [10, 40])

    if instruction_page == 2:
        # Draw instructions, page 2
        text = font.render("This program bounces a rectangle", True, WHITE)
        screen.blit(text, [10, 10])

        text = font.render("Page 2", True, WHITE)
        screen.blit(text, [10, 40])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            done = True

        # Restart game with space if game over
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_over:
                    game_over = False
                    score = 0
                    lives = 3
                    spawn_timer = 1000
                    max_followers = 5
                    max_blocks = 10
                    level_2_reached = False
                    level_3_reached = False
                    level_4_reached = False
                    level_5_reached = False
                    pygame.time.set_timer(pygame.USEREVENT + 2, spawn_timer)
                    enemy_list.empty()
                    block_list.empty()
                    bullet_list.empty()
                    all_sprites_list.empty()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    all_sprites_list.add(player)
                    player.rect.x = SCREEN_WIDTH / 2
                    player.rect.y = SCREEN_HEIGHT / 2

        # Fire a bullet if the user clicks the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            shoot(m_pos)
            pygame.time.set_timer(pygame.USEREVENT + 1, 100)

        if event.type == SHOOT_EVENT:
            m_pos = pygame.mouse.get_pos()
            shoot(m_pos)

        if event.type == STUCK_EVENT:
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            stuck = False

        if event.type == ENEMY_SPAWN_EVENT:
            # Spawn enemies that follow
            if len(enemy_list) < max_followers:
                close = True
                while close:
                    random_pos = (random.randrange(SCREEN_WIDTH),
                                  random.randrange(30, SCREEN_HEIGHT - 50))
                    x_distance_to_player = abs(random_pos[0] - player.rect.x)
                    y_distance_to_player = abs(random_pos[1] - player.rect.y)
                    if x_distance_to_player > 100 and y_distance_to_player > 100:
                        close = False
                enemy = Enemy(random_pos, player.getPlayerPos())
                enemy_list.add(enemy)
            # Spawn stationary enemies
            if len(block_list) < max_blocks:
                close = True
                while close:
                    random_pos = (random.randrange(SCREEN_WIDTH),
                                  random.randrange(30, SCREEN_HEIGHT - 50))
                    x_distance_to_player = abs(random_pos[0] - player.rect.x)
                    y_distance_to_player = abs(random_pos[1] - player.rect.y)
                    if x_distance_to_player > 50 and y_distance_to_player > 50:
                        close = False
                block = Block(PURPLE)
                block.rect.x = random_pos[0]
                block.rect.y = random_pos[1]
                block_list.add(block)
                all_sprites_list.add(block)

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
        if stuck:
            player.changespeed(0, 0)
        else:
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
    if not game_over:

        # Call the update() method on all the sprites
        all_sprites_list.update()
        enemy_list.update(player.getPlayerPos())
        # Calculate mechanics for each bullet
        for bullet in bullet_list:

            # See if it hit a block or enemy
            block_hit_list = pygame.sprite.spritecollide(
                bullet, block_list, True)
            enemy_hit_list = pygame.sprite.spritecollide(
                bullet, enemy_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                all_sprites_list.remove(block)
                #score += 1
                print("Stationary killed -> ", score)

            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 10
                print("Follower killed -> ", score)

            # Remove the bullet if it flies off the screen
            if bullet.rect.y < -10 or bullet.rect.y > SCREEN_HEIGHT + 10 or bullet.rect.x < -10 or bullet.rect.x > SCREEN_WIDTH + 10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        if pygame.sprite.spritecollideany(player, enemy_list) != None:
            pygame.time.wait(500)
            print("Player was hit by follower!")
            enemy_list.remove(
                pygame.sprite.spritecollideany(player, enemy_list))
            lives -= 1
            if lives == 0:
                print("GAME OVER")
                # show game over screen
                game_over = True
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)

        if pygame.sprite.spritecollideany(player, block_list) != None:
            print("Player hit a stationary enemy!")
            hit_block = pygame.sprite.spritecollideany(player, block_list)
            block_list.remove(hit_block)
            all_sprites_list.remove(hit_block)
            stuck = True
            pygame.time.set_timer(pygame.USEREVENT + 3, 500)

        if not level_2_reached and score >= 100:
            print("---------LEVEL 2---------")
            level_2_reached = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 750)
        elif not level_3_reached and score >= 250:
            print("---------LEVEL 3---------")
            level_3_reached = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 500)
        elif not level_4_reached and score >= 500:
            print("---------LEVEL 4---------")
            level_4_reached = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 300)
            max_blocks = 40
        elif not level_5_reached and score >= 1000:
            print("---------LEVEL 5---------")
            level_5_reached = True
            pygame.time.set_timer(pygame.USEREVENT + 2, 200)

    # --- Draw a frame

    # Clear the screen
    screen.fill(WHITE)

    # draw bar on top
    pygame.draw.rect(screen, GRAY, [0, 0, 800, 30])
    display_score = font.render("Score: " + str(score), True, BLACK)
    screen.blit(display_score, [10, 10])

    display_lives = font.render("Lives: x" + str(lives), True, BLACK)
    screen.blit(display_lives, [725, 10])

    # Draw all the spites
    all_sprites_list.draw(screen)
    enemy_list.draw(screen)

    if game_over:
        display_game_over = large_font.render("GAME OVER", True, BLACK)
        screen.blit(display_game_over, [300, 250])
        restart = font.render("Press space to restart", True, BLACK)
        screen.blit(restart, [330, 350])
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
