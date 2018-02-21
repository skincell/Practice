import pygame

# Checks which keys are pressed and does behavior on those

pygame.init()

width_height_screen = (1200, 300)
screen = pygame.display.set_mode(width_height_screen)
background_color = (255, 255, 255)
paddle_color = (25, 20, 100)
wall_color = (40,50,10)
# wall and paddle sizes
paddle_width = .01 * width_height_screen[0]
paddle_height = .10 * width_height_screen[1]
wall_width = width_height_screen[0]
wall_height = 0.2 * width_height_screen[1]

# starting locations
paddle_y = 0.5 * width_height_screen[1]
paddle_x = 0.1 * width_height_screen[0]
wall_x = 0
wall_y = 0

# had to think about the position coordinates for the longest time. Should be an easier way to have this in my brain
paddle1 = pygame.Rect((paddle_x, paddle_y, paddle_width, paddle_height))
paddle2 = pygame.Rect((width_height_screen[0] - paddle_x - paddle_width, paddle_y, paddle_width, paddle_height))

wall1 = pygame.Rect((wall_x, wall_y, wall_width, wall_height))
wall2 = pygame.Rect((wall_x, width_height_screen[1] - wall_height - wall_y, wall_width, wall_height))

collision_objects = [paddle1, paddle2, wall1, wall2]
movement_objects = [paddle1, paddle2]
counter = 0
circleXpos = int(width_height_screen[0] / 2.0)
circleYpos = int(width_height_screen[1] / 2.0)
circle = pygame.draw.circle(screen, paddle_color, (circleXpos,circleYpos), 10)
circle_velocity = -1
game_is_running = True
while game_is_running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_is_running = False


    keys = pygame.key.get_pressed()

    counter += 1

    # want to put a restriction on movement...
    # what about an if statement...
    # nah... what about a list of expected colliders

    # movement for paddle2
    if keys[pygame.K_w] and counter > 10 and not paddle2.colliderect(wall1):
        paddle2 = paddle2.move(0,-1)
    if keys[pygame.K_s] and counter > 10 and not paddle2.colliderect(wall2):
        paddle2 = paddle2.move(0,1)

    # movement for paddle1
    if keys[pygame.K_UP] and counter > 10 and not paddle1.colliderect(wall1):
        paddle1 = paddle1.move(0,-1)

    if keys[pygame.K_DOWN] and counter > 10 and not paddle1.colliderect(wall2):
        paddle1 = paddle1.move(0,1)

    if counter > 10 and not circle.colliderect(wall1) \
            and not circle.colliderect(wall2) \
            and not circle.colliderect(paddle1) and not circle.colliderect(paddle2):
        circle = circle.move(circle_velocity,0)
        circleXpos -= 1
    elif counter > 10:
        circle_velocity = -circle_velocity
        circle = circle.move(circle_velocity, 0)


    if counter > 10:
        counter = 0

    screen.fill(background_color)
    screen.fill(paddle_color, circle)
    pygame.draw.circle(screen, paddle_color, (circleXpos, circleYpos), 10)
    screen.fill(paddle_color, paddle1)
    screen.fill(wall_color, wall1)
    screen.fill(wall_color, wall2)
    screen.fill(paddle_color, paddle2)
    pygame.display.flip()

pygame.quit()