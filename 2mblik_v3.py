import pygame, random

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 1080, 1080
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mukikaka")
test_font = pygame.font.Font(None, 32)
game_active = True

player_surface = pygame.image.load("graphics/player_small.png").convert_alpha()
player_surface = pygame.transform.scale(player_surface, (20, 20)) 
player_surface.set_colorkey((255,255,255,255))  
player_rect = player_surface.get_rect(center=(100,100))

score_surf = pygame.font.Font(None, 32).render("Score: 0", False, "white")
score_surf = score_surf.get_rect(center=(400,50))
score_rect = test_font.render("Score: 0", False, "white").get_rect(center=(50,20))

enemy_surface = pygame.image.load("graphics/enemy_small.png").convert_alpha()
enemy_surface = pygame.transform.scale(enemy_surface, (60, 60))
enemy_surface.set_colorkey((255,255,255,255))   
enemy_rect = enemy_surface.get_rect(center=(100,100))

food_surface = pygame.image.load("graphics/food_small.png").convert_alpha()
food_surface = pygame.transform.scale(food_surface, (60, 60))
food_surface.set_colorkey((255,255,255,255))
food_rect = food_surface.get_rect(center=(100,100))

game_over_surf = test_font.render("Game Over", False, "white")
game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

restart_surf = test_font.render("Restart Game", False, "white")
restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

# Load resources
def load_resources():
    ground_surface = pygame.image.load("graphics/ground.jpg").convert()
    player_surface = pygame.image.load("graphics/player_small.png").convert_alpha()
    return ground_surface, player_surface

# Handle player input
def handle_input(player_pos, dt): 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt 
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

class Enemy:
    def __init__(self):
        self.radius = 20                                                                            
        self.color = (0, 0, 0)                                                                    
        self.position = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) 
        self.velocity = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))                
        self.surface = enemy_surface

    def update(self):
        self.position += self.velocity 
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= WIDTH:
            self.velocity.x = -self.velocity.x
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= HEIGHT:
            self.velocity.y = -self.velocity.y

    def draw(self):
        enemy_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, self.surface.get_rect(center=self.position))

    def reset_position(self):
        self.position = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))


class Food:
    def __init__(self):
        self.radius = 20
        self.color = (255, 0, 0)
        self.position = pygame.Vector2(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))     
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))                    
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)
        self.surface = food_surface

    def update(self):
        self.position += self.velocity
        self.rect = pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= WIDTH:
            self.velocity.x = -self.velocity.x
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= HEIGHT:
            self.velocity.y = -self.velocity.y

    def draw(self):
        food_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, food_rect)

# Main game loop
def main():
    global game_active
    clock = pygame.time.Clock()
    ground_surface, player_surface = load_resources()
    player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    player_rect = player_surface.get_rect(center=player_pos)
    
    enemies = [Enemy() for _ in range(10)]
    food_items = [Food() for _ in range(10)]

    running = True

    score = 0
    score_surf = test_font.render(f"Score: {score}", False, "white")
    score_rect = score_surf.get_rect(center=(50,20))

    def reset_enemies_position():
        for enemy in enemies:
            enemy.reset_position()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        dt = clock.tick(FPS) / 1000
        handle_input(player_pos, dt)

        if not game_active:
            screen.blit(game_over_surf, game_over_rect)
            screen.blit(restart_surf, restart_rect)

            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] == 1:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    game_active = True
                    reset_enemies_position()
                elif game_over_rect.collidepoint(mouse_pos):
                    game_active = True
                    exit()

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
                pygame.quit()


        if game_active:
            for enemy in enemies:
                enemy.update()
            for food_item in food_items:
                food_item.update()

            screen.fill(BLACK)
            screen.blit(ground_surface, (0, 0))
            # pygame.draw.rect(screen, RED, (50, 50, 20, 50))
            
            for enemy in enemies:
                enemy.draw()
            for food_item in food_items:
                food_item.draw()
            
            enemies[0].rect = pygame.Rect(enemies[0].position.x, enemies[0].position.y, enemies[0].radius, enemies[0].radius)
            food_items[0].rect = pygame.Rect(food_items[0].position.x, food_items[0].position.y, food_items[0].radius, food_items[0].radius)
            player_rect.center = player_pos
            food_items[0].rect = pygame.Rect(food_items[0].position.x, food_items[0].position.y, food_items[0].radius, food_items[0].radius)
            
            for enemy in enemies:
                enemy.rect = pygame.Rect(enemy.position.x - enemy.radius, enemy.position.y - enemy.radius, enemy.radius * 2, enemy.radius * 2) 
                if player_rect.colliderect(enemy.rect): 
                    print("Player collided with enemy")
                    game_active = False

            for food_item in food_items:
                if player_rect.colliderect(food_item.rect):
                    print("Player collided with food")
                    score += 1
                    score_surf = test_font.render(f"Score: {score}", False, "white")
                    food_items.remove(food_item)
                    food_items.append(Food())

                    score_rect = test_font.render(f"Score: {score}", False, "white").get_rect(center=(50, 50))
                    score_rect = score_rect.move(0, 50)

            screen.blit(player_surface, player_rect)
            screen.blit(score_surf, score_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
