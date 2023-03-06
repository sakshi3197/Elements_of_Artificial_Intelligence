# a0-release
Question 1

In this question, we are supposed to find a shortest route for pichu from its original position to the goal state '@'. The heuristic function that I have used to get the shortest path is Manhattan Distance. I have pre-computed the Manhattan Distances in a copy of the same house map matrix and kept it in a different matrix. So here we always check if pichu's current location is equal to the goal state. If so, we end the computation and return the path and count of steps required to reach.

Approach:

We have created a list of previous locations, move options, final visited list.
Various important lists in the code:
  ->previous locations: it holds all the previous locations which pichu has travelled.
  ->move options: this list holds all the coordinated of valid possible moves from pichu's current location
  ->final visited list: This list holds the final locations that pichu travelled from. This list if different from previous locations since here if there is a dead end in the path, then we back track and delete entries from final list.

At the last, we use the final visited list to compute the directions:L,R,U,D.
Based on the coordinates we compute the final shortest path to the destination node and return the path along with the total number of steps required to reach there.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Question 2

Approach:

In question 2 we are expected to return a map holding 'k' pichus such that they do not attack each other. So I have used the predefined methods to do so and, I have written another method called checkState(house_map) which will be majorly used. So, firstly we are getting the total number of pichus and then we start a while lopp which runs until the total number of pichus in the house map is not equal to k(expected output). Now, we use the successor function which returns the possible states after the present one. So we have passed these possible successor states in a loop to our method checkState.

checkState(house_map):
  This method returns False or True values depending on the location of the pichus in that particular state. This method basically records the locations of all the pichus in the state and stores it in a list. Now, in a loop we check the attack cases for all the pichus.

Cases being checked:
  -> Horizontal Check: We firstly check if whether there is a pichu in the same row as that of i'th pichu. If so we direclty return False.
  -> Vertical Check: We check if there is a pichu in the same column as that of the ith pichu.
  -> Diagonals: Now we check for all the diagonals in all the 4 directions (North-East, South-East, North-West, South-West)

Terms:

Successor Function: Successor function basically returns all the possible states after the current state. In this example particularly, the successor function gives all the states having k + 1 pichus.
Initial State: Initial State is the state having single or no pichus. We have to modify this state to get the output.
Goal State: Goal state in this case is the state where we get all the k pichus in the map without attacking each other in horizontal, vertical or diagonal directions.


While checking all these conditions if we find an 'X' in between then we stop the search for a pichu in that direction since it is blocked by a Wall and wont attack in that direction.
In the solve method if the number of the pichus is equal to k, then we return the map and 'TRUE' else we return False.

Previously I used different approach in the checkState method. The problem in the previous approach was that it was not considering any 2 consecutive pichus if the row had an X at the star. Similar was happening for the columns as well.

We are adding all the selected possible states in the fringe so that we can go back in case if a map is not getting finalized. If next possible states are already in fringe then we skip those states.

At the last we return the tuple of final house_map and True or False depending on the result.

Alternative Code for the method checkState(house_map):

def checkState(state):
  number_of_pichus = count_pichus(state[0])
  pichu_locations = []
  for i in range(0, len(state)):
    for j in range(0, len(state[0])):
      if state[i][j] == "p":
        pichu_locations.append([i,j])
        total_pichus = len(pichu_locations)

        for r in range(0, total_pichus):

              x_location = pichu_locations[r][0]
              y_location = pichu_locations[r][1]
              ##Towards Left
              left_clearance = 0
              for left in range(x_location-1,-1):
                  if(state[left][y_location] == '#'):
                      left_clearance = 1
                      break
                  if(state[left][y_location] == 'p'):
                      return False
                  if(left == 0):
                      left_clearance = 1

              ##Towards Right
              right_clearance = 0
              for right in range(x_location+1, len(state)):

                  if(state[right][y_location] == '#'):
                      right_clearance = 1
                      break
                  if(state[right][y_location] == 'p'):
                      return False
                  if(right == len(state)-1 ):
                      right_clearance = 1

              ##Towards Up
              up_clearance = 0
              for up in range(y_location-1,-1):
                  if(state[x_location][up] == '#'):
                      up_clearance = 1
                      break
                  if(state[x_location][up] == 'p'):
                      return False
                  if(up == 0):
                      up_clearance = 1

              ##Towards Bottom
              bottom_clearance = 0
              for bottom in range(y_location + 1, len(state[0])):
                  if(state[x_location][bottom] == '#'):
                      bottom_clearance = 1
                      break
                  if(state[x_location][bottom] == 'p'):
                      return False
                  if(bottom == y_location - 1):
                      bottom_clearance = 1

              ##South_East check
              south_east_clearance = 0
              se_x = x_location + 1
              se_y = y_location + 1
              while(se_x < len(state) and se_y < len(state[0])):
                  if(state[se_x][se_y] == '#'):
                      south_east_clearance = 1
                      break
                  if(state[se_x][se_y] == 'p'):
                      return False
                  if (se_x == len(state)-1 or se_y == len(state[0]) -1 ):
                      south_east_clearance = 1
                  se_x = se_x + 1
                  se_y = se_y + 1
              ##North_East check
              north_east_clearance = 0
              ne_x = x_location - 1
              ne_y = y_location + 1
              while(ne_x >=0 and ne_y < len(state[0])):
                  if(state[ne_x][ne_y] == '#'):
                      north_east_clearance = 1
                      break
                  if(state[ne_x][ne_y] == 'p'):
                      return False
                  if(ne_x == 0 or ne_y == len(state[0]) - 1):
                      north_east_clearance = 1
                  ne_x = ne_x - 1
                  ne_y = ne_y + 1
              ##North_west check
              north_west_clearance = 0
              nw_x = x_location - 1
              nw_y = y_location - 1

              while(nw_x >=0 and nw_y >=0 ):

                  if(state[nw_x][nw_y] == '#'):
                      north_west_clearance = 1
                      break
                  if(state[nw_x][nw_y] == 'p'):
                      return False
                  if(nw_x == 0 or nw_y == 0):
                      north_west_clearance = 1
                  nw_x = nw_x - 1
                  nw_y = nw_y - 1
              ##South_west check
              south_west_clearance = 0
              sw_x = x_location + 1
              sw_y = y_location - 1
              while(sw_x < len(state) and sw_y >= 0):
                  if(state[sw_x][sw_y] == '#'):
                      south_west_clearance = 1
                      break
                  if(state[sw_x][sw_y] == 'p'):
                      return False
                  if(sw_x == 0 or sw_y == 0):
                      south_west_clearance = 1
                  sw_x = sw_x + 1
                  sw_y = sw_y - 1
              if((left_clearance == 0 or right_clearance == 0 or bottom_clearance == 0 or up_clearance == 0 or south_east_clearance == 0 or south_west_clearance == 0 or north_west_clearance == 0 or north_east_clearance == 0)):

                  return False
              else:
                  return True   
