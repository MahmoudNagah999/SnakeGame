# import modules nessary for the game
import random
import curses

# initialize the curses library to create our screen 
screen = curses.initscr()

# hide the mouse cursor
curses.curs_set(0)

# get max screen hight and width
screen_hight, screen_width = screen.getmaxyx()

#create a new window
window = curses.newwin(screen_hight, screen_width, 0, 0)

#allow window to recieve input from keyboard
window.keypad(1) 

# set the delay for updating the screen 
window.timeout(100)

# set x,y coordinates for the initial position of the snake
snk_x = screen_width // 4
snk_y = screen_hight // 2  # // = integer division (the result is integer value)

#define the initial position of the snake body
snk = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# create the food in the middel of the window
food = [screen_hight // 2, screen_width // 2]

# add the food by using the PI character from curses model
window.addch(food[0], food[1], curses.ACS_PI)

# set the initial movement direction of the snake to the right
key = curses.KEY_RIGHT

#create the game loop that loops forever until the player lose or exits the game
while True:
    # get the next key input from the user
    next_key = window.getch()
    # if the user dosn't input anything, key remains the same, else key will be set to the new preessed key  
    key = key if next_key == -1 else next_key
    # check if snake collided with the walls or itself
    if snk[0][0] in [0, screen_hight] or snk[0][1] in [0, screen_width] or snk[0] in snk[1:]:
        # if it collided, close the window and end the game
        curses.endwin() # close the window 
        quit() # end the program
    # set the new position of the head of the snake based on the current direction
    new_head = [snk[0][0], snk[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1

    # add the new head of the snake to the first position of the snake list
    snk.insert(0, new_head)

    # if the snake ate the food
    if snk[0] == food:
        food = None # remove the food if snake ate
        # while food is None, generate new food in random position
        while food is None:
            new_food = [
                random.randint(1, screen_hight - 1), 
                random.randint(1, screen_width - 1)
            ]
            # set the food to the new food if the new food is not in the snake body
            food = new_food if new_food not in snk else None
        
        # add the new food to the screen
        window.addch(food[0], food[1], curses.ACS_PI)
    else:
        # otherwise remove the last segq of the snake body
        tail = snk.pop()
        window.addch(tail[0], tail[1], ' ')

    # update the position of the snake on the screen
    window.addch(snk[0][0], snk[0][1], curses.ACS_CKBOARD)