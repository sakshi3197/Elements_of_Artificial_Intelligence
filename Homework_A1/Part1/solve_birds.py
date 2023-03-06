#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Kenny Lawrence Swamy kenswamy, Krishna Teja Jillelamudi kjillela, Sakshi Sitoot ssitoot
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
from queue import PriorityQueue

N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
def h(state):
    th = 0
    for i in range(N):
        th += abs((i+1) - state[i])
    return th

#########
#
# THE ALGORITHM:

def solve(initial_state):
    fringe = PriorityQueue()
    H, G = 0, 0
    visited_states = []
    fringe.put((H+G, initial_state, [], (H, G)))

    while fringe.qsize() > 0:
        (cost, state, path, (hs, gs)) = fringe.get()

        if is_goal(state):
            return path+[state, ]

        visited_states.append(state)
        gs += 1

        for s in successors(state):
            if s not in visited_states:
                hs = h(state)
                fringe.put((hs+gs, s, path+[state], (hs, gs)))

    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))
