import pygame
import math

class movement_info():
    def __init__(self, v0, a0):
        self.velocity_x = v0
        self.velocity_y = v0
        self.acceleration_x = a0
        self.acceleration_y = a0

        # maybe add an ID to this

class rect_info():
    # Rect info class
    def __init__(self, x, y, width, height, color):
        # global tracking ID, so every rect does not have the same numbering
        global ID_number
        # Basic rect properties
        self.obj_x = x
        self.obj_y = y
        self.width = width
        self.height = height
        self.color = color
        # Make sure that this structure can be identified as a Rect for the renderer, etc.
        self.ID = "Rect" + str(ID_number)
        ID_number += 1
        self.movement = movement_info(0, 1)

# Any other class besides the Rect class is required to have a non-Rect name for an ID and have a collision rect inside
class ball_info():
    def __init__(self, x, y, radius, color):
        global ID_number
        # Basic circle properties
        self.obj_x = x
        self.obj_y = y
        self.radius = radius
        self.color = color
        # The rect x and y coordinates used for collisions
        x_prime = math.sqrt(2) / 2.0 * radius
        y_prime = x_prime
        # Collision rect info for the circle
        self.rect_info = rect_info(int(self.obj_x - x_prime), int(self.obj_y - y_prime),
                                   int(2 * x_prime), int(2 * y_prime) , color)

        # An ID that allows other functions to know that this is a ball object for rendering, collision, etc.
        self.ID = "Ball" + str(ID_number)
        ID_number+= 1
        self.movement = movement_info(0, 1)

# TODO implement collision  options: use the pythoageron thereom (regular shapes), bitmap + (irregular shapes)minkowsi based collision
# Movement functions
def move_up(object_renderer_info):
    # limit to acceleration
    if abs(object_renderer_info.movement.velocity_y) < 10:  # car speed max
        object_renderer_info.movement.velocity_y -= object_renderer_info.movement.acceleration_y

def stop_up(object_renderer_info):
    object_renderer_info.movement.velocity_y += 1 # constant slow down

def stop_down(object_renderer_info):
    object_renderer_info.movement.velocity_y -= 1 # constant slow down

def move_down(object_renderer_info):
    if object_renderer_info.movement.velocity_y < 10:  # car speed max
        object_renderer_info.movement.velocity_y += object_renderer_info.movement.acceleration_y

# Currently there is no max speed for a ball.

def move_right(object_renderer_info):
    object_renderer_info.obj_x += 1

def move_left(object_renderer_info):
    object_renderer_info.obj_x -= 1

# Handle key input and movement
def handle_keys_and_movement(renderers):

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Paddle 1 acceleration
    if keys[pygame.K_w]:
        move_up(renderers["paddle1"])
    elif renderers["paddle1"].movement.velocity_y < 0:
        stop_up(renderers["paddle1"])

    if keys[pygame.K_s]:
        move_down(renderers["paddle1"])
    elif renderers["paddle1"].movement.velocity_y > 0:
        stop_down(renderers["paddle1"])

    # Paddle 2 controls
    if keys[pygame.K_UP]:
        move_up(renderers["paddle2"])
    elif renderers["paddle2"].movement.velocity_y < 0:
        stop_up(renderers["paddle2"])

    if keys[pygame.K_DOWN]:
        move_down(renderers["paddle2"])
    elif renderers["paddle2"].movement.velocity_y > 0:
        stop_down(renderers["paddle2"])
    # Paddle 2 controls
    if keys[pygame.K_LEFT]:
        move_left(renderers["paddle2"])

    # movement loop
    for renderer in renderers:
        if "Rect" in renderers[renderer].ID:
            renderers[renderer].obj_y += renderers[renderer].movement.velocity_y
            renderers[renderer].obj_x += renderers[renderer].movement.velocity_x
        else:
            renderers[renderer].obj_y += renderers[renderer].movement.velocity_y
            renderers[renderer].obj_x += renderers[renderer].movement.velocity_x
            renderers[renderer].rect_info.obj_y += renderers[renderer].movement.velocity_y
            renderers[renderer].rect_info.obj_x += renderers[renderer].movement.velocity_x
    # TODO create ball movement increment
    # TODO possibly add the paddle

def detect_collisions(renderers):
    """
    Detects any collisions between the renderers that are to be shown and returns a dict of objects that are colliding

    :param renderers:
    :return:
    """

    # TODO add in extra data about the collisions, so the collision resolution can do something about it -> or just have it take the velocity or offset to do this?
    # brainstorm -> keep track of the velocity and do something to do it -> transformations and everything to that value and the acceleration, etc.
    # This will be crazy to figure out how to do momentum transfer etc. This might be complicated to put together. How do we want to put this together??
    # It might be fun to use alternate forms of those equations.. etc.
    # brainstorm, check for the collision and note the collisions then determine what to do with it.
    # This will cause problems if the object is moving too fast and the object looks to the program to be on the other side then it will bounce off in the wrong direction

    renderer_keys = list(renderers.keys())
    num_renderers = len(renderer_keys)
    collisions = {}

    """
    Code Comment Block 000 -> goes through the renderers for collision in a manner which doesn't redo collision checks
    """
    # Start Code Comment Block 000
    for render_number, renderer_key in enumerate(renderer_keys):
        renderer = renderers[renderer_key]
        if 'Rect' in renderer.ID:
            rect1 = pygame.Rect((renderer.obj_x, renderer.obj_y, renderer.width, renderer.height))
        else:
            rect1 = pygame.Rect((renderer.rect_info.obj_x, renderer.rect_info.obj_y, renderer.rect_info.width,
                                 renderer.rect_info.height))

        for check_number in range(render_number + 1, num_renderers):
            # End Code Comment Block 000
            """
            Code Comment Block 001 -> does collision detection using pygame rects
            """
            renderer2 = renderers[renderer_keys[check_number]]
            if 'Rect' in renderer2.ID:
                rect2 = pygame.Rect((renderer2.obj_x, renderer2.obj_y, renderer2.width, renderer2.height))
            else:
                rect2 = pygame.Rect((renderer2.rect_info.obj_x, renderer2.rect_info.obj_y, renderer2.rect_info.width, renderer2.rect_info.height))
            # Start Code Comment Block 001
            # Determine if colliding
            if rect1.colliderect(rect2):
                # add a key for it, and add a list of collisions
                print("Collisions detected")
                if renderer_key not in collisions:
                    collisions[renderer_key] = [renderer_keys[check_number]]
                else:
                    collisions.append(renderer_keys[check_number])
                if renderer_keys[check_number] not in collisions:
                    collisions[renderer_keys[check_number]] = [renderer_key]
                else:
                    collisions[renderer_key].append([renderer_keys[check_number]])

                # End Code Comment Block 001
    return collisions

def handle_collisions(renderers, collisions):
    # Resolve collision
    # TODO create something to handle collisions with ball with ball
    # TODO create something to handle collisions with rect with rect
    # TODO create something to handle collisions with ball and rect
    for collision1 in collisions:
        # renderers[collision1].obj_x = -renderers[collision1].movement.velocity_x
        # renderers[collision1].obj_y = -renderers[collision1].movement.velocity_y
        # renderers[collision1].movement.velocity_y = -renderers[collision1].movement.velocity_y
        # renderers[collision1].movement.velocity_x = -renderers[collision1].movement.velocity_x
        for collision2 in collisions[collision1]:

            # Moves us out of the collision
            renderers[collision2].obj_x -= renderers[collision2].movement.velocity_x
            renderers[collision2].obj_y -= renderers[collision2].movement.velocity_y
            # Makes us go in the opposite direction
            renderers[collision2].movement.velocity_y = -renderers[collision2].movement.velocity_y
            renderers[collision2].movement.velocity_x = -renderers[collision2].movement.velocity_x

            # Ball logic to impart speed/velocity from paddle/walls to ball
            if "Rect" not in renderers[collision2].ID:
               renderers[collision2].movement.velocity_y += renderers[collision1].movement.velocity_y
               renderers[collision2].movement.velocity_x += renderers[collision1].movement.velocity_x

        # move the collision object back the other way if it is the one moving

    # want some sense of momentum transfer?
    # want the velocity and acceleration to work together
    # bounce angles

# Initialize the game
pygame.init()

# Initialize the initial screen size, and set the colors
width_height_screen = (1200, 300)
screen = pygame.display.set_mode(width_height_screen)
background_color = (255, 255, 255)
paddle_color = (25, 20, 100)
wall_color = (40,50,10)

# Set the rects dimensions
paddle_width = .01 * width_height_screen[0]
paddle_height = .10 * width_height_screen[1]
wall_width = width_height_screen[0]
wall_height = 0.2 * width_height_screen[1]

# Global ID number that is part of the entity IDs (not really entities)
ID_number = 0

circle_radius = 10

# Initial coordinates that tells us where the game things (intentionally not objects) [I'm experimenting with functional programming]
# The paddle and wall initial coordinates are only one set rather than two because of symmetry in opposing things.
paddle_y = 0.5 * width_height_screen[1]
paddle_x = 0.1 * width_height_screen[0]
wall_x = 0
wall_y = 0

circleXpos = int(width_height_screen[0] / 2.0)
circleYpos = int(width_height_screen[1] / 2.0)

# Make the data structs for rendering, input, and movement logic
paddle1 = rect_info(paddle_x, paddle_y, paddle_width, paddle_height, paddle_color)
paddle2 = rect_info(width_height_screen[0] - paddle_x - paddle_width, paddle_y, paddle_width, paddle_height, paddle_color)

wall1 = rect_info(wall_x, wall_y, wall_width, wall_height, wall_color)
wall2 = rect_info(wall_x, width_height_screen[1] - wall_height - wall_y, wall_width, wall_height, wall_color)

ball1 = ball_info(circleXpos, circleYpos, circle_radius, paddle_color)

ball1.movement.velocity_x = 1

# Dict of info to renderer each time
renderers = {'paddle1':paddle1, 'paddle2':paddle2, 'wall1':wall1, 'wall2':wall2, 'ball': ball1}

# Clock - only for FPS for now
clock = pygame.time.Clock()

# Game loop boolean
game_is_running = True

fps = 30
time_tick_interval = 1.0 / fps

# Main game loop
while game_is_running:

    # Handle events queue
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_is_running = False
    # Handle input and movement for now
    handle_keys_and_movement(renderers)

    # Detect collisions
    collisions = detect_collisions(renderers)

    # Handle collisions with appropiate logic
    handle_collisions(renderers, collisions)

    # Fill in the background of the screen for now - can fill it in with different backgrounds if need be/ conditions are met.
    screen.fill(background_color)

    # Render everything on the screen
    for dict_key in renderers.keys():
        renderer = renderers[dict_key]
        # Rect renderer condition
        if 'Rect' in renderer.ID:
            screen.fill(renderer.color, pygame.Rect((renderer.obj_x, renderer.obj_y, renderer.width, renderer.height)))
        # Ball renderer condition
        elif "Ball" in renderer.ID:
            pygame.draw.circle(screen, renderer.color, (renderer.obj_x, renderer.obj_y), renderer.radius)

    # Push the updates to the screen
    pygame.display.flip()
    # Keep this clock ticking for 30 fps
    clock.tick(fps)


# Close the game
pygame.quit()
