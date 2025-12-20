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
YELLOW = (255, 255, 0)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    """Represents the player's spaceship."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        # NEW: Add shooting cooldown
        self.shoot_delay = 250 # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        """Update the player's position and handle shooting."""
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed_x = 5
        
        self.rect.x += self.speed_x

        # Keep the player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # NEW: Handle shooting
        self.shoot()

    def shoot(self):
        """Create a bullet if the cooldown has passed."""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# NEW: The Bullet class
class Bullet(pygame.sprite.Sprite):
    """Represents a bullet fired by the player."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        """Move the bullet up the screen."""
        self.rect.y += self.speed_y
        # Kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# --- Initialize Pygame and Create Window ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# --- Sprite Groups ---
all_sprites = pygame.sprite.Group()
# NEW: A group just for bullets, useful for collision detection later
bullets = pygame.sprite.Group()

# --- Create Game Objects ---
player = Player()
all_sprites.add(player)

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()