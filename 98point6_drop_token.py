#  Keoni Akina
#  98point6_drop_token.py
#  This is a ConnectFour command line implementation
# Simply run the Python Script
# The game responds to the commands that were listed in the instructions and below

#PUT -> (OK | ERROR | WIN | DRAW)
#GET -> List of columns that have been successfully put to
#BOARD -> a 4x4 matrix that shows the board state
#EXIT -> Ends the Program

from sys import stdin
import numpy

#  Command List
GET = "GET"
BOARD = "BOARD"
EXIT = "EXIT"

#  Globals
const_game_size = 4
turns_remaining = const_game_size ** 2
game_board = numpy.zeros((const_game_size,const_game_size), dtype=int)
player_turn = 1
put_stack = []


def print_game_board():

    row_string = "| "
    dash_string = "+ "
    num_string = "  "

    for row in range(0, const_game_size):
        for col in range(0, const_game_size):
            row_string += str(int(game_board[row, col])) + " "
        print(row_string)
        row_string = "| "

    for i in range(0, const_game_size):
        dash_string += "- "
    print(dash_string)

    for i in range(1, const_game_size + 1):
        num_string += str(i) + " "
    print(num_string)


def inspect_for_put_command(command):

    for put_col_index in range(1, const_game_size + 1):
        if command == "PUT " + str(put_col_index):
            return check_and_execute_put(put_col_index)
    return False


def check_and_execute_put(put_col_index):

    if put_col_index <= 0 or put_col_index > const_game_size:
        print("Error: Out of Bounds")
        return False
    elif game_board[0, put_col_index - 1] != 0:
        print("Error: Column Full")
        return False
    else:
        insert_put_value(put_col_index)
        return True


def insert_put_value(put_col_index):

    global turns_remaining

    for row in range(const_game_size - 1, -1, -1):
        if game_board[row, put_col_index - 1] == 0:
            game_board[row, put_col_index - 1] = get_player_turn()
            turns_remaining -= 1
            set_player_turn()
            add_to_put_stack(put_col_index)
            print("OK")
            return
    print("ERROR: Full Column")
    return


def get_player_turn():

    return player_turn


def set_player_turn():

    global player_turn

    if player_turn == 1:
        player_turn = 2
    else:
        player_turn = 1


def check_for_winner():

    if lr_diagonal_down_win():
        return True
    elif lr_diagonal_up_win():
        return True
    elif check_row_win():
        return True
    elif check_col_win():
        return True
    else:
        return False


def lr_diagonal_down_win():

    # Check for left to right diagonal win
    for row in range(0, const_game_size):
        col = row
        if game_board[row, col] == 0:
            return False

        elif game_board[row, col] != game_board[row + 1, col + 1]:
            return False
        elif row == const_game_size - 2:
            # We've reached the end of the diagonal successfully
            return get_player_turn()


def lr_diagonal_up_win():

    for row in range(const_game_size - 1, 0, -1):
        col = (const_game_size - 1) - row
        if game_board[row, col] == 0:
            return False
        elif game_board[row, col] != game_board[row - 1, col + 1]:
            return False
        elif col == const_game_size - 2:
            # We've reached the end of the diagonal successfully
            return get_player_turn()


def check_row_win():

    for row in range(0, const_game_size):
        for col in range(0, const_game_size):
            if game_board[row, col] == 0:
                break
            elif game_board[row, col] != game_board[row, col + 1]:
                break
            elif col == const_game_size - 2:
                # We've reached the end of the row successfully
                return get_player_turn()
    return False


def check_col_win():

    for col in range(0, const_game_size):
        for row in range(0, const_game_size):
            if game_board[row, col] == 0:
                break
            elif game_board[row, col] != game_board[row + 1, col]:
                break
            elif row == const_game_size - 2:
                # We've reached the end of the col successfully
                return get_player_turn()
    return False


def add_to_put_stack(put_num):

    global put_stack

    put_stack.append(put_num)


def print_put_stack():

    global put_stack

    for i in range(0, len(put_stack)):
        print(put_stack[i])


# TESTING FUNCTIONS

def reset_game():

    global game_board
    global turns_remaining
    global put_stack

    turns_remaining = const_game_size ** 2
    game_board = numpy.zeros((const_game_size, const_game_size), dtype=int)
    put_stack = []


def play_again():

    yes = 'Y'
    no = 'N'

    print("Play again? Y/N")
    ans = stdin.readline().rstrip('\n')
    while ans != yes and ans != no:
        ans = stdin.readline().rstrip('\n')
    if ans == yes:
        reset_game()
        command = stdin.readline().rstrip('\n')
    else:
        command = EXIT

    return command

# TESTING FUNCTIONS


def main():

    print("Welcome to Drop Token!")
    print("Press any key to start...")
    stdin.readline().rstrip('\n')
    print("Player " + str(get_player_turn()) + " > ")
    command = stdin.readline().rstrip('\n')
    win = False
    draw = False

    while command != EXIT:
        valid_move = inspect_for_put_command(command)
        print("Player " + str(get_player_turn()) + " > ")
        if turns_remaining == 0 and not draw:
            draw = True
            print("DRAW")
        elif valid_move:
            if check_for_winner() and not win:
                    win = True
                    print("WIN")
        elif command == BOARD:
            print_game_board()
        elif command == GET:
            print_put_stack()
        else:
            print("Error: Unknown command")
        command = stdin.readline().rstrip('\n')

    if command == EXIT:
        print("DONE.")
    else:
        "DRAW."

main()





