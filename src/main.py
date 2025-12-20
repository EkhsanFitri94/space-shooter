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
RED = (255, 0, 0)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed_x = 5
        
        self.rect.x += self.speed_x

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# --- Functions ---
# NEW: Function to start a new game
def new_game():
    global player, all_sprites, enemies, bullets, score, game_over

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create initial enemies
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Reset score and game state
    score = 0
    game_over = False

# --- Initialize Pygame and Create Window ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
# NEW: Font for drawing text
font_name = pygame.font.match_font('arial')
font = pygame.font.Font(font_name, 30)

# NEW: Global variables for game state
score = 0
game_over = False

# NEW: Start the first game
new_game()

# --- Game Loop ---
running = True
while running:
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # NEW: Check for restart key press
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r and game_over:
                new_game()

    # UPDATED: Only update game logic if the game is not over
    if not game_over:
        # Update
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10 # Increase score for each enemy destroyed
            # Spawn a new enemy to keep the challenge going
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # NEW: Check for player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True # Trigger game over

    # Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # NEW: Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # NEW: Draw game over screen if the game is over
    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        
        # Center the text
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 2 - 60))
        screen.blit(final_score_text, (SCREEN_WIDTH / 2 - final_score_text.get_width() / 2, SCREEN_HEIGHT / 2))
        screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() / 2, SCREEN_HEIGHT / 2 + 40))

    # Flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()