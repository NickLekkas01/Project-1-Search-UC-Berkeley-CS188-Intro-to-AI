# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def dfs_function(problem, current_state, action, Visited, Stack, Path):
    
    #If current state is the destination/goal state then put it in the list and return
    if(problem.isGoalState(current_state)):
        Path.append(action)
        return 1
    #if state is not visited make it visited, else return
    if current_state not in Visited:
        Visited.append(current_state)
    else:
        return 0
    #Push state in stack if it hasn't been visited before
    Stack.push(current_state)
    #Insert action in path to remember the movements
    if action is not 'NULL':
        Path.append(action)
    #Find succesors
    succ_list = problem.getSuccessors(current_state)
    for i in succ_list:
        #Do the same for the kids of this state
        #If functions returns 1 it found goal state, return
        if dfs_function(problem, i[0], i[1], Visited, Stack, Path) is 1:
            return 1
    #All kids searched, pop from stack
    Stack.pop()
    #and delete the last state from path since we don't need it
    del Path[-1]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    #List for visited states
    Visited = list()
    #Stack to implement dfs and save states in lifo
    Stack = util.Stack()
    #The path from start to goal
    Path = list()
    dfs_function(problem, state, 'NULL', Visited, Stack, Path)
    return Path
    util.raiseNotDefined()
   

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #starting position
    state = problem.getStartState()
    action = 'NULL'
    #list for visited states
    Visited = list()
    #queue to implement bfs and save states in fifo
    Queue = util.Queue()
    Path = list()
    #push first state in queue
    Queue.push([state, action, 'NULL'])
    tmp = [state, action, 'NULL']
    Visited.append(state)
    while( Queue.isEmpty() is False ):
        #tmp = [state, action, prev_state]
        tmp = Queue.pop()
        state = tmp[0]
        action = tmp[1]
        #if state is goal state the return and return Path
        if (problem.isGoalState(state) is True):
            break

        #Get the successors of this state
        succ_list = problem.getSuccessors(state)
        for i in succ_list:
            #For every successor if he is not visited make him visited and push him in the queue
            if i[0] not in Visited:
                Visited.append(i[0])
                Queue.push([i[0], i[1], tmp])
    
    #create a stack to insert data in it and find path of actions
    stack = util.Stack()
    #tmp2 = prev_state
    while(tmp[2] is not 'NULL'):
        #tmp[1] = action
        stack.push(tmp[1])
        #move to the previous state
        tmp = tmp[2]

    #Finally put data to Path and return it
    Path = list()
    while(not stack.isEmpty()):
        Path.append(stack.pop())
    return Path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    action = 'NULL'
    #List of indexes for the Visites List
    Visited_idx = list()
    #List of visited states
    Visited = list()
    #Priority Queue for the states to be sorted by priority
    PQueue = util.PriorityQueue()
    #Path to show actions
    Path = list()
    count = 0
    #list has state, action, prev_state, step
    PQueue.push([state, action, 'NULL', count], count)
    tmp = [state, action, 'NULL', count]
    Visited_idx.append(state)
    Visited.append(-1)
    while( PQueue.isEmpty() is False ):
        #tmp = [state, action, prev_state, count]
        tmp = PQueue.pop()
        state = tmp[0]
        action = tmp[1]
        current_count = tmp[3]
        #if current state is goal state return
        if (problem.isGoalState(state) is True):
            break

        #get successors of this state
        succ_list = problem.getSuccessors(state)
        for i in succ_list:
            #if state is not Visited make it visited and push it on Priority Queue with priority = current_count + new_count 
            #else if count is smaller than the already visited state save the smaller count
            if not i[0] in Visited_idx:
                Visited_idx.append(i[0])
                Visited.append(current_count+i[2])
                PQueue.push([i[0], i[1], tmp, current_count+i[2]] , current_count + i[2])
            elif  current_count+i[2]  < Visited[Visited_idx.index(i[0])]:
                Visited[Visited_idx.index(i[0])] = current_count+i[2]
                PQueue.push([i[0], i[1], tmp, current_count+i[2]] , current_count + i[2])
                
    #create a stack to insert data in it and find path of actions
    stack = util.Stack()
    #tmp2 = prev_state
    while(tmp[2] is not 'NULL'):
        #tmp[1] = action
        stack.push(tmp[1])
        #move to the previous state
        tmp = tmp[2]

    #Finally put data to Path and return it
    Path = list()
    while(not stack.isEmpty()):
        Path.append(stack.pop())
    return Path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    state = problem.getStartState()
    action = 'NULL'
    #List of indexes for the Visites List
    Visited_idx = list()
    #List of visited states
    Visited = list()
    #Priority Queue for the states to be sorted by priority
    PQueue = util.PriorityQueue()
    #Path to show actions
    Path = list()
    count = 0
    #list has state, action, prev_state, step
    PQueue.push([state, action, 'NULL', count], count)
    tmp = [state, action, 'NULL', count]
    Visited_idx.append(state)
    Visited.append(-1)
    while( PQueue.isEmpty() is False ):
        #tmp = [state, action, prev_state, count]
        tmp = PQueue.pop()
        state = tmp[0]
        action = tmp[1]
        current_count = tmp[3]
        #if current state is goal state return
        if (problem.isGoalState(state) is True):
            break

        #get successors of this state
        succ_list = problem.getSuccessors(state)
        for i in succ_list:
            #if state is not Visited make it visited and push it on Priority Queue with priority = current_count + new_count + heuristic
            #else if count is smaller than the already visited state save the smaller count
            if not i[0] in Visited_idx:
                Visited_idx.append(i[0])
                Visited.append(current_count+i[2])
                PQueue.push([i[0], i[1], tmp, current_count+i[2]] , current_count + i[2] + heuristic(i[0], problem))
            elif  current_count+i[2]  < Visited[Visited_idx.index(i[0])]:
                Visited[Visited_idx.index(i[0])] = current_count+i[2]
                PQueue.push([i[0], i[1], tmp, current_count+i[2]] , current_count + i[2] + heuristic(i[0], problem))

    #create a stack to insert data in it and find path of actions
    stack = util.Stack()
    #tmp2 = prev_state
    while(tmp[2] is not 'NULL'):
        #tmp[1] = action
        stack.push(tmp[1])
        #move to the previous state
        tmp = tmp[2]

    #Finally put data to Path and return it
    Path = list()
    while(not stack.isEmpty()):
        Path.append(stack.pop())
    return Path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
