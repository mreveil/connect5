"""connectFive.py

General library to calculate the value of a give state of the game and also determine if a player has won.

Author: Mardochee Reveil
1/8/2017

"""


import constants

def getStateUtility(state):

    #Player 2 is the maximizer (and player 1 the minimizer)

    totalPoints = 0

    for player in [1,2]:

	if player == 1:
	    multiplier = -1
	else:
	    multiplier = 1

        for i in range(len(state)): 
	    rowPoints = getPoints(state[i],player) # Checking rows
	    columnPoints = getPoints([s[i] for s in state ],player)  # For columns
	    #TODO: Implement both diagonals

	    #print rowPoints,columnPoints
		
	    if rowPoints == constants.GAME_OVER or columnPoints == constants.GAME_OVER: #This is a final state
		#print 'GAME OVER!!!!!'
		return constants.GAME_OVER*multiplier
	    else:
		if player == 2:
		    totalPoints += multiplier*(rowPoints + columnPoints) 
		else:
		    totalPoints += multiplier*2*(rowPoints + columnPoints) 
                    #The factor of 2 encodes the fact that the AI has to prioritize preventing the other player to connect 5
	    
    
    return totalPoints

def getPoints(positions,player):


    # 5 connected pawns are worth constants.GAME_OVER (arbitrarily large value)
    # 4 connected unbound pawns are worth 10 points
    # 3 connected unbound pawns are workth 5 points 

    n = 0
    if player == 1:
	otherPlayer = 2
    else:
	otherPlayer = 1

    points = 0
    indexOfFirst = 0

    for i in range(len(positions)):

        if positions[i] == player:
	    if n == 0:
		indexOfFirst = i
	    n += 1
		
	elif n > 0:
	    if n >= 5: # Game over
		return constants.GAME_OVER
	    if n > 2:
		if positions[indexOfFirst-1] != otherPlayer:
		    if n == 3:
			points += 5
		    else:
			points += 10

		if positions[i] != otherPlayer:
		    if n == 3:
			points += 5
		    else:
			points += 10
	    n = 0

		  
    return points



