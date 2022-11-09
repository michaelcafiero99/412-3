# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """


        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
         successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        min_dist_G = 5000
        min_dist_F = 5000
        min_dist_P = 5000

        coordinates_ghost = []
        coordinates_power = successorGameState.getCapsules()
        coordinates_food = newFood.asList()

        for i in range(len(newGhostStates)):
            thisGhost = newGhostStates[i]
            coordinates = thisGhost.getPosition()
            coordinates_ghost.append(coordinates)

        for i in range(len(coordinates_food)):
            this_coord = coordinates_food[i]
            if not manhattanDistance(newPos, this_coord) >= min_dist_F:
                min_dist_F = manhattanDistance(newPos, this_coord)
            else:
                continue

        for i in range(len(coordinates_ghost)):
            this_ghost = coordinates_ghost[i]

            if not manhattanDistance(newPos, this_ghost) >= min_dist_P:
                min_dist_G = manhattanDistance(newPos, this_ghost)
            else:
                continue

        for i in range(len(coordinates_power)):
            this_power = coordinates_power[i]
            if not manhattanDistance(newPos, this_power) >= min_dist_P:
                min_dist_P = manhattanDistance(newPos, this_power)
            else:
                continue


        if 2 > min_dist_G:
            return -5000

        else:
            score_power = len(coordinates_power) * (-35)
            score_food = len(coordinates_food) * (-30)
            score_dist = 3 / min_dist_F + 5 / min_dist_P
            total_score = score_power + score_food + score_dist
            return total_score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        currScore = -10000
        returnAction = ''
        
        #return the val for the min part of minimax
        def mini(gameState, depth, agentIndex):
            val = 10000
            #check if we finished
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            actions = gameState.getLegalActions(agentIndex)
            #go through each possible action
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == (gameState.getNumAgents() - 1):
                    val = min(val, maximum(successor, depth))
                else:
                    val = min(val,mini(successor,depth,agentIndex+1))   
            return val

        #return the val for the max part of minimax
        def maximum(gameState, depth):
            val = -10000
            #update depth in the max part (one level deeper)
            currDepth = depth + 1
            #check if we are at the end
            #since we update depth in maximum
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(0)
            #go through each possible action
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                val = max(val, mini(successor, currDepth, 1))
            return val
        #go through each action, find the one with minimax highest score
        #return the action that produces highest score
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = mini(nextState, 0, 1)
            #update score
            if score > currScore:
                returnAction = action
                currScore = score
        return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #return the val for the min part of AB
        def mini(gameState, depth, agentIndex, a, b):
            val = 10000
            #check if we finished
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            newBeta = b

            actions = gameState.getLegalActions(agentIndex)
            #go though each possible action
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == (gameState.getNumAgents() - 1):
                    val = min (val, maximum(successor, depth, a, newBeta))
                    #prune
                    if val < a:
                        return val
                    newBeta = min(newBeta, val)
                else:
                    val = min(val, mini(successor, depth, agentIndex + 1, a, newBeta))
                    #prune
                    if val < a:
                        return val
                    #update beta
                    newBeta = min(newBeta, val)
            
            return val

        #return the val for the max part of AB
        def maximum(gameState, depth, a, b):
            val = -10000
            #update depth in the max part (one level deeper)
            currDepth = depth + 1
            #check if we are at the end
            #since we update depth in maximum
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                return self.evaluationFunction(gameState)
            newAlpha = a

            actions = gameState.getLegalActions(0)
            #go through each possible action
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                val = max (val, mini(successor, currDepth, 1, newAlpha, b))
                #prune if possible and update aplha
                if val > b:
                    return val
                newAlpha = max(newAlpha, val)
            return val
        
        #Pruning
        a = -10000
        b = 10000
        currScore = -10000
        returnAction = ''
        actions = gameState.getLegalActions(0)

        #same as minimax
        #go through each action, find the one with minimax highest score
        #return the action that produces highest score
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = mini(nextState, 0, 1, a, b)
            #update score
            if score > currScore:
                returnAction = action
                currScore = score
            #prune
            if score > b:
                return returnAction
            a = max(a, score)
        return returnAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # a little different implementation than ab or minimax that my partner did
        def expectimax(state, depth, agent):
            
            #if it is a terminal node, or there are no more actions
            if state.isWin() or state.isLose() or depth == self.depth or state.getLegalActions(agent) == 0:
                return (self.evaluationFunction(state), None)
            #For pacman
            if agent == 0:
                val = -10000
                for action in state.getLegalActions(agent):
                    #get all the succesors
                    #doing mod here in case there isnt a ghost, not sure if this is an edge case we shoult worry about
                    newVal = expectimax(state.generateSuccessor(agent, action), depth, (agent + 1) % state.getNumAgents())[0]
                    #see if the successor val is better than current
                    if newVal > val :
                        val = newVal
                        maxAction = action
                #Return the val and the action from which we found
                return (val, maxAction)  

            #For Ghost           
            else:
                #keep track of total and counter to find average
                totalVal = 0
                count = 0
                for action in state.getLegalActions(agent):
                    #same depth (this isnt the last ghost)
                    if agent + 1 < state.getNumAgents():
                        newVal = expectimax(state.generateSuccessor(agent, action), depth, agent + 1)[0]
                    #otherwise, it is a new depth (last ghost)
                    else:
                        newVal = expectimax(state.generateSuccessor(agent, action), depth + 1, 0)[0]

                    #simple average
                    totalVal += newVal
                    count += 1
                    minAction = action
                    #Return the average val and the action 
                return (totalVal/count, minAction)
        #run this function
        return expectimax(gameState, 0, 0)[1]



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
