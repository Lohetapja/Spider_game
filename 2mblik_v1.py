import pygame


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 1080)) # width, height
pygame.display.set_caption("Mukikaka")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 32) # font, size
running = True # 
dt = 0

width = 1080
height = 1080

screen_res = (width, height)
red = (255, 0, 0)
black = (0, 0, 0)

ball_obj = pygame.draw.circle(surface=screen, color=black, center=[100, 100], radius=40, )
# define speed of ball
# speed = [X direction speed, Y direction speed]
speed = [10, 10]

# test_surface = pygame.Surface((100, 100))
ground_surface = pygame.image.load("graphics/ground.jpg").convert()
text_surface = test_font.render("Hello", False, "white")
# enemy_surface = pygame.image.load("graphics/enemy.jpg").convert()
player_surfase = pygame.image.load("graphics/player.jpg").convert_alpha()
# player_rect = player_surfase.get_rect(center = (x,y))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_obj = ball_obj.move(speed)                    
    
    screen.blit(ground_surface, (0, 0)) # draw the surface to the screen at position (0, 0)
    screen.blit(text_surface, (100, 100))
    # screen.blit(player_surfase, (player_surfase, player_rect))
    
    # screen.blit(enemy_surface, (100, 100))
    
    if ball_obj.left <= 0 or ball_obj.right >= width:
        speed[0] = -speed[0] #
    if ball_obj.top <= 0 or ball_obj.bottom >= height:
        speed[1] = -speed[1]
 
    # draw ball at new centers that are obtained after moving ball_obj
    pygame.draw.circle(surface=screen, color=red,center=ball_obj.center, radius=40)

    pygame.draw.circle(screen, "red", player_pos, 20)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()