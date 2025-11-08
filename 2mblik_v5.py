import os
import sys
import random
from pathlib import Path
import pygame

# Mukikaka 🎮
#
# A tiny Pygame experiment revived from my first-ever game project. Built with a lot of curiosity and “vibe coding.”  
# 1080×1080, 60 FPS, simple controls, and a few home-made assets.


# ---------- Path handling: run from the script folder ----------
BASE_DIR = Path(__file__).parent.resolve()
os.chdir(BASE_DIR)  # force CWD → script folder (so relative paths work)

# ---------- Setup ----------
pygame.init()
WIDTH, HEIGHT = 1080, 1080
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Anette")
clock = pygame.time.Clock()

ui_font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

def load_image(path, size=None, colorkey=None):
    """Load image relative to CWD (already set to script folder)."""
    surf = pygame.image.load(path)
    # use convert_alpha when image supports alpha, otherwise convert (faster)
    if path.lower().endswith((".png", ".bmp", ".gif")):
        surf = surf.convert_alpha()
    else:
        surf = surf.convert()
    if size:
        surf = pygame.transform.smoothscale(surf, size)
    if colorkey is not None:
        surf.set_colorkey(colorkey)
    return surf

# ---------- Assets ----------
# Ground (fallback to plain black if not found)
try:
    ground_surface = load_image("graphics/ground.jpg")
    ground_surface = pygame.transform.smoothscale(ground_surface, (WIDTH, HEIGHT))
except Exception as e:
    print("[WARN] ground.jpg not found or failed to load:", e)
    ground_surface = pygame.Surface((WIDTH, HEIGHT))
    ground_surface.fill(BLACK)

player_img = load_image("graphics/player_small.png", (60, 60), (255, 255, 255))
enemy_img  = load_image("graphics/enemy_small.png",  (60, 60),  (255, 255, 255))
food_img   = load_image("graphics/food_small.png",   (60, 60),  (255, 255, 255))

game_over_text  = big_font.render("Game Over", True, WHITE)
restart_text    = ui_font.render("Press R to Restart, ESC to Quit", True, WHITE)

# ---------- Entities ----------
class Player:
    def __init__(self):
        self.image = player_img
        self.pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.speed = 300
        self.rect = self.image.get_rect(center=self.pos)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a]),
            (keys[pygame.K_s] - keys[pygame.K_w])
        )
        if move.length_squared() > 0:
            self.pos += move.normalize() * self.speed * dt
        # clamp to screen
        self.pos.x = max(0, min(WIDTH, self.pos.x))
        self.pos.y = max(0, min(HEIGHT, self.pos.y))
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.pos = pygame.Vector2(
            random.randint(60, WIDTH - 60),
            random.randint(60, HEIGHT - 60)
        )
        self.vel = pygame.Vector2(
            random.uniform(-200, 200),
            random.uniform(-200, 200)
        )
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.vel * dt
        # bounce
        if self.pos.x <= 0 or self.pos.x >= WIDTH:
            self.vel.x *= -1
        if self.pos.y <= 0 or self.pos.y >= HEIGHT:
            self.vel.y *= -1
        self.rect.center = self.pos

    def reset_position(self):
        self.pos.update(
            random.randint(60, WIDTH - 60),
            random.randint(60, HEIGHT - 60)
        )
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Food:
    def __init__(self):
        self.image = food_img
        self.pos = pygame.Vector2(
            random.randint(60, WIDTH - 60),
            random.randint(60, HEIGHT - 60)
        )
        self.vel = pygame.Vector2(
            random.uniform(-120, 120),
            random.uniform(-120, 120)
        )
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.vel * dt
        if self.pos.x <= 0 or self.pos.x >= WIDTH:
            self.vel.x *= -1
        if self.pos.y <= 0 or self.pos.y >= HEIGHT:
            self.vel.y *= -1
        self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# ---------- Game State ----------
def new_round():
    player = Player()
    enemies = [Enemy() for _ in range(10)]
    food = [Food() for _ in range(10)]
    score = 0
    return player, enemies, food, score

def draw_score(surface, score):
    surf = ui_font.render(f"Score: {score}", True, WHITE)
    rect = surf.get_rect(topleft=(16, 16))
    surface.blit(surf, rect)

def main():
    # Quick debug to verify we’re running the expected file/folder
    print("RUNNING:", __file__)
    print("CWD    :", os.getcwd())

    player, enemies, food_items, score = new_round()
    game_active = True

    while True:
        dt = clock.tick(FPS) / 1000.0

        # ----- Events -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if not game_active and event.key == pygame.K_r:
                    player, enemies, food_items, score = new_round()
                    game_active = True

        # ----- Update -----
        if game_active:
            player.handle_input(dt)
            for e in enemies:
                e.update(dt)
            for f in food_items:
                f.update(dt)

            # player vs enemies
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    game_active = False
                    break

            # player vs food (avoid mutating while iterating)
            new_food = []
            gained = 0
            for f in food_items:
                if player.rect.colliderect(f.rect):
                    gained += 1
                else:
                    new_food.append(f)
            if gained:
                score += gained
                for _ in range(gained):
                    new_food.append(Food())
            food_items = new_food

        # ----- Draw -----
        screen.blit(ground_surface, (0, 0))

        if game_active:
            for f in food_items:
                f.draw(screen)
            for e in enemies:
                e.draw(screen)
            player.draw(screen)
            draw_score(screen, score)
        else:
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            screen.blit(restart_text,    restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        pygame.display.flip()

if __name__ == "__main__":
    main()
