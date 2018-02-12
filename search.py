# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
     

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  #Initializing variables
  fringe = util.Stack()
  #Creating visited list
  visited = []
  #Pushing start state to Stack
  fringe.push((problem.getStartState(), []))
  #Adding start state to visited list
  visited.append(problem.getStartState())
  
  #Popping point from the stack
  while fringe.isEmpty() == False:
      state, actions = fringe.pop()
      #Getting successor nodes
      for next in problem.getSuccessors(state):
        newstate = next[0]
        newdirection = next[1]
        #Pushing successor nodes to the stack and appending to visited
        if newstate not in visited:
            if problem.isGoalState(newstate):
                return actions + [newdirection]        
            else:
                fringe.push((newstate, actions + [newdirection]))
                visited.append(newstate)

  util.raiseNotDefined()

def breadthFirstSearch(problem):
  #Initializing variables
  fringe = util.Queue()
  #Creating visited list
  visited = []
  #Pushing start state to Stack
  fringe.push((problem.getStartState(), []))
  #Adding start state to visited list
  visited.append(problem.getStartState())
  
  #Popping point from the queue
  while fringe.isEmpty() == False:
      state, actions = fringe.pop()
      #Getting successor nodes
      for next in problem.getSuccessors(state):
        newstate = next[0]
        newdirection = next[1]
        #Pushing successor nodes to the queue and appending to visited
        if newstate not in visited:
            if problem.isGoalState(newstate):
                return actions + [newdirection]        
            else:
                fringe.push((newstate, actions + [newdirection]))
                visited.append(newstate)

  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  #Update function to find node of least cost
  def update(fringe, item, priority):
    for index, (p, c, i) in enumerate(fringe.heap):
      if i[0] == item[0]:
          if p <= priority:
                break
          del fringe.heap[index]
          fringe.heap.append((priority, c, item))
          heapq.heapify(fringe.heap)
          break
    else:
      fringe.push(item, priority)
  #Initialize variables
  fringe = util.PriorityQueue()
  #Creating visited list
  visited = []
  fringe.push((problem.getStartState(), []), 0)
  visited.append(problem.getStartState())
  #Popping node from fringe
  while fringe.isEmpty() == False:
    state, actions = fringe.pop()
    if problem.isGoalState(state):
      return actions
    #Adding current node to visited list
    if state not in visited:
      visited.append(state)
    #Getting successors and finding the one of least cost using update function
    for next in problem.getSuccessors(state):
      newstate = next[0]
      newdirection = next[1]
      if newstate not in visited:
        update(fringe, (newstate, actions + [newdirection]), problem.getCostOfActions(actions+[newdirection]))
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  visited = []
  fringe = util.PriorityQueue()
  start = problem.getStartState()
  fringe.push((start, list()), heuristic(start, problem))

  while not fringe.isEmpty():
    state, actions = fringe.pop()

    if problem.isGoalState(state):
      return actions

    visited.append(state)

    for state, dir, cost in problem.getSuccessors(state):
      if state not in visited:
        newactions = actions + [dir]
        score = problem.getCostOfActions(newactions) + heuristic(state, problem)
        fringe.push( (state, newactions), score)

  return []

  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch