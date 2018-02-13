import pygame

# initial game variables
window_width_height = (1200, 300)
background_color = (255, 255, 255)
screen = pygame.display.set_mode(window_width_height)
game_running = True

# attributes for the game things to be rendered
paddle_color = (255, 50, 50)
wall_color = (40, 50, 30)
paddle_width = 10
paddle_height = 30

wall_width = window_width_height[0]
wall_height = window_width_height[1] * 0.1 # May have an error with float in an int space

paddle_Xoffset = 0.05 * window_width_height[0]
paddle_Yoffset =  0.5 * window_width_height[1]
# initial game things to be rendered

paddle1 = pygame.Rect((paddle_Xoffset, paddle_Yoffset, paddle_width, paddle_height))
paddle2 = pygame.Rect((window_width_height[0] - paddle_Xoffset, paddle_Yoffset, paddle_width, paddle_height))
wall1 = pygame.Rect((0, 0, wall_width, wall_height))
wall2 = pygame.Rect((0, window_width_height[1] - wall_height, wall_width, wall_height))
delay = 0
while game_running:

    events = pygame.event.get()
    for event in events:

        # Quit scenarios
        if event.type == pygame.QUIT:
                game_running = False

    keys = pygame.key.get_pressed()
    delay += 1
    if keys[pygame.K_ESCAPE]:
        game_running = False
    if keys[pygame.K_UP] and delay > 10 and not paddle1.colliderect(wall1):
        paddle1 = paddle1.move(0, -1)
        delay = 0
    if keys[pygame.K_DOWN] and delay > 10 and not paddle1.colliderect(wall2):
        paddle1 = paddle1.move(0, 1)
        delay = 0

    if keys[pygame.K_w] and delay > 10  and not paddle2.colliderect(wall1):
        paddle2 = paddle2.move(0, -1)
        delay = 0
    if keys[pygame.K_s] and delay > 10 and not paddle2.colliderect(wall2):
        paddle2 = paddle2.move(0, 1)
        delay = 0

    # Rendering game stuff
    screen.fill(background_color)
    screen.fill(paddle_color, paddle1)
    screen.fill(paddle_color, paddle2)
    screen.fill(wall_color, wall1)
    screen.fill(wall_color, wall2)
    pygame.display.flip()


pygame.quit()