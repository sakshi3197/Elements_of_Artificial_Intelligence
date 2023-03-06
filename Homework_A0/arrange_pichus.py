#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [PUT YOUR NAME AND USERNAME HERE]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    pichu_count = count_pichus(initial_house_map)
    while (pichu_count != k):


        possible_states = successors(initial_house_map)

        for j in range(0,len(possible_states)):
            if(len(fringe)!= 0 and possible_states[j] in fringe):
                break
            check_state = checkState(possible_states[j])
            if(check_state == True):
                initial_house_map = possible_states[j]
                fringe.append(possible_states[j])
                break
                
        pichu_count = count_pichus(initial_house_map)

    return (initial_house_map,True)

def checkState(state):

    try:
        number_of_pichus = count_pichus(state[0])

        pichu_locations = []
        #print(state)
        for i in range(0, len(state)):
            for j in range(0, len(state[0])):
                if state[i][j] == "p":
                    pichu_locations.append([i,j])

        total_pichus = len(pichu_locations)

        for i in range(0, total_pichus):
                x_location = pichu_locations[i][0]
                y_location = pichu_locations[i][1]


                for rows in range(0, len(state)):
                    if(state[rows][y_location] == 'X'):
                        break
                    if(state[rows][y_location] == 'p'):
                        if(rows != pichu_locations[i][0]):
                            flag = 0
                            for a in range(rows,pichu_locations[i][0]):
                                if(state[a][y_location] == "X"):
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                            else:
                                return False
                    #elif(state[rows][y_location] == '.'):
                     #   state[rows][y_location] = "*"
                for columns in range(0, len(state[0])):
                    if(state[x_location][columns] == 'X'):
                        break
                    if(state[x_location][columns] == 'p'):
                        if(columns != pichu_locations[i][1]):
                            flag = 0
                            for a in range(columns,pichu_locations[i][1]):
                                if(state[x_location][a] == "X"):
                                    flag = 1
                                    break
                            if flag == 1:
                                break
                            else:
                                return False

                    #elif(state[x_location][columns] == '.'):
                     #   state[x_location][columns] = "*"

                m = x_location
                n = y_location
                while (m < len(state) and n < len(state[0])):

                    if(state[m][n] == "X"):
                        break
                    if(state[m][n] == 'p'):
                        if(m != pichu_locations[i][0] and n!=pichu_locations[i][1]):#############[i][0...changed this 1 to 0]
                            flag = 0
                            g = n
                            h = m
                            while ( g != pichu_locations[i][0] and h != pichu_locations[i][1]):
                                if(state[g][h] == "X"):
                                    flag = 1
                                    break
                                g = g + 1
                                h = h + 1
                            if flag == 1:
                                break
                            else:
                                return False

                    #elif(state[m][n] == '.'):
                     #   state[m][n] = "*"
                    m = m + 1
                    n = n + 1


                m = x_location
                n = y_location
                while (m >= 0 and n >=0):

                    if(state[m][n] == "X"):
                        break
                    if(state[m][n] == 'p'):
                        if(m != pichu_locations[i][0] and n!=pichu_locations[i][1]):
                            flag = 0
                            g = n
                            h = m
                            while ( g != pichu_locations[i][0] and h != pichu_locations[i][1]):
                                if(state[g][h] == "X"):
                                    flag = 1
                                    break
                                g = g + 1
                                h = h + 1
                            if flag == 1:
                                break
                            else:
                                return False

                    #elif(state[m][n] == '.'):
                     #   state[m][n] = "*"
                    m = m - 1
                    n = n - 1


                m = y_location
                n = x_location

                state_backup = [[None for _ in range(len(state))] for _ in range(len(state[0]))]
                for p in range(len(state)):
                    for q in range(len(state[0])):
                        state_backup[q][p] = state[p][q]

                while (m < len(state_backup) and n < len(state_backup[0])):

                    if(state_backup[m][n] == "X"):
                        break
                    if(state_backup[m][n] == 'p'):
                        if(m != pichu_locations[i][1] and n!=pichu_locations[i][0]):

                            flag = 1
                            g = m
                            h = n
                            while ( h != pichu_locations[i][1] and g != pichu_locations[i][0]):
                                if(state_backup[g][h] == "X"):
                                    flag = 0
                                    break
                                g = g + 1
                                h = h + 1
                            if flag == 0:
                                break
                            else:
                                return False

                    #elif(state_backup[m][n] == '.'):
                     #   state_backup[m][n] = "*"
                    m = m + 1
                    n = n + 1

                m = y_location
                n = x_location
                while (m >= 0 and n >=0):

                    if(state_backup[m][n] == "X"):
                        break
                    if(state_backup[m][n] == 'p'):
                        if(m != pichu_locations[i][1] and n!=pichu_locations[i][0]):

                            flag = 0
                            g = m
                            h = n
                            while ( h != pichu_locations[i][1] and g != pichu_locations[i][0]):
                                if(state_backup[g][h] == "X"):
                                    flag = 1
                                    break
                                g = g + 1
                                h = h + 1
                            if flag == 1:
                                break
                            else:
                                return False

                    #elif(state_backup[m][n] == '.'):
                     #   state_backup[m][n] = "*"

                    m = m - 1
                    n = n - 1

                for p in range(len(state_backup)):
                    for q in range(len(state_backup[0])):
                        state[q][p] = state_backup[p][q]



        for c in range(0,len(state)-1):
            for d in range(0,len(state[0])-2):
                if(state[c][d] == 'p' and state[c][d+1] == 'p'):
                    return False
                if(state[c][d] == 'p' and state[c][d+2] == 'p'):
                    return False
                if(c>0 and d > 0):
                    if(state[c][d] == 'p' and state[c-1][d-1] == 'p'):
                        return False
                    if(state[c][d] == 'p' and state[c+1][d-1] == 'p'):
                        return False
                    if(state[c][d] == 'p' and state[c-1][d+1] == 'p'):
                        return False
                if(state[c][d] == 'p' and state[c+1][d+1] == 'p'):
                    return False


        return True
    except:
        return False

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")
