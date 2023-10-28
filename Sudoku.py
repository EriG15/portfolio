# Name: Erik Griswold

"""
Replace this generic text with a description of what your submission
depicts or any guidelines I should have about how it works or operates
"""

# Now you are free to import whatever you need from pgl and take it from here!
# I'll be excited to see these!



from pgl import GWindow, GRect, GLabel
import random

# constants

GLABEL_GRID = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

GWINDOW_SIZE = 901
INSET = 50

GRID_SIZE = GWINDOW_SIZE - INSET * 2
SQUARE_SIZE = GRID_SIZE // 9
BLOCK_SIZE = GRID_SIZE // 3

GRID_COLOR = "#959595"
FILLED_SQUARE_COLOR = "#E1E1E1"
SELECT_COLOR = "#FFDA00"
FILLED_SELECT_COLOR = "#E6C500"

EASY_MODE = 38
MEDIUM_MODE = 30
HARD_MODE = 23

# gw variables
gw = GWindow(GWINDOW_SIZE,GWINDOW_SIZE)

gw.first_action = True
gw.highlighted = GRect(1,1,0,0)
gw.selected_is_const = True
gw.click_col = 0
gw.click_row = 0


# function for creating sudoku
def fill_window():
    
    # making 9x9 grid

    for i in range(9):
        for j in range(9): 

                square_fill = GRect(INSET + j * SQUARE_SIZE, INSET + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                square_fill.set_filled(True)      
                if gw.SUDOKU_GRID[j][i] != 0:
                    square_fill.set_color(FILLED_SQUARE_COLOR)
                else:
                    square_fill.set_color("#ffffff")
                gw.add(square_fill)

                square = GRect(INSET + j * SQUARE_SIZE, INSET + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                square.set_line_width(1)
                square.set_color(GRID_COLOR)
                gw.add(square)

    # making 3x3 grid
    for i in range(3):
         for j in range(3):
                
                square = GRect(INSET + j * BLOCK_SIZE, INSET + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                square.set_line_width(4)
                square.set_color(GRID_COLOR)
                gw.add(square)

    # making border for grid
    gw.border = GRect(INSET, INSET, GRID_SIZE, GRID_SIZE)
    gw.border.set_line_width(4)
    gw.add(gw.border)

    # adding numbers
    for i in range(9):
        for j in range(9):
                if gw.SUDOKU_GRID[j][i] != 0:
                    number = GLabel(str(gw.SUDOKU_GRID[j][i]))
                    number.set_font("bold 45pt 'serif'")
                    gw.add(number, INSET + j * SQUARE_SIZE + number.get_width() - 4, INSET + i * SQUARE_SIZE + number.get_height())
                    GLABEL_GRID[i].append(number)
                else:
                    number = GLabel("0")
                    number.set_font("bold 45pt 'serif'")
                    gw.add(number, INSET + j * SQUARE_SIZE + number.get_width() - 4, INSET + i * SQUARE_SIZE + number.get_height())
                    GLABEL_GRID[i].append(number)
                    number.set_label(" ")


# function for generating numbers
def generate_numbers(GAME_MODE):

    # configuring board
    def pattern(r,c): 
        return (3 * (r % 3) + r // 3 + c ) % 9

    r_3 = range(3) 
    rows  = [ g * 3 + r for g in random.sample(r_3, len(r_3)) for r in random.sample(r_3, len(r_3)) ] 
    cols  = [ g * 3 + c for g in random.sample(r_3, len(r_3)) for c in random.sample(r_3, len(r_3)) ]
    nums  = random.sample((range(1, 3 * 3 + 1)), len((range(1, 3 * 3 + 1))))

    gw.SUDOKU_GRID = [ [nums[pattern(r, c)] for c in cols] for r in rows ]

    # removing numbers
    to_remove = 81 - GAME_MODE # CAN BE CHANGED TO GET MORE OR LESS STARTING BLOCKS

    i = 0
    while i < to_remove:
        r_col = random.randint(0,8)
        r_row = random.randint(0,8)

        if gw.SUDOKU_GRID[r_col][r_row] != 0:
            gw.SUDOKU_GRID[r_col][r_row] = 0
            i += 1


    gw.USER_GRID = gw.SUDOKU_GRID
    

# function for creating starting screen
def create_starter():

    difficulty_starter = GRect(650,100)
    difficulty_starter.set_line_width(5)
    gw.add(difficulty_starter, 125,300)

    difficulty_text = GLabel("CHOOSE DIFFICULTY LEVEL")
    difficulty_text.set_font("bold 34pt 'serif'")
    gw.add(difficulty_text,135,365)

    for i in range(3):
        difficulty_level = GRect(191,75)
        difficulty_level.set_line_width(5)
        gw.add(difficulty_level, 125 + i * 229, 425)

    gw.easy_text = GLabel("EASY")
    gw.easy_text.set_font("bold 35pt 'serif'")
    gw.add(gw.easy_text,157,480)

    gw.medium_text = GLabel("MEDIUM")
    gw.medium_text.set_font("bold 34.5pt 'serif'")
    gw.add(gw.medium_text,358,480)

    gw.hard_text = GLabel("HARD")
    gw.hard_text.set_font("bold 35pt 'serif'")
    gw.add(gw.hard_text,612,480)


# algorithm for determining what square a GRect is
def find_square(x,y):
    return (x-INSET)//SQUARE_SIZE, (y-INSET)//SQUARE_SIZE


# highlight a square
def highlight(x,y):

    # removing last highlighted square
    if gw.selected_is_const == False:
        gw.highlighted.set_fill_color("#ffffff")
    else:
        gw.highlighted.set_fill_color(FILLED_SQUARE_COLOR)
    
    # getting to current square (could be more efficient)
    gw.remove(gw.border)

    block = gw.get_element_at(INSET + x * SQUARE_SIZE, INSET + y * SQUARE_SIZE)
    gw.remove(block)

    square_outline = gw.get_element_at(INSET + x * SQUARE_SIZE, INSET + y * SQUARE_SIZE)
    gw.remove(square_outline)

    square = gw.get_element_at(INSET + x * SQUARE_SIZE, INSET + y * SQUARE_SIZE)

    gw.add(square_outline)
    gw.add(block)
    gw.add(gw.border)

    # highlighting square
    if square.get_color() == "#FFFFFF":
        square.set_fill_color(SELECT_COLOR)
        gw.selected_is_const = False
    else:
        square.set_fill_color(FILLED_SELECT_COLOR)
        gw.selected_is_const = True
        
    
    gw.highlighted = square


# check if game is successfully completed
def check_game():
    sudoku_completed = True

    for i in range(9):
        for j in range(9):
            for k in range(9):
                if (gw.USER_GRID[i][j] == gw.USER_GRID[k][j] and i != k) or (gw.USER_GRID[i][j] == gw.USER_GRID[i][k] and j != k) or gw.USER_GRID[i][j] == 0:
                    sudoku_completed = False
                    
    return sudoku_completed

# for if game is successfully completed
def you_win():
    try:
        gw.remove(gw.winning_message)
    except:
        pass
    try:
        gw.remove(gw.persistence_message)
    except:
        pass
    gw.winning_message = GLabel("You win!")
    gw.winning_message.set_font("bold 30pt 'serif'")
    gw.add(gw.winning_message,370,38)

# for if game is not successfully completed
def try_again():
    def remove_persistence():
        gw.remove(gw.persistence_message)
    try:
        gw.remove(gw.winning_message)
    except:
        pass
    try:
        gw.remove(gw.persistence_message)
    except:
        pass
    gw.persistence_message = GLabel("Try again!")
    gw.persistence_message.set_font("bold 30pt 'serif'")
    gw.add(gw.persistence_message,350,38)
    gw.set_timeout(remove_persistence, 1000)

# when click action
def click_action(click):
    
    # determining difficulty mode
    if gw.first_action == True:
        
        if gw.easy_text.contains(click.get_x(),click.get_y()):
            gw.first_action = False
            gw.clear()
            generate_numbers(EASY_MODE)
            fill_window()

        elif gw.medium_text.contains(click.get_x(),click.get_y()):
            gw.first_action = False
            gw.clear()
            generate_numbers(MEDIUM_MODE)
            fill_window()

        elif gw.hard_text.contains(click.get_x(),click.get_y()):
            gw.first_action = False
            gw.clear()
            generate_numbers(HARD_MODE)
            fill_window()

    # determining click action in sudoku game
    elif gw.get_element_at(click.get_x(),click.get_y()) != None:
        gw.click_col, gw.click_row = find_square(click.get_x(),click.get_y())
        highlight(gw.click_col,gw.click_row)
        

# when key action
def key_action(key):

    if key.get_key().isnumeric() == True and gw.selected_is_const == False and key.get_key() != "0":
        GLABEL_GRID[gw.click_row][gw.click_col].set_label(key.get_key())
        GLABEL_GRID[gw.click_row][gw.click_col].send_to_front()
        gw.USER_GRID[gw.click_col][gw.click_row] = int(key.get_key())
    
    elif key.get_key() == "<SPACE>" or key.get_key() == "<BACKSPACE>":
        GLABEL_GRID[gw.click_row][gw.click_col].set_label(" ")
        GLABEL_GRID[gw.click_row][gw.click_col].send_to_front()
        gw.USER_GRID[gw.click_col][gw.click_row] = 0
    
    elif key.get_key() == "<RETURN>":
        if check_game() == True: 
            you_win()
        else:
            try_again()

# starting window
def play_sudoku():
    
    create_starter()
    gw.add_event_listener("click",click_action)
    gw.add_event_listener("key",key_action)



play_sudoku()