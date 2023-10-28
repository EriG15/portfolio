# Name: Erik Griswold
# File: Breakout.py

"""
This program implements the Breakout game
"""

from pgl import GWindow, GOval, GRect, GLabel
import random

# Constants
GWINDOW_WIDTH = 360                     # Width of the graphics window
GWINDOW_HEIGHT = 600                    # Height of the graphics window
N_ROWS = 10                             # Number of brick rows
N_COLS = 10                             # Number of brick columns
BRICK_ASPECT_RATIO = 4 / 1              # Width to height ratio of a brick
BRICK_TO_BALL_RATIO = 3 / 1.5           # Ratio of brick width to ball size
BRICK_TO_PADDLE_RATIO = 2 / 3           # Ratio of brick to paddle width
BRICK_SEP = 2                           # Separation between bricks (in pixels)
TOP_FRACTION = 0.1                      # Fraction of window above bricks
BOTTOM_FRACTION = 0.05                  # Fraction of window below paddle
N_BALLS = 3                             # Number of balls (lives) in a game
TIME_STEP = 10                          # Time step in milliseconds
INITIAL_Y_VELOCITY = 3.0                # Starting y velocity downwards
MIN_X_VELOCITY = 1.0                    # Minimum random x velocity
MAX_X_VELOCITY = 3.0                    # Maximum random x velocity

# Derived Constants
BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS
BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO
PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO
PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO
PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT
BALL_DIAMETER = BRICK_WIDTH / BRICK_TO_BALL_RATIO

# Additional constants
COLORS = ["Red",
          "Orange",
          "Green",
          "Cyan",
          "Blue"]
TOP_Y = GWINDOW_HEIGHT * TOP_FRACTION
HALF_PADDLE_WIDTH = PADDLE_WIDTH // 2
PADDLE_START = GWINDOW_WIDTH // 2 - HALF_PADDLE_WIDTH


# Function: breakout
def breakout():
    """The main program for the Breakout game."""

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)

    # function for making brick
    def make_brick(color, x, y):
        brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
        brick.set_filled(True)
        brick.set_color(color)
        gw.add(brick, x, y)

    # making grid of bricks
    for i in range(N_ROWS):
        for j in range(N_COLS):
            make_brick(COLORS[i%10//2], 
                       BRICK_SEP * (j + 1) + BRICK_WIDTH * j , 
                       TOP_Y + i * (BRICK_HEIGHT + BRICK_SEP))

    # adding paddle
    paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle.set_filled(True)
    gw.add(paddle, PADDLE_START, PADDLE_Y)

    # making paddle move
    def move_paddle(coor):
        new_x = coor.get_x() - HALF_PADDLE_WIDTH
        if new_x < 0:
            paddle.set_location(0, PADDLE_Y)
        elif new_x + PADDLE_WIDTH > GWINDOW_WIDTH:
            paddle.set_location(GWINDOW_WIDTH - PADDLE_WIDTH, PADDLE_Y)
        else:
            paddle.set_location(new_x, PADDLE_Y)
    gw.add_event_listener("mousemove", move_paddle)

    # adding ball
    ball = GOval(BALL_DIAMETER, BALL_DIAMETER)
    ball.set_filled(True)
    gw.add(ball, 
           GWINDOW_WIDTH / 2 - BALL_DIAMETER / 2, 
           GWINDOW_HEIGHT / 2 - BALL_DIAMETER / 2)

    # getting ball to move and bounce
    gw.vx = random.uniform(MIN_X_VELOCITY, 
                           MAX_X_VELOCITY)
    if random.uniform(0,1) < 0.5:
        gw.vx = -gw.vx
    gw.vy = INITIAL_Y_VELOCITY

    # variables for animation
    gw.moving = False
    gw.spare_balls = N_BALLS - 1
    gw.brick_n = N_ROWS * N_COLS

    begin_message = GLabel("Begin!", 0,45)
    begin_message.set_color("#000000")
    begin_message.set_font("bold 35pt 'serif'")

    losing_message = GLabel("You lost!", 0,45)
    losing_message.set_color("#000000")
    losing_message.set_font("bold 35pt 'serif'")

    winning_message = GLabel("You won!", 0,45)
    winning_message.set_color("#000000")
    winning_message.set_font("bold 35pt 'serif'")

    def animation():
        # for animating ball
        if gw.moving == True:

            # setting bounds for the ball
            if ball.get_x() <= 0 or ball.get_x() >= GWINDOW_WIDTH - BALL_DIAMETER:
                gw.vx = -gw.vx
            if ball.get_y() <= 0: 
                gw.vy = -gw.vy
            
            # if game is won
            if gw.brick_n == 0:
                try:
                    gw.add(winning_message)
                except:
                    pass
                return

            # adding or renewing ball
            if ball.get_y() >= GWINDOW_HEIGHT - BALL_DIAMETER:
                if gw.spare_balls > 0:
                    gw.moving = False
                    gw.spare_balls -= 1
                    gw.vx = random.uniform(MIN_X_VELOCITY, MAX_X_VELOCITY)
                    if random.uniform(0,1) < 0.5:
                        gw.vx = -gw.vx
                    ball.set_location(GWINDOW_WIDTH / 2 - BALL_DIAMETER / 2, GWINDOW_HEIGHT / 2 - BALL_DIAMETER / 2)
                    return
                # if game is lost
                else:
                    try:
                        gw.add(losing_message)
                    except:
                        pass
                    return
            
            # moving ball
            ball.move(gw.vx, gw.vy)

            # variables for paddle / brick detection
            ball_x = ball.get_x()
            ball_y = ball.get_y()

            top_left = gw.get_element_at(ball_x, ball_y)
            top_right = gw.get_element_at(ball_x + BALL_DIAMETER, ball_y)
            bottom_left = gw.get_element_at(ball_x, ball_y + BALL_DIAMETER)
            bottom_right = gw.get_element_at(ball_x + BALL_DIAMETER, ball_y + BALL_DIAMETER)

            # paddle mechanics
            if bottom_left == paddle and bottom_right == paddle: # top
                if gw.vy > 0:
                        gw.vy = -gw.vy
            elif top_left == paddle and top_right == paddle: # bottom
                if gw.vy > 0:
                        gw.vy = -gw.vy
            elif bottom_left == paddle or top_left  == paddle: # left
                if gw.vy > 0:
                        gw.vy = -gw.vy
                if gw.vx < 0:
                        gw.vx = -gw.vx
            elif bottom_right == paddle or top_right == paddle: # right
                if gw.vy > 0:
                        gw.vy = -gw.vy
                if gw.vx > 0:
                        gw.vx = -gw.vx
            
            # brick mechanics
            else:
                if top_left != None:
                    if top_right != None: # top
                        gw.remove(top_right)
                        gw.brick_n -= 1
                        gw.vy = -gw.vy
                    elif bottom_left != None: # left
                        gw.remove(bottom_left)
                        gw.brick_n -= 1
                        gw.vx = -gw.vx
                    else: # top left
                        gw.remove(top_left)
                        gw.brick_n -= 1
                        if gw.vy < 0:
                            gw.vy = -gw.vy
                        if gw.vx < 0:
                            gw.vx = -gw.vx
                elif top_right != None:
                    if bottom_right != None: # right
                        gw.remove(bottom_right)
                        gw.brick_n -= 1
                        gw.vx = -gw.vx
                    else: # top right
                        gw.remove(top_right)
                        gw.brick_n -= 1
                        if gw.vy < 0:
                            gw.vy = -gw.vy
                        if gw.vx > 0:
                            gw.vx = -gw.vx
                elif bottom_right != None:
                    if bottom_left != None: # bottom
                        gw.remove(bottom_left)
                        gw.brick_n -= 1
                        gw.vy = -gw.vy
                    else: # bottom right
                        gw.remove(bottom_right)
                        gw.brick_n -= 1
                        if gw.vy > 0:
                            gw.vy = -gw.vy
                        if gw.vx > 0:
                            gw.vx = -gw.vx
                elif bottom_left != None: # bottom left
                    gw.remove(bottom_left)
                    gw.brick_n -= 1
                    if gw.vy > 0:
                        gw.vy = -gw.vy
                    if gw.vx < 0:
                        gw.vx = -gw.vx

    gw.set_interval(animation,TIME_STEP)
    
    # initiation function
    def initiate(coor):
        if gw.moving == False and gw.brick_n > 0:
            gw.moving = True

            # begin message
            def begin_clear():
                gw.remove(begin_message)
            if gw.spare_balls == 2:
                try:
                    gw.add(begin_message)
                except:
                    pass
                gw.set_timeout(begin_clear, 2000)
    
    gw.add_event_listener("click", initiate)

# Startup code
if __name__ == "__main__":
    breakout()