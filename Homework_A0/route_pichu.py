#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]

        final_visited_list = []

        manhattan_distance = [[None for _ in range(len(house_map[0]))] for _ in range(len(house_map))]

        total_positions = 0
        for i in range(0,len(house_map)):
            for j in range(0,len(house_map[0])):
                if(house_map[i][j] == '@'):
                    goal_position_X, goal_position_Y = i, j
                if(house_map[i][j] == '.'):
                    total_positions = total_positions + 1

        for i in range(0,len(house_map)):
            for j in range(0,len(house_map[0])):
                manhattan_distance[i][j] = abs(i-goal_position_X) + abs(j-goal_position_Y)


        route = []
        route.append(pichu_loc)
        previous_locations = []
        previous_locations.append(pichu_loc)
        next_location = []
        move_options = []
        next_position = pichu_loc

        goal_position = (goal_position_X, goal_position_Y)
        positions_travelled = 0

        if (pichu_loc == goal_position):
            return -1

        #move_options = [[None for _ in range(4)] for _ in range(4)]

        x=0
        y=0
        min_manhattan_distance = total_positions

        #fringe=[(pichu_loc,0)]
        #(curr_move, curr_dist)=fringe.pop()


        while(positions_travelled<total_positions):

            final_visited_list.append(pichu_loc)
            fringe=[(pichu_loc,0)]
            (curr_move, curr_dist)=fringe.pop()

            move_options = moves(house_map,*curr_move)
            #print("Here move options are:",move_options)
            next_x = 0
            next_y = 0

            #print("Move Options:",move_options, "  len(move_options):",len(move_options))
            if(next_position == goal_position):
                break
            if(len(move_options) > 1):

                options_from_visited_locations = 0

                length = len(move_options)
                i = 0
                m = 0
                while i < length:
                    i = i + 1

                    #print("Previous_locations are:",previous_locations)
                    #print("Move_options:",move_options,"   Value of m:",m)
                    if(move_options[m] in previous_locations):

                        move_options.remove(move_options[m])
                        #print("Move_options after deleting:",move_options)
                        #print("DELETED !!!!!!!!!!!!!!!!!!!!!!")
                        options_from_visited_locations = options_from_visited_locations + 1
                    else:
                        #print("M is incremented")
                        m = m + 1

                #print("Length of move_options after removing repeated nodes:", move_options)
                if(len(move_options) == 0):
                    return -1

                for i in range(0,len(move_options)):

                    #print("move_options[i]:",move_options[i])

                    x = move_options[i][0]
                    y = move_options[i][1]
                    #print("X:",x ,"  Y:",y)

                    #print("min_manhattan_distance:",min_manhattan_distance)
                    #print("manhattan_distance[x][y]",manhattan_distance[x][y])

                    if(min_manhattan_distance > manhattan_distance[x][y] or len(move_options) == 1):
                        min_manhattan_distance = manhattan_distance[x][y]
                        next_x = x
                        next_y = y

                    #   print("manhattan_distance[x][y] here in the other if",manhattan_distance[x][y])

                    #    print("next_x:",next_x,"")
                    #    print("next_y:",next_y,"")

                next_position = (next_x, next_y)
                #print("Setting Next Location:",next_position)
                move_options = []
                previous_locations.append(next_position)
                positions_travelled = positions_travelled + 1
                pichu_loc = next_position
            elif(len(move_options) == 0):
                #print("Here1")
                return -1
            else:
                if move_options[0] in previous_locations:
                    #print("Here2")
                    #print("move_options:",move_options)

                    return -1
                else:
                    #print("Here3 in else")

                    next_position = move_options[0]
                    previous_locations.append(move_options[0])
                    move_options = []
                    positions_travelled = positions_travelled + 1
                    pichu_loc = next_position

        print(final_visited_list)
        j = 1
        move = ""
        final_count = 0
        for i in range(0,len(final_visited_list)-1):

            x = final_visited_list[i][0]
            y = final_visited_list[i][1]

            x1 = final_visited_list[j][0]
            y1 = final_visited_list[j][1]

            j = j + 1

            res_x = x1 - x
            res_y = y1 - y

            if(res_x > 0 and res_y == 0):
                move = move + "D"
                final_count = final_count + 1
            if(res_x < 0 and res_y == 0):
                move = move + "U"
                final_count = final_count + 1
            if(res_x == 0 and res_y > 0):
                move = move + "R"
                final_count = final_count + 1
            if(res_x == 0 and res_y < 0):
                move = move + "L"
                final_count = final_count + 1

        return (final_count, move)

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])
