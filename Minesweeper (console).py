# DEPRECATED

"""
MINESWEEPER

(BETA BUILD)

PLEASE DO CONTACT FOR REPORTING ANY BUG!
"""

# Imports->
from random import randint, choice
from time import perf_counter, sleep
from os import system

# Global Declarations->
MIN_BOXES = 5
MAX_BOXES = 20  # (database part)
grid_dict = {}

if input('''\nNOTE- IDE used for this program is Pycharm and so it's best compatible with it.
So, if you are not running this on Pycharm, you may see weird characters printing out, or the shape of the grid going sick while playing.\n
Type 'p' for Pycharm or else leave it blank: ''').lower() == 'p':
    Pycharm = True
    NUM_SIGNS_DICT = {0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣'}
    # Colors->
    DEFAULT = '\033[m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    BOLD = '\033[1m'
    RED_BOLD = '\033[31;1m'
    GREEN_BOLD = '\033[32;1m'
    YELLOW_BOLD = '\033[33;1m'
    BLUE_BOLD = '\033[34;1m'
    # Notations->
    BLACK_BOX = '⬛'
    WHITE_BOX = '⬜'
    MINE_NOTATION = '💣'
    FLAG_NOTATION = '🚩'
else:
    Pycharm = False
    # Colors->
    DEFAULT = RED = GREEN = YELLOW = BLUE = BOLD = RED_BOLD = GREEN_BOLD = YELLOW_BOLD = BLUE_BOLD = ''
    # Notations->
    BLACK_BOX = 'X'
    WHITE_BOX = ' '
    MINE_NOTATION = 'M'
    FLAG_NOTATION = 'F'

    system('cls')  # clearing screen


print(BLUE_BOLD + '\nGAME DESCRIPTION :' + DEFAULT, BOLD + 'Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field. The game originates from the 1960s, and has been written for many computing platforms in use today. It has many variations and offshoots.' + DEFAULT, BLUE_BOLD + '(Wikipedia)' + DEFAULT)


# Functions->
def show_grid(game_over=False, flagging=False, flag_position=0):
    print(BLUE_BOLD + f'\n{column_numbering}' + DEFAULT, BOLD + line)  # top line

    pos = 0
    for r in range(rows):

        gap = '|' if r >= 9 else' |'  # one digit - two digit
        print(BLUE_BOLD + str(r + 1) + DEFAULT, BOLD, end=gap)  # numbering

        for c in range(columns):

            pos += 1
            output_sign = grid_dict[pos]  # copying values in a variable for showing

            if not game_over and output_sign == MINE_NOTATION:  # hiding the mines
                output_sign = BLACK_BOX

            if flagging and pos == flag_position:  # flagging
                flag_dict[pos] = FLAG_NOTATION

            if not game_over and pos in flag_dict:  # showing the flags
                output_sign = flag_dict[pos]

            gap = '  '
            if Pycharm and (output_sign in NUM_SIGNS_DICT):
                output_sign = NUM_SIGNS_DICT[output_sign]
                gap = ' '

            print(gap + str(output_sign), end='  |')  # data

        print(line)  # following line

    print(DEFAULT)  # color


def neighbours_of(x):
    # nums on vertices of grid->
    if (x in first_row) and (x in first_column):  # first row first column
        return bottom, right, bottom_right

    if (x in first_row) and (x in last_column):  # first row last column
        return bottom, left, bottom_left

    if (x in last_row) and (x in first_column):  # last row first column
        return top, right, top_right

    if (x in last_row) and (x in last_column):  # last row last column
        return top, left, top_left

    # nums on edges of grid->
    if x in first_row:
        return bottom, right, left, bottom_right, bottom_left

    if x in first_column:
        return top, bottom, right, top_right, bottom_right

    if x in last_column:
        return top, bottom, left, bottom_left, top_left

    if x in last_row:
        return top, right, left, top_right, top_left

    # All other(in the center)->
    return top, bottom, right, left, top_right, bottom_right, bottom_left, top_left


def get_mine_count_at(x):
    m_count = 0
    for neighbor in neighbours_of(x):
        if grid_dict[x+neighbor] == MINE_NOTATION:
            m_count += 1
    return m_count


def opened_boxes():
    o_boxes = 0
    for b in grid_dict:
        if grid_dict[b] != BLACK_BOX:
            o_boxes += 1
    return o_boxes


def fill_grid_with_black():
    for b in range(total_boxes):
        grid_dict[b+1] = BLACK_BOX  # notation


def won():
    show_grid(game_over=True)
    print(GREEN_BOLD + 'YOU WON! :)' + DEFAULT)
    time_taken = perf_counter() - timer
    print(YELLOW_BOLD + f'\nTime Taken: {time_taken} seconds,' + DEFAULT, end=' ')

    # Record Implementation->
    import sqlite3

    con = sqlite3.connect('DB (console).sqlite')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS "Data" (
                    "Row"	INTEGER NOT NULL,
                    "Column"	INTEGER NOT NULL,
                    "Time"	REAL,
                    PRIMARY KEY("Row","Column"))''')

    cur.execute('SELECT * FROM Data')
    if cur.fetchone() is None:  # for new computer
        for r in range(MIN_BOXES, MAX_BOXES + 1):
            for c in range(MIN_BOXES, MAX_BOXES + 1):
                cur.execute('INSERT INTO Data("Row", "Column") VALUES(?, ?)', (r, c))  # tuple->preventing sql injection!

    # Main->
    cur.execute('SELECT "Time" FROM Data WHERE "Row" = ? AND "Column" = ?', (rows, columns))
    fetched_time = cur.fetchone()[0]
    if fetched_time is None or fetched_time > time_taken:
        print(RED_BOLD + 'Congratulations! This is your new Best! 🎆' + DEFAULT)
        cur.execute('UPDATE Data SET "Time" = ? WHERE "Row" = ? AND "Column" = ?', (time_taken, rows, columns))
    else:
        print(RED_BOLD + f'(Best: {fetched_time} seconds)' + DEFAULT)

    con.commit()
    cur.close()


# GAME START ->
while True:
    print(BLUE_BOLD + '\nNEW GAME ->' + DEFAULT)

    flag_dict = {}  # to store positions of flags!
    timer = 0  # seconds

    # Grid dimension input->
    try:
        rows = int(input(f'\nEnter the no. of rows you want in the game(at least {MIN_BOXES}): '))
        if rows < MIN_BOXES:
            rows = MIN_BOXES
            print(GREEN_BOLD + f':| Rows changed to {rows}' + DEFAULT)
        columns = int(input(f'Enter the no. of columns you want in the game(at least {MIN_BOXES}): '))
        if columns < MIN_BOXES:
            columns = MIN_BOXES
            print(GREEN_BOLD + f':| Columns changed to {columns}' + DEFAULT)
            sleep(1)  # :)

    except Exception as e:
        print(RED + f'Error Occurred: [{e}]' + DEFAULT)
        continue

    # Weird logic for nice view->
    column_numbering = '    ' if Pycharm else '      '
    for i in range(columns):
        space = '      ' if Pycharm else '     '
        if i >= 9:  # one digit - two digit
            space = '    '
        column_numbering += str(i+1) + space
    line = ('\n   -' + ('-' * 6 * columns + '-' * (columns // 2))) if Pycharm else ('\n   -' + ('-' * 6 * columns))

    total_boxes = rows * columns
    fill_grid_with_black()  # filling initial grid!
    print(BLUE + '\nGrid will look like this->' + DEFAULT, end='')
    show_grid()
    # print('\n', grid_dict); continue  # debugging!

    # Mines->
    no_of_mines = (rows * columns) // MIN_BOXES
    positions_of_mines = []

    # Making random hole->
    while True:
        white_boxes = 0
        rand_row_starting = randint(1, rows//2)
        rand_row_ending = randint(rows//2 + 1, rows)
        # print(rand_row_starting, rand_row_ending)  # debugging!
        row_number = 0
        for row in range(0, total_boxes, rows):
            row_number += 1
            if rand_row_starting <= row_number <= rand_row_ending:  # imp! both included
                rand_column_starting = randint(1, columns//2)
                rand_column_ending = randint(columns//2 + 1, columns)
                # print('\n', rand_column_starting, rand_column_ending, '\n')  # debugging!
                column_number = 0
                for box in range(rows):
                    column_number += 1
                    if rand_column_starting <= column_number <= rand_column_ending:  # imp! both included
                        # print(row, column_number)  # debugging!
                        grid_dict[row+column_number] = WHITE_BOX  # notation!
                        white_boxes += 1

        # Checking if the no. of mines is not equal to the no of closed boxes->
        if total_boxes-white_boxes > no_of_mines:
            # print(total_boxes-white_boxes, no_of_mines); show_grid()  # debugging!
            break
        fill_grid_with_black()

    # Generating random mines->
    eligible_mine_positions = [box for box in grid_dict if box != WHITE_BOX]
    for i in range(no_of_mines):
        position = choice(eligible_mine_positions)
        grid_dict[position] = MINE_NOTATION
        positions_of_mines.append(position)
        eligible_mine_positions.remove(position)

    # show_grid(game_over=True); continue  # debugging!

    # Neighbours->
    top = -columns
    bottom = +columns
    right = +1
    left = -1
    top_right = top + right
    bottom_right = bottom + right
    bottom_left = bottom + left
    top_left = top + left
    # print('\n', top, bottom, right, left, top_right, bottom_right, bottom_left, top_left)  # debugging!

    # Edges of grid->
    first_row = [(i + 1) for i in range(columns)]
    last_row = [(total_boxes - columns + i + 1) for i in range(columns)]
    first_column = [i for i in range(1, total_boxes, columns)]
    last_column = [(i + columns) for i in range(0, total_boxes, columns)]
    # print(first_row, '\n', last_row, '\n', first_column, '\n', last_column)  # debugging!

    # Game difficulty->
    if no_of_mines <= 10:
        game_diff = 'Easy'
    elif no_of_mines <= 35:
        game_diff = 'Medium'
    elif no_of_mines <= 75:
        game_diff = 'Hard'
    else:
        game_diff = 'Bro you sure?'

    print(YELLOW_BOLD + 'Game Difficulty (depends on the size of the grid) ->', game_diff + DEFAULT)

    print(BOLD + f"\n[ Notations ->\nClosed Box = '{BLACK_BOX}'\nOpened Box = '{WHITE_BOX}'\nMine = '{MINE_NOTATION}'\nFlag = '{FLAG_NOTATION}' ]" + DEFAULT)  # notation info!

    input(BLUE + '\nPress Enter to Start!' + DEFAULT)  # giving time to user to checkout wth is going on!

    # REAL GAME START ->
    flag_count = no_of_mines
    user_input = None
    flagging_box = opening_box = False

    while True:
        if user_input is not None:

            if flagging_box:
                flag_count -= 1

            elif opening_box:

                if grid_dict[user_input] == MINE_NOTATION:
                    show_grid(game_over=True)
                    print(RED_BOLD + 'YOU LOSE! :(' + DEFAULT, RED + '(the box you opened had bomb)' + DEFAULT)
                    break

                else:
                    grid_dict[user_input] = WHITE_BOX

                    if opened_boxes() == total_boxes:
                        grid_dict[user_input] = get_mine_count_at(user_input)  # writing mine count on the last opened box!
                        won()
                        break

        # Finding eligible numbering positions->
        numbering_positions = []
        for position in grid_dict:
            if grid_dict[position] == WHITE_BOX:
                numbering_positions.append(position)

        # print('\n', numbering_positions)  # debugging!

        # Managing and doing numbering->
        for position in numbering_positions:
            mine_count = get_mine_count_at(position)
            # print('\n', position, mine_count, end='')  # debugging!

            # doing numbering where it's not 0->
            if mine_count != 0:
                grid_dict[position] = mine_count

        # show_grid(game_over=True)  # debugging!

        # Opening EXTRA boxes->
        junk = True
        while junk:  # till no left!
            junk = False
            for box in grid_dict:
                # print(box, grid_dict[box])  # debugging!
                if grid_dict[box] == WHITE_BOX:
                    # print('outer')  # debugging!
                    for neighbour in neighbours_of(box):
                        if grid_dict[box + neighbour] == BLACK_BOX:
                            # print('inner')  # debugging!
                            mine_count = get_mine_count_at(box + neighbour)
                            if mine_count == 0:
                                grid_dict[box + neighbour] = WHITE_BOX
                            else:
                                grid_dict[box + neighbour] = mine_count
                            junk = True

        # Checking the winning condition again after opening extra boxes->
        if opened_boxes() == total_boxes:
            # Rare Case->
            if user_input is None:
                show_grid(game_over=True)
                print(GREEN_BOLD + 'YOU WON BY LUCK! :)' + DEFAULT, GREEN + '(this happens rarely, when the no. of boxes are too few, try again with greater no. of boxes!)' + DEFAULT)
                break

            won()
            break

        # show_grid(game_over=True); break  # debugging!

        # show_grid(True)  # dev's stuff 😁

        show_grid(flagging=flagging_box, flag_position=user_input)  # final(fully ready) grid!

        if user_input is None:
            print(BLUE + f'Number of Mines (inside closed boxes): {no_of_mines}' + DEFAULT)

            print(BLUE + '\nTimer has been started! (running in background, will be updated soon!)\n' + DEFAULT)
            timer = perf_counter()

        if flagging_box:
            print(BLUE + f'Flags Left-> {flag_count}\n' + DEFAULT)

        # TOTALLY REAL GAME STARTED ->
        while True:
            flagging_box = removing_flag = opening_box = False

            print(GREEN + f'Timer : {int(perf_counter() - timer)} seconds\n' + DEFAULT)

            user_input = input("Enter '1' to flag/ '2' to open a box: ")

            if user_input == '1':

                while True:
                    try:
                        row_value = int(input("\nTo flag a box, enter box's row number: "))
                        if not (0 < row_value <= rows):
                            print(RED + f"Row {row_value} doesn't exists." + DEFAULT)
                            continue

                        column_value = int(input('and column number: '))
                        if not (0 < column_value <= columns):
                            print(RED + f"Column {column_value} doesn't exists." + DEFAULT)
                            continue

                        user_input = columns * (row_value - 1) + column_value

                        if grid_dict[user_input] == BLACK_BOX or user_input in positions_of_mines:

                            if user_input in flag_dict:

                                if input("\nRemove the flag? Enter '1' for yes or '2' for no: ") == '1':
                                    flag_dict.__delitem__(user_input)
                                    flag_count += 1
                                    print(BLUE + f'\nFlag removed, flags available-> {flag_count}' + DEFAULT)
                                    removing_flag = True
                                    break

                                continue

                            elif flag_count <= 0:
                                print(RED + 'No Flags Left.\n' + DEFAULT)
                                break

                            flagging_box = True
                            break

                        print(RED + 'Flags are meant to be on closed boxes only :)' + DEFAULT)

                    except ValueError as e:
                        print(RED + f'Error Occurred: [{e}]\n' + DEFAULT)
                        break

                if flagging_box or removing_flag:
                    break

            elif user_input == '2':

                while True:
                    try:
                        row_value = int(input("\nTo open a box, enter box's row number: "))
                        if not (0 < row_value <= rows):
                            print(RED + f"Row {row_value} doesn't exists." + DEFAULT)
                            continue

                        column_value = int(input('and column number: '))
                        if not (0 < column_value <= columns):
                            print(RED + f"Column {column_value} doesn't exists." + DEFAULT)
                            continue

                        user_input = columns * (row_value - 1) + column_value

                        if grid_dict[user_input] == BLACK_BOX or user_input in positions_of_mines:

                            if user_input in flag_dict:
                                print(RED + "Can't open a flagged box!!" + DEFAULT)
                                continue

                            opening_box = True
                            break

                        print(RED + 'Only opening a closed box makes sense :)' + DEFAULT)

                    except ValueError as e:
                        print(RED + f'Error Occurred: [{e}]\n' + DEFAULT)
                        break

                if opening_box:
                    break

            else:
                print(RED + 'Enter correct choice.\n' + DEFAULT)
                continue

    print(BLUE_BOLD + '\nTHANKS FOR PLAYING! :)\n' + DEFAULT)
