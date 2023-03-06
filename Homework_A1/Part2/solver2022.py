#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Sakshi Sitoot (ssitoot)
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
import numpy as np

ROWS=5
COLS=5

def move_right(board, row):
    board[row] = board[row][-1:] + board[row][:-1]
    return board

def move_left(board, row):
    board[row] = board[row][1:] + board[row][:1]
    return board

def move_up(board, col):
    board = transpose_board(move_left(transpose_board(board), col))
    return board

def move_down(board, col):
    board = transpose_board(move_right(transpose_board(board), col))
    return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_clockwise_inner(board):
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_clockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    return board

def move_cclockwise(board):
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def move_cclockwise_inner(board):
    board=np.array(board)
    inner_board=board[1:-1,1:-1].tolist()
    inner_board = move_cclockwise(inner_board)
    board[1:-1,1:-1]=np.array(inner_board)
    board=board.tolist()
    return board

def getSingleManhattanDistance(r,c,goal_r,goal_c):
    manhattan_single_cell = abs(r-goal_r) + abs(c-goal_c)
    return manhattan_single_cell

def getBoardManhattanDistance(board):
    goal_position_dict = {1:(0,0), 2:(0,1), 3:(0,2), 4:(0,3), 5:(0,4), 6:(1,0), 7:(1,1), 8:(1,2), 9:(1,3), 10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2), 19:(3,3), 20:(3,4), 21:(4,0),22:(4,1),23:(4,2),24:(4,3),25:(4,4)}
    board_manhattan_result = 0
    displaced_tiles = 0
    #goal_position = (-1,-1)
    for i in range(0,len(board)):
        for j in range(0,len(board[0])):
            goal_position = goal_position_dict[board[i][j]]
            distance_of_cell = getSingleManhattanDistance(i,j,goal_position[0],goal_position[1])
            board_manhattan_result = board_manhattan_result + distance_of_cell

    return board_manhattan_result

def transpose_board(board):
    return [list(col) for col in zip(*board)]

def transpose_board(board):
    return [list(col) for col in zip(*board)]

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# return a list of possible successor states
def successors(state):
    original_state = state[:]
    goal_state_list = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]

    successor_states = []

    for i in range(0,5):
        successor_states.append(move_right(state, i))
        state = original_state[:]
        successor_states.append(move_left(state, i))
        state = original_state[:]
        successor_states.append(move_up(state,i))
        state = original_state[:]
        successor_states.append(move_down(state,i))
        state = original_state[:]

    successor_states.append(move_clockwise(state))
    successor_states.append(move_cclockwise(state))
    successor_states.append(move_clockwise_inner(state))
    successor_states.append(move_cclockwise_inner(state))

    printable_successor_states = []
    temporary_list = []
    for i in range(0,len(successor_states)):
        temporary_list = []
        for j in range(0,len(successor_states[0])):
            temporary_list = temporary_list + successor_states[i][j]
        printable_successor_states.append(temporary_list)

    return successor_states

def solve(initial_board):

    temp_list = []
    initial_board_2d = []
    for i in range(0,len(initial_board)):
        temp_list.append(initial_board[i])
        if(i%5 == 4 ):
            initial_board_2d.append(temp_list)
            temp_list = []



    valid_moves_set = {0:'R1',1:'L1',2:'U1',3:'D1',4:'R2',5:'L2',6:'U2',7:'D2',8:'R3',9:'L3',10:'U3',11:'D3',12:'R4',13:'L4',14:'U4',15:'D4',16:'R5',17:'L5',18:'U5',19:'D5',20:'Oc',21:'Occ',22:'Ic',23:'Icc'}
    goal_state = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    current_state = initial_board_2d
    list_of_moves = []
    lowest_heuristics = 1000
    chosen_move_index = 0
    visited_states = []
    visited_states.append(current_state)
    j = 0

    while(current_state != goal_state):
        successors_list = successors(current_state)

        for i in range(0,len(successors_list)):
            if successors_list[i] == visited_states[j]:
                pass
            else:
                a = getBoardManhattanDistance(successors_list[i])
                if(lowest_heuristics > a):
                    lowest_heuristics = a
                    chosen_move_index = i

        current_state = successors_list[chosen_move_index]
        visited_states.append(current_state)
        list_of_moves.append(valid_moves_set[chosen_move_index])

        if(len(list_of_moves) > 100):
            j = j + 1
            list_of_moves = []
            current_state = initial_board_2d

    return list_of_moves

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
