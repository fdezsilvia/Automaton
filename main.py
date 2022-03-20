from karel.stanfordkarel import *
from random import *

'''
Karel is an automaton following Conway's rule 22. The initial state is chose randomly between the simple initial condition(one corner paint in the midpoint of the last street)
or multiple painted corners, these are randomly separated.
Living cells are blue and dead cells are blank.
'''

def main():
    put_beeper()            # Works as a final point indicator in (1,1)
    go_up()
    choose_state()
    start_line()
    # Karel generate the pattern while no beeper present. One beeper is present in (1,1), this is the final point indicator
    while no_beepers_present():
        check_cells()
        check_7_to_0()
    pick_beeper()    # Pick beeper in (1,1)

"""
Karel moves to the last street and stay in the first avenue
Pre: Karel is in (1,1) and faces east
Post: Karel is in the same avenue, in the north edge and faces the same direction
"""
def go_up():
    turn_left()
    while front_is_clear():
        move()
    turn_right()

"""
Choose between two options, that is going to be the initial state
Pre: Karel faces east in the last street and the first avenue
Post: Karel faces east in the same street in the last avenue.
"""
def choose_state():
    seed()
    rand = randint(0,1)
    if rand == 1:
        pattern_state()
    else:
        one_triangle()

"""
Karel paints blue multiple corner in the last street. The corners are separated between 0 and 10 movements.
"""
def pattern_state():
    seed()
    # Paint the next corner only if front is clear
    while front_is_clear():
        p = randint(0,10)
        # P is the separation between corners
        for i in range(p):
            if front_is_clear():
                move()
        # She paint a corner blue, just if she can move p corners
        if front_is_clear():
            paint_corner(BLUE)

"""
Karel paints blue one corner in the middle of the last street
"""
def one_triangle():
    middler_point()

def middler_point():
    find_point()
    pick_all_beepers()

"""
Find the middle point using beepers
"""
def find_point():
    put_beeper()
    move_to_wall()
    put_beeper()
    move()
    while no_beepers_present():
        while no_beepers_present():
            move()
        middle_corner()
        move()
        turn_around()
        if no_beepers_present():
            move()
            put_beeper()
            middle_corner()
        else:
            move()
            put_beeper()
            paint_corner(BLUE)
            if left_is_blocked():
                turn_around()
"""
Remove all the beepers in the last street
Pre: Karel is in the midpoint facing west
Post: Karel is in the east edge, and faces east. It's in the same street
"""
def pick_all_beepers():
    move_to_wall()
    while front_is_clear():
        pick_beeper()
        move()
    # Pick the last corner beeper
    pick_beeper()


# Karel checks if it's possible to have a trio
def check_cells():
    if front_is_clear():
        move()
        if front_is_clear():
            middle_corner()
            turn_around()
        else:
            start_line()
    else:
        start_line()

"""
Check if the first corner of the trio is alive or dead.
If it's alive is going to be one of the 7 to 4 states.
If it's dead is going to be one of the 3 to 0 states.
"""
def check_7_to_0():
    while no_beepers_present():
        if corner_color_is(BLUE):
            move()
            check_7_to_4()
        else:
            move()
            check_3_to_0()

"""
If the first cell is alive checks the middle cell of the trio.
If it's alive is going to be one of the 7 to 6 states.
If it's dead is going to be one of the 5 to 4 states.
"""
def check_7_to_4():
    if corner_color_is(BLUE):
        move()
        check_7_to_6()
    else:
        move()
        check_5_to_4()

"""
If the first cell and the middle one are alive checks the right cell of the trio.
If it's alive is going to be the 7 state.
If it's dead is going to be the 6 state.
"""
def check_7_to_6():
    if corner_color_is(BLUE):
        state_7()
    else:
        state_6()

"""
If the first cell is alive and the middle one is dead checks the right cell of the trio.
If it's alive is going to be the 5 state.
If it's dead is going to be the 4 state.
"""
def check_5_to_4():
    if corner_color_is(BLUE):
        state_5()
    else:
        state_4()

"""
If the first cell is dead checks the middle cell of the trio.
If it's alive is going to be 3 or 2 state.
If it's dead is going to be one of 1 or 0 states.
"""
def check_3_to_0():
    if corner_color_is(BLUE):
        move()
        check_3_to_2()
    else:
        move()
        check_1_to_0()

"""
If the first cell and the middle one are alive checks the right cell of the trio.
If it's alive is the 3 state.
If it's dead is the 2 state.
"""
def check_3_to_2():
    if corner_color_is(BLUE):
        state_3()
    else:
        state_2()

"""
If the first cell is alive and the middle one is dead checks the right cell of the trio.
If it's alive is 1 state.
If it's dead is 0 state.
"""
def check_1_to_0():
    if corner_color_is(BLUE):
        state_1()
    else:
        state_0()

# It depends on the state that it is born a new cell or not in the right corner of the central clump of the trio. D = dead, L = alive, B = born

# 7 = LLL = D
def state_7():
    dead()

# 6 = LLD = D
def state_6():
    dead()
    
# 5 = LDL = D
def state_5():
    dead()

# 4 = LDD = B
def state_4():
    born()

# 3 = DLL = D
def state_3():
    dead()

# 2 = DLD = B
def state_2():
    born()

# 1 = DDL = B
def state_1():
    born()

# 0 = DDD = D
def state_0():
    dead()


def dead():
    if front_is_clear():         # if it isn't in the end of row. She move to start checking another trio
        middle_corner()
        turn_around()
    else:                        # if it is in the end of row
        middle_corner()
        move_down()
        paint_corner(BLANK)
        turn_right()
        move_to_wall()

def born():
    if front_is_clear():        # if it isn't in the end of row
        middle_corner()
        turn_left()
        if front_is_clear():  # A cell is born only if there isn't the south wall
            move()
            paint_corner(BLUE)
            middle_corner()
            turn_right()
    else:                      # if it is in the end of row
        middle_corner()
        move_down()
        paint_corner(BLUE)
        turn_right()
        move_to_wall()


# move to the middle corner of a trio
def middle_corner():
    turn_around()
    move()

"""
Pre: Karel faces east
Post: Karel is in the corner below facing south
"""
def move_down():
    turn_left()
    move()

"""
Pre: She is in front the east wall
Post: She is in the first avenue, facing east
"""
def start_line():
    turn_around()
    move_to_wall()

# Pre: She is in front of the east wall facing west
# Pro: faces east next to west wall
def move_to_wall():
    while front_is_clear():
        move()
    turn_around()

# Karel turn 180º
def turn_around():
    for i in range(2):
        turn_left()

# Karel turn 270º to left
def turn_right():
    for i in range(3):
        turn_left()


if __name__ == "__main__":
    main()
