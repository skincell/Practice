import pygame

# inits all the modules including the dsiplay mode to get the initial screen working as we see fit.
pygame.init()

# size of screen
width = 1100
height = 300

# flipping function to update display
screen = pygame.display.set_mode((width, height))

game_is_running = True

# initial setup
background_color = 255, 255,255
paddle1_color = 0,40,50
paddle2_color = 0,40,90

# objects
paddle1_width = 100
paddle2_width = 100
horizonal_offset = 50
vertical_offset = height / 5.0
paddle1 = pygame.Rect(horizonal_offset, vertical_offset, paddle1_width, paddle1_width)
# Some complex obtuse math that makes sure that the left corner coordinate and right corner coordinate are both on screen.
paddle2 = pygame.Rect( width - horizonal_offset - paddle2_width, vertical_offset, paddle2_width, paddle2_width)

wall_height = 40
wall1 = pygame.Rect(0, 0, width, wall_height)
wall2 = pygame.Rect(0, height - wall_height, width, wall_height)
wall1_color = 20,50,100
wall2_color = 100,200,40

while game_is_running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_is_running = False

    screen.fill(background_color)
    screen.fill(paddle1_color, rect=paddle1)
    screen.fill(paddle2_color, rect=paddle2)
    screen.fill(wall1_color, rect=wall1)
    screen.fill(wall2_color, rect=wall2)
    # blit only works with images/surfaces
    pygame.display.flip()

pygame.quit()
