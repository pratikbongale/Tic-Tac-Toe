import math

class State:
    '''
    Defines a State in our game tree (a configuration of game board)
    :param: player - Current player(min/max)
    :param: stateDesc - The configuration of game board, a 3x3 matrix
    :param: utility - The utility value of current state
    :param: playerSymbol - The symbol used by the player('X' or '0')
    '''
    def __init__(self, player, board):
        self.player = player
        self.utility = None
        self.successors = None
        self.stateDesc = board
        self.playerSymbol = 'X' if player == 'max' else '0'

    def getSuccessors(self):
        '''
        Generates all the successor states possible from the current state(as described by state description)
        '''
        if self.successors == None:

            board = self.stateDesc
            self.successors = []

            i = 0
            j = 0

            # who will be the player for next turn
            nextPlayer = 'min' if self.player == 'max' else 'max'

            # walk through the board
            while i < 3 and j < 3:
                if board[i][j] == None:
                    newBoard = getCopy(board)
                    child = State(nextPlayer, newBoard)    # create a new state
                    child.stateDesc[i][j] = child.playerSymbol
                    self.successors.append(child)
                if j == 2:
                    i += 1
                    j = 0
                else:
                    j += 1

        return self.successors

def getCopy(board):
    '''
    Create a copy of game board passed as argument and returns the new copy
    '''
    newBoard = [[None for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            newBoard[i][j] = board[i][j]

    return newBoard

states_count = 0
def minimax_decision(state):
    '''
    Return the best move for computer at a given state
    We need to call this method after the human player plays to decide the computers play
    '''

    if is_terminal(state):
        return state

    value = max_value(state)

    for s in state.getSuccessors():
        if s.utility == value:
            print('\nComputer plays :')
            print_state(s.stateDesc) # the next stage chosen
            break
    return s

def is_game_over(state):
    '''
    Checks if we have reached the terminal state so that we can declare if the game is over
    '''
    return is_terminal(state)

def max_value(state):
    global states_count
    if is_terminal(state):
        # state.utility = calculate_utility(state)
        return state.utility
    else:
        v = -1 * math.inf
        for s in state.getSuccessors():
            states_count += 1
            temp = min_value(s)
            s.utility = temp
            v = max(v, temp)
        return v

def min_value(state):
    global states_count
    if is_terminal(state):
        # state.utility = calculate_utility(state)
        return state.utility
    else:
        v = math.inf
        for s in state.getSuccessors():
            states_count += 1
            temp = max_value(s)
            s.utility = temp
            v = min(v, temp)
        return v

def is_terminal(state):
    '''
    Checks all the possible terminal state conditions
    '''
    s = state.stateDesc

    noneExists = False

    # check rows and columns
    for i in range(3):
        # check each row
        if None not in s[i]:
            if s[i][:] == ['X', 'X', 'X']:
                state.utility = -1
                return True
            elif s[i][:] == ['0', '0', '0']:
                state.utility = 1
                return True
        else:
            noneExists = True

        # check each column
        if s[0][i] == 'X' and s[1][i] == 'X' and s[2][i] == 'X':
            state.utility = -1
            return True

        if s[0][i] == '0' and s[1][i] == '0' and s[2][i] == '0':
            state.utility = 1
            return True

    # check diagonals
    if s[0][0] == 'X' and s[1][1] == 'X' and s[2][2] == 'X':
        state.utility = -1
        return True
    if s[0][0] == '0' and s[1][1] == '0' and s[2][2] == '0':
        state.utility = 1
        return True
    if s[0][2] == 'X' and s[1][1] == 'X' and s[2][0] == 'X':
        state.utility = -1
        return True
    if s[0][2] == '0' and s[1][1] == '0' and s[2][0] == '0':
        state.utility = 1
        return True

    if noneExists == False:
        # we have reached a tie
        state.utility = 0
        return True
    else:
        return False

def min_max_algorithm():
    '''
    The implementation of regular minimax algorithm
    '''
    game_over = False

    global states_count
    states_count = 0

    # create an initial playground
    board = [[None for _ in range(3)] for _ in range(3)]

    while game_over is not True:
        print('\nPlease provide position(x,y) to mark \'X\' (range [0-2][0-2]): ', end="")
        x, y = input().split(" ")

        x = int(x)
        y = int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print('Please provide a input in range [0-2] only : ')
            continue

        if board[x][y] is not None:
            print('Block already occupied')
            continue

        board[x][y] = 'X'
        print_state(board)

        state = State(player='max', board=board)
        # states_count += 1

        # count before making this move
        local_state_count = states_count

        # decide on what action to take and return the result of action
        res_state = minimax_decision(state)
        board = res_state.stateDesc

        print('States generated to decide this move : ', (states_count-local_state_count) )

        if is_game_over(res_state) == True:
            if res_state.utility == 0:
                print('========== Tie ===========')
            elif res_state.utility == -1:
                print('========== Human wins =========')
            else:
                print('========== Computer wins =========')
            game_over = True

def print_state(board):
    '''
    Print the state board(3x3 matrix)
    '''
    for i in range(3):
        for j in range(3):
            print(board[i][j] if board[i][j] is not None else ' ', end=' ')
        print()

def min_max_with_alpha_beta_pruning():
    '''
    The implementation of minimax algorithm with alpha beta pruning
    '''
    game_over = False

    global states_count
    states_count = 0

    # create an initial playground
    board = [[None for _ in range(3)] for _ in range(3)]

    while game_over is not True:
        print('\nPlease provide position(x,y) to mark \'X\' (range [0-2][0-2]): ', end="")
        x, y = input().split(" ")

        x = int(x)
        y = int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print('Please provide a input in range [0-2] only : ')
            continue

        board[x][y] = 'X'
        print_state(board)
        state = State(player='max', board=board)
        # states_count += 1

        # count before making this move
        local_state_count = states_count

        # decide on what action to take and return the result of action
        res_state = minimax_decision_abp(state)
        board = res_state.stateDesc

        print('States generated to decide this move : ', (states_count - local_state_count))

        if is_game_over(res_state) == True:
            if res_state.utility == 0:
                print('========== Tie ===========')
            elif res_state.utility == -1:
                print('========== Human wins =========')
            else:
                print('========== Computer wins =========')
            game_over = True

def minimax_decision_abp(state):
    '''
    Decides what move should be played
    :param state: current state of game
    :return: The state of the game after the computer has played its move
    '''
    # return the best move for computer at a given state
    # we need to call this method after whatever the human player plays

    if is_terminal(state):
        return state

    value = max_value_abp(state, -1 * math.inf, math.inf)

    for s in state.getSuccessors():
        if s.utility == value:
            print('\nComputer plays :')
            print_state(s.stateDesc) # the next stage chosen
            break
    return s

def max_value_abp(state, a, b):
    global states_count
    if is_terminal(state):
        # state.utility = calculate_utility(state)
        return state.utility
    else:
        v = -1 * math.inf
        for s in state.getSuccessors():
            states_count += 1
            temp = min_value_abp(s, a, b)
            s.utility = temp
            v = max(v, temp)

            if v >= b:   # no scope of better results
                return v
            a = max(a, v)
        return v

def min_value_abp(state, a, b):
    global states_count
    if is_terminal(state):
        # state.utility = calculate_utility(state)
        return state.utility
    else:
        v = math.inf
        for s in state.getSuccessors():
            states_count += 1
            temp = max_value_abp(s, a, b)
            s.utility = temp
            v = min(v, temp)

            if v <= a:
                return v

            b = min(b,v)
        return v

def main():

    print('Which Algorithm to use :\n1. Regular Minimax\n2. Minimax using alpha-beta pruning\nPlease select : ',end="")
    choice = int(input())

    if choice == 1:
        min_max_algorithm()
        print('Total number of states generated by general algorithm : ', states_count)
    elif choice == 2:
        min_max_with_alpha_beta_pruning()
        print('Total number of states generated by minimax with alpha beta pruning : ', states_count)
    else:
        return

main()






