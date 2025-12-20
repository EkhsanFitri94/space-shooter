# src/main.py

import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    """Represents the player's spaceship."""
    def __init__(self):
        super().__init__() # Always call the parent class (Sprite) constructor first
        self.image = pygame.Surface((50, 40)) # Create a blank image surface
        self.image.fill(GREEN) # Fill it with green color
        self.rect = self.image.get_rect() # Get the rectangle of the image for positioning
        self.rect.centerx = SCREEN_WIDTH / 2 # Position it at the center bottom of the screen
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        """Update the player's position based on key presses."""
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed_x = 5
        
        # Update the rect's position
        self.rect.x += self.speed_x

        # Keep the player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# --- Initialize Pygame and Create Window ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()

# --- Create Game Objects ---
player = Player()
all_sprites.add(player)

# --- Game Loop ---
running = True
while running:
    # Keep loop at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update() # This will call the update() method of every sprite in the group

    # Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen) # This will draw the image of every sprite at its rect's position

    # Flip the display to show your new frame
    pygame.display.flip()

pygame.quit()
sys.exit()