#
# raichu.py : Play the game of Raichu
#
# Sakshi Sitoot(ssitoot@iu.edu), Chaitrali Ghanekar (chghanek@iu.edu), Shreya Mariyam Varghese (svarghe@iu.edu)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import numpy as np
import sys
import time

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def board_to_matrix(board, N):
    return np.array(list(board)).reshape(N, N)

def get_unique(board):
    return np.unique(board, return_counts = True)

def find_players(board, player):
    return np.where(board == player)

def combine_row_column(row, col):
    return np.column_stack((row, col))

def numpy_add(param1, param2):
    return np.add(param1, param2)

def build_numpy_array(param1, param2):
    return np.array([param1, param2])

def check_if_valid_move(location, N):
    if(N > location[0] >= 0 and N > location[1] >= 0 ):
        return True
    else:
        return False

def pichu_next_move_options(board, player):
    empty_place = '.'
    pichu_possible_boards = []
    pichu_pikachu_raichu_moves = []
    total_number_of_jumps = 0

    #initializing the variables of all the players
    if player == 'w':
        front = 1
        back = -1
        end = N - 1

        raichu = '@'
        pikachu = 'W'
        pichu = 'w'

        raichu_opponent = '$'
        pikachu_opponent = 'B'
        pichu_opponent = 'b'

    if player == 'b':
        front = 1
        back = -1
        end = N - 1

        raichu = '$'
        pikachu = 'B'
        pichu = 'b'

        raichu_opponent = '@'
        pikachu_opponent = 'W'
        pichu_opponent = 'w'

    #Finding all the pichus on the board
    location_row, location_column = find_players(board, pichu)
    pichus_on_board = np.column_stack((location_row,location_column))

    for individual_pichu_location in pichus_on_board:
        # check one block ahead in all the diagonal directions
        one_ahead_diagonal_left = build_numpy_array(front*1,1)
        one_ahead_diagonal_right = build_numpy_array(front*1,-1)
        one_ahead_diagonal = np.vstack([numpy_add(individual_pichu_location, one_ahead_diagonal_left),
                            numpy_add(individual_pichu_location, one_ahead_diagonal_right)])
        one_ahead_diagonal_moves = [tuple(next_step_to_take) for next_step_to_take in one_ahead_diagonal]

        # if the place is empty adding it to the possible options
        blank = []
        for next_step_to_take in one_ahead_diagonal_moves:
            if check_if_valid_move(next_step_to_take, N) and board[next_step_to_take]==empty_place:
                blank=next_step_to_take

                updated_board = board.copy()
                updated_board[tuple(individual_pichu_location)]=empty_place

                update_location_row = next_step_to_take[0]
                if update_location_row == end:
                    updated_board[next_step_to_take]=raichu
                else:
                    updated_board[next_step_to_take]=pichu
                pichu_possible_boards.append(updated_board)

        #checking two block ahead in the diagonal directions
        two_ahead_diagonal_left = build_numpy_array(front*2,2)
        two_ahead_diagonal_right = build_numpy_array(front*2,-2)
        two_ahead_diagonal = np.vstack([numpy_add(individual_pichu_location, two_ahead_diagonal_left),
                            numpy_add(individual_pichu_location, two_ahead_diagonal_right)])
        one_two_ahead_diagonal = np.concatenate((one_ahead_diagonal, two_ahead_diagonal), axis = 1).reshape(-1, 2,2)
        one_two_ahead_diagonal_next_steps = [[tuple(next_step_to_take[0]), tuple(next_step_to_take[1])] for next_step_to_take in one_two_ahead_diagonal]

        #if pichu can kill opponent pichu and jump over to an empty place, adding such options to the possible moves list

        for next_step_to_take in one_two_ahead_diagonal_next_steps:
            if check_if_valid_move(next_step_to_take[1], N):
                if pichu_opponent + empty_place == board[next_step_to_take[0]]+board[next_step_to_take[1]]:
                    check_jump = True
                else:
                    check_jump = False

                if check_jump == True:
                    pichu_after_jump_location =next_step_to_take[1]
                    updated_board = board.copy()
                    updated_board[tuple(individual_pichu_location)]=empty_place
                    updated_board[next_step_to_take[0]]=empty_place

                    update_location_row = pichu_after_jump_location[0]
                    if update_location_row == end:
                        updated_board[pichu_after_jump_location]=raichu
                    else:
                        updated_board[pichu_after_jump_location]=pichu

                    pichu_possible_boards.append(updated_board)
                    total_number_of_jumps = total_number_of_jumps + 1


    return pichu_possible_boards, total_number_of_jumps

def pikachu_next_move_options(board, player):
    empty_place = '.'
    pikachu_possible_boards = []
    pikachu_scope = 3

    pichu_pikachu_raichu_moves = []

    total_number_of_jumps = 0


    #initializing the variables of all the players
    if player == 'w':
        front = 1
        back = -1
        end = N - 1

        raichu = '@'
        pikachu = 'W'
        pichu = 'w'

        raichu_opponent = '$'
        pikachu_opponent = 'B'
        pichu_opponent = 'b'

    if player == 'b':
        front = 1
        back = -1
        end = N - 1

        raichu = '$'
        pikachu = 'B'
        pichu = 'b'

        raichu_opponent = '@'
        pikachu_opponent = 'W'
        pichu_opponent = 'w'

    #finding all the pikachus on the board
    location_row, location_column = find_players(board, pikachu)
    combined_pikachus = combine_row_column(location_row, location_column)

    forward_left_right_moves = []
    front_steps = []
    right_steps = []
    left_steps = []

    move_range = 3
    for i in range(1, pikachu_scope+1):
        front_steps.append((i*front,0))
    for i in range(1, pikachu_scope+1):
        right_steps.append((0,i))
    for i in range(1, pikachu_scope+1):
        left_steps.append((0,i*-1))
    forward_left_right_moves.append(front_steps)
    forward_left_right_moves.append(right_steps)
    forward_left_right_moves.append(left_steps)

    #moving the pikachus to empty places
    step_one_two = []
    step_one_two.append(front_steps[:2])
    step_one_two.append(left_steps[:2])
    step_one_two.append(right_steps[:2])

    location_one_two = []
    for i in range(len(combined_pikachus)):
        loc = numpy_add(combined_pikachus[i], step_one_two)
        location_one_two.append([[tuple(m) for m in loc[i]] for i in range(len(step_one_two))])

    for single_pik, individual_pikachu_location in enumerate(location_one_two):
        single_pikachu = tuple(combined_pikachus[single_pik])
        for way in individual_pikachu_location:
            track = []
            for next_step_to_take in way:
                if check_if_valid_move(next_step_to_take, N):
                    track.append(next_step_to_take)
            check_board =[board[track[m]] for m in range(len(track))]
            for k , step in enumerate(check_board):
                if step ==empty_place:
                    updated_board = board.copy()
                    updated_board[single_pikachu]=empty_place

                    update_location_row = track[k][0]
                    if update_location_row == end:
                        updated_board[track[k]]=raichu
                    else:
                        updated_board[track[k]]=pikachu
                    pikachu_possible_boards.append(updated_board)
                else:
                    break


    location_one_two_three = []
    for i in range(len(combined_pikachus)):
        loc = numpy_add(combined_pikachus[i], forward_left_right_moves)
        location_one_two_three.append([[tuple(m) for m in loc[i]] for i in range(len(forward_left_right_moves))])

    for i, individual_pikachu_location in enumerate(location_one_two_three):
        single_pikachu = tuple(combined_pikachus[i])
        for way in individual_pikachu_location:
            track = []
            for next_step_to_take in way:
                if check_if_valid_move(next_step_to_take, N):
                    track.append(next_step_to_take)
            check_board =[board[track[m]] for m in range(len(track))]
            try:
                if check_board[0] in pichu_opponent+pikachu_opponent and check_board[1] ==empty_place:
                    updated_board = board.copy()
                    updated_board[single_pikachu]=empty_place
                    updated_board[track[0]]=empty_place

                    update_location_row = track[1][0]
                    if update_location_row == end:
                        updated_board[track[1]]=raichu
                    else:
                        updated_board[track[1]]=pikachu
                    pikachu_possible_boards.append(updated_board)
                    total_number_of_jumps = total_number_of_jumps + 1
            except:
                pass

            try:
                if check_board[0] in pichu_opponent+pikachu_opponent and check_board[1]==empty_place and check_board[2]==empty_place:
                    updated_board = board.copy()
                    updated_board[single_pikachu]=empty_place
                    updated_board[track[0]]=empty_place

                    update_location_row = track[2][0]
                    if update_location_row == end:
                        updated_board[track[2]]=raichu
                    else:
                        updated_board[track[2]]=pikachu
                    pikachu_possible_boards.append(updated_board)
                    total_number_of_jumps = total_number_of_jumps + 1
            except:
                pass

            try:
                if check_board[0] == empty_place and check_board[1] in pichu_opponent+pikachu_opponent and check_board[2]==empty_place:
                    updated_board = board.copy()
                    updated_board[single_pikachu]=empty_place
                    updated_board[track[1]]=empty_place

                    update_location_row = track[2][0]
                    if update_location_row == end:
                        updated_board[track[2]]=raichu
                    else:
                        updated_board[track[2]]=pikachu
                    pikachu_possible_boards.append(updated_board)
                    total_number_of_jumps = total_number_of_jumps + 1
            except:
                pass
    return pikachu_possible_boards, total_number_of_jumps

def raichu_next_move_options(board, player):
    empty_place = '.'
    individual_raichu_locationsible_boards = []
    pichu_pikachu_raichu_moves = []
    total_number_of_jumps = 0

    #initializing the variables of all the players
    if player == 'w':
        front = 1
        back = -1
        end = N - 1

        raichu = '@'
        pikachu = 'W'
        pichu = 'w'

        raichu_opponent = '$'
        pikachu_opponent = 'B'
        pichu_opponent = 'b'

    if player == 'b':
        front = 1
        back = -1
        end = N - 1

        raichu = '$'
        pikachu = 'B'
        pichu = 'b'

        raichu_opponent = '@'
        pikachu_opponent = 'W'
        pichu_opponent = 'w'

    #finding all the raichus on the board
    location_row, location_column = np.where(board == raichu)
    combined_raichus = np.column_stack((location_row, location_column))
    forward_left_right_moves = []
    front_steps = []
    back_steps = []
    right_steps = []
    left_steps = []
    diagonal_front_right = []
    diagonal_back_right = []
    diagonal_back_left = []
    diagonal_front_left = []

    move_range = N
    for i in range(1, N):
        front_steps.append((front*i,0))
    for i in range(1, N):
        back_steps.append((back*i, 0))
    for i in range(1, N):
        right_steps.append((0,i))
    for i in range(1, N):
        left_steps.append((0,-1*i))
    for i in range(1, N):
        diagonal_back_right.append((back*i, i))
    for i in range(1, N):
        diagonal_front_right.append((front*i,i) )
    for i in range(1, N):
        diagonal_back_left.append((back*i, -1*i))
    for i in range(1, N):
        diagonal_front_left.append((front*i, -1*i))
    forward_left_right_moves.append(front_steps)
    forward_left_right_moves.append(back_steps)
    forward_left_right_moves.append(right_steps)
    forward_left_right_moves.append(left_steps)
    forward_left_right_moves.append(diagonal_back_right)
    forward_left_right_moves.append(diagonal_front_right)
    forward_left_right_moves.append(diagonal_back_left)
    forward_left_right_moves.append(diagonal_front_left)


    locations_total = []
    for individual_raichu_location in combined_raichus:
        loc = np.add(individual_raichu_location, forward_left_right_moves)
        locations_total.append([[tuple(m) for m in loc[i]] for i in range(len(forward_left_right_moves))])


    for m, individual_raichu_location in enumerate(locations_total):
        current_raichu = tuple(combined_raichus[m])
        for way in individual_raichu_location:
            track = []
            for next_step_to_take in way:
                if check_if_valid_move(next_step_to_take, N):
                    track.append(next_step_to_take)
            check_board =[board[track[n]] for n in range(len(track))]
            for j , step in enumerate(check_board):
                if step ==empty_place:
                    updated_board = board.copy()
                    updated_board[current_raichu]=empty_place
                    updated_board[track[j]]=raichu
                    individual_raichu_locationsible_boards.append(updated_board)
                else:
                    break
    for m, individual_raichu_location in enumerate(locations_total):
        current_raichu = tuple(combined_raichus[m])
        for way in individual_raichu_location:
            track = []
            for next_step_to_take in way:
                if check_if_valid_move(next_step_to_take, N):
                    track.append(next_step_to_take)
            check_board =[board[track[i]] for i in range(len(track))]


            for move_board in check_board:
                if move_board in pichu_opponent+pikachu_opponent+raichu_opponent:
                    opponent_one = check_board.index(move_board)
                    prior_opponent_one = check_board[:opponent_one]
                    was_empty_place = all([m == empty_place for m in prior_opponent_one])
                    if not was_empty_place:
                        break
                    else:
                        now = check_board[opponent_one:]
                        if len(now)==1:
                            break
                        else:
                            for i, move_board in enumerate(now[1:],1):
                                if move_board == empty_place:
                                    updated_board = board.copy()
                                    updated_board[current_raichu]=empty_place
                                    updated_board[track[opponent_one]]=empty_place
                                    updated_board[track[opponent_one+i]]=raichu
                                    individual_raichu_locationsible_boards.append(updated_board)
                                    total_number_of_jumps = total_number_of_jumps + 1
                                else:
                                    break
                        break

    return individual_raichu_locationsible_boards, total_number_of_jumps

#appending all the possible states to the main list of successor states
def successors(board, player):

    pichu_pikachu_raichu_moves = []
    pichu_pikachu_raichu_moves.append(pichu_next_move_options(board, player)[0])
    pichu_pikachu_raichu_moves.append(pikachu_next_move_options(board, player)[0])
    pichu_pikachu_raichu_moves.append(raichu_next_move_options(board, player)[0])
    pichu_pikachu_raichu_moves = [board for coin in pichu_pikachu_raichu_moves for board in coin]
    return pichu_pikachu_raichu_moves

def two_level_traversal(board, player):

    #setting both white and black players
    if player == 'w':
        opponent_player = 'b'
    if player =='b':
        opponent_player ='w'
    levels = []
    # the root vertex will be the initial board and the structure will be(board, depth, parent state)
    level = 0
    levels.append([[board, level, 'NA', float('-inf')]])

    level = 1
    #choosing player's turn
    if level % 2 == 1:
        turn = player
    else:
        turn = opponent_player
    previous_boards = [vertex[0] for vertex in levels[level-1]]

    d_nodes = []
    for n, parent_board in enumerate(previous_boards):
        d_nodes.append([[successor_state, level, n, float('inf')] for successor_state in successors(parent_board, turn)])
    levels.append(d_nodes)
    return levels

def is_end_state(board, player):
    # total number of player pieces
    if player == 'w':
        maximum_participant = 'w'
        minimum_participant = 'b'

    if player == 'b':
        maximum_participant = 'b'
        min_plyaer = 'w'

    if maximum_participant == 'w':
        maximum_coins='wW@'
        minimum_coins = 'bB$'

    if maximum_participant == 'b':
        maximum_coins = 'bB$'
        minimum_coins = 'wW@'


    distinct, numbers = np.unique(board, return_counts = True)
    zipped = zip(distinct, numbers)
    total_coins_playing = dict(zipped)

    maximum = 0
    for coin in maximum_coins:
        try:
            maximum= maximum + total_coins_playing[coin]
        except:
            continue

    minimum = 0
    for coin in minimum_coins:
        try:
            minimum = minimum + total_coins_playing[coin]
        except:
            continue
    return (maximum == 0  or minimum ==0, minimum, maximum)

def check_for_end_states(levels):
#checking leaf nodes for end states
    winner = []
    terminal_state_position = len(levels)-1
    for m, batch in enumerate(levels[terminal_state_position]):
        for n, vertex in enumerate(batch):
            is_end = is_end_state(vertex[0], player)
            if is_end[0] and is_end[1]==0:
                victory_state = levels[terminal_state_position][m][n][0].flatten()
                return True, ''.join([str(x) for x in victory_state])
    return False, ''


def append_to_graph(levels, level, player, opponent_player):

    if level % 2 ==0:
        maximum_graph_vertex = True
        positive_negative_infinity = float('-inf')
        turn = opponent_player
    else:
        maximum_graph_vertex = False
        positive_negative_infinity = float('inf')
        turn = player

    d_nodes = []
    for batch in levels[level-1]:
        for i, board in enumerate([m[0] for m in batch]):
            d_nodes.append([[successor_state, level, i, positive_negative_infinity]for successor_state in successors(board, turn)])
    levels.append(d_nodes)
    return levels

def coin_points(board, player):

    if player == 'w':
        maximum_participant = 'w'
        minimum_participant = 'b'

    if player == 'b':
        maximum_participant = 'b'
        minimum_participant = 'w'

    if maximum_participant == 'w':
        maximum_coins='wW@'
        minimum_coins = 'bB$'

    if maximum_participant == 'b':
        maximum_coins = 'bB$'
        minimum_coins = 'wW@'


    distinct, numbers = np.unique(board, return_counts = True)
    total_coins_playing = dict(zip(distinct, numbers))
    maximum_points_coins = 0
    points = [1,2,10]

    for i, coin in enumerate(maximum_coins):
        try:
            maximum_points_coins += points[i]*total_coins_playing[coin]
        except:
            continue
    minimum_points_coins = 0
    points = [1,2,10]

    for i, coin in enumerate(minimum_coins):
        try:
            minimum_points_coins += points[i]*total_coins_playing[coin]
        except:
            continue
    return maximum_points_coins-minimum_points_coins


def next_step_jump_options_total(board, player):

    jump_states = []

    jump_states.append(pichu_next_move_options(board, player)[1])
    jump_states.append(pikachu_next_move_options(board, player)[1])
    jump_states.append(raichu_next_move_options(board, player)[1])

    return sum(jump_states)

def pi_pik_travel(board, player):

    if player == 'w':
        pichu = 'w'
        pikachu = 'W'

    if player == 'b':
        pichu = 'b'
        pikachu = 'B'

    location_row, location_column = np.where(((board == pichu) | (board == pikachu)))
    location_row
    if len(location_row)>0:
        result = []
        if player == 'w':
            for i in range(0, len(location_row)):
                result.append(i**2)

        if player == 'b':
            for i in range(0, len(location_row)):
                result.append((N-1-i)**2)
        return np.mean(result)
    else:
        return 0

def heuristic_evaluation(board, player, opponent_player):
    if player == 'w':
        raichu = '@'
    if player == 'b':
        raichu = '$'

    distinct, numbers = get_unique(board)
    if raichu in distinct:
        points = [12, 2, 1]
    else:
        points = [7, 2, 5]

    attributes = np.array([coin_points(board, player),
                        next_step_jump_options_total(board, player)-next_step_jump_options_total(board, opponent_player),
                        pi_pik_travel(board, player)-pi_pik_travel(board,opponent_player)])

    if attributes[0]>25:
        points = [2, 1, 12]

    if attributes[0]>35:
        points = [12, 1, 1]

    result = sum(attributes*points)
    return result

###  given (N, player (w or b), board, timelimit (sec)) return the next best next_step_to_take for the player
def find_best_move(board, N, player, timelimit):
    final_board = board

    while True:
        time.sleep(1)
        yield final_board

        #initializing the players
        if player == 'w':
            opponent_player = 'b'
        if player =='b':
            opponent_player ='w'

        board = board_to_matrix(board, N)
        # first two levels
        levels = two_level_traversal(board, player)
        #checking if there is a winning state
        is_winning_state = check_for_end_states(levels)
        if is_winning_state[0]:
            final_board = is_winning_state[1]
            print(final_board)
            return final_board

        else:
            level = len(levels)-1
            for i, batch in enumerate(levels[level]):
                group_max = [float('-inf'),i,'']
                for j, vertex in enumerate(batch):
                    vertex[3]=(heuristic_evaluation(vertex[0], player, opponent_player))
                    if vertex[3]> group_max[0]:
                        group_max = [vertex[3],i,j]

            choice = levels[level][group_max[1]][group_max[2]][0]
            final_board = ''.join([str(x) for x in choice.flatten()])

            #proceeding in case of no winning states
            level = len(levels)-1

            level = len(levels)
            h = 1

            for i in range(h):
                append_to_graph(levels,level, player, opponent_player)
                level = level + 1


            level = len(levels)-1
            evaluations = []
            for  m, batch in enumerate(levels[level]):
                group_min = [float('inf'),m,'']
                for n, vertex in enumerate(batch):
                    vertex[3]=(heuristic_evaluation(vertex[0], player, opponent_player))
                    if vertex[3]< group_min[0]:
                        group_min = [vertex[3],m,n]
                evaluations.append(group_min)

            max_of_mins = [m[0] for m in evaluations].index(max([m[0] for m in evaluations]))

            final_boards = levels[1][0][max_of_mins][0]
            final_board = ''.join([str(i) for i in final_boards.flatten()])
            print (final_board)
            return final_board

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best next_step_to_take for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for updated_board in find_best_move(board, N, player, timelimit):
        print(updated_board)
