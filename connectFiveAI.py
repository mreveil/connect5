"""connectFiveAI.py

simple AI engine to play the connect5 game using a minimax algorithm.

Author: Mardochee Reveil
1/8/2017


"""

import connectFive as cf
from copy import deepcopy
import constants

def getSuccessors(state,player):

    successors,bestSuccessors = [],[]
    for i in range(1,len(state)-1):
	for j in range(1,len(state[i])-1):
	    if state[i][j] == 0:
		if state[i][j-1] != 0 or state[i][j+1] != 0 or state[i+1][j] !=0 or state[i-1][j] != 0 or state[i-1][j-1] != 0 or state[i-1][j+1] != 0 or state[i+1][j-1] != 0 or state[i+1][j+1] != 0:
	
		    newState = deepcopy(state)
		    newState[i][j] = player
		    	 
		    if newState not in successors:
			successors.append(newState)#,i,j])
			utility = cf.getStateUtility(newState)
			if utility == constants.GAME_OVER or utility == -1*constants.GAME_OVER:
			    bestSuccessors.append(newState)
			    break
			
    if len(bestSuccessors) > 0:
	#print 'Returning 1 successor!'
	return bestSuccessors

    return successors



def isNodeTerminal(state):
    utility = cf.getStateUtility(state)
    if utility == constants.GAME_OVER or utility == constants.GAME_OVER*-1:
	return True
    else:
	return False



def alphabeta(node,depth,alpha,beta,maximizingPlayer,player):
        #print 'Recursion'
    if player == 1:
	otherPlayer = 2
    else:
	otherPlayer = 1

    if depth == 0 or isNodeTerminal(node):
	utility = cf.getStateUtility(node)
	#print 'Inside alphabeta\n','depth =',depth,'\nutility =',utility,'\nnode is:',node
	return utility,node

    if maximizingPlayer:
	v = float("-inf")
	nextState = 0
	for child in getSuccessors(node,player):
	    a,state = alphabeta(child,depth-1,alpha,beta,False,otherPlayer)	    
	    if a > v:
		nextState = child
		#print 'Found one potential play',child,nextState
	    v = max(v,a)
	    alpha = max(alpha,v)
	    if beta <= alpha:
		break
	return v,nextState

    else:
	v = float("inf")
	nextState = 0
	for child in getSuccessors(node,player):
	    b,state = alphabeta(child,depth-1,alpha,beta,True,otherPlayer)
	    if b < v:
		nextState = child
	    v = min(v,b)
	    beta = min(beta,v)
	    if beta <= alpha:
		break
	return v,nextState


def play(currentState):

    v,nextState = alphabeta(currentState,3,float("-inf"),float("inf"),True,2)

    for i in range(len(currentState)):
	for j in range(len(currentState[i])):
	    if currentState[i][j] != nextState[i][j]:
		best_i = i
		best_j = j
		break

    print 'Best move found!'  #,best_i,best_j,'Value of this move is:',v
    return best_i,best_j



