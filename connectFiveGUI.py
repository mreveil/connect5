"""connectFiveGUI.py

Basic GUI to play a connect5 game. Supports two human players or one human and an AI player.

Author: Mardochee Reveil
1/8/2017


"""

import Tkinter as tk
from PIL import Image, ImageTk
from copy import deepcopy
import connectFive as cf
import connectFiveAI as ai
import constants

# NB: Player 1 is minimizer, player 2 is maximizer

class ConnectFive:

    def __init__(self,master):
	self.master = master
	master.title("Connect5")
	
	self.c = tk.Canvas(root, height=1000, width=1000, bg='white')
	self.c.pack(fill=tk.BOTH, expand=True)

	self.w = 1000
	self.h = 1000

	self.gridSize = 50

	self.c.bind('<Configure>', self.create_grid)
        self.c.bind("<Button-1>", self.callback)

	
	image = Image.open('star.png')
	image = image.resize((50,50),Image.ANTIALIAS)
	self.star = ImageTk.PhotoImage(image)

	image = Image.open('circle.png')
	image = image.resize((40,40),Image.ANTIALIAS)
	self.circle = ImageTk.PhotoImage(image)

	
	self.currentPlayer = tk.IntVar()
	self.currentPlayer.set(1) # Player 1 always start 

	#TODO: Allow player 1 and 2 to alternate starting the game
	#TODO: Keep track of score
	#TODO: Allow players to have names

	self.currentState = [[0 for x in range(0,self.w,self.gridSize)] for y in range(0,self.w,self.gridSize)] 

	self.isAIPlaying = True # Change to False to allow for two humans to play
	self.isGameOver = False


    def create_grid(self,event=None): 

	#self.w = self.c.winfo_width() # Get current width of canvas
    	#self.h = self.c.winfo_height() # Get current height of canvas

    	self.c.delete('grid_line') # Will only remove the grid_line
    	# Creates all vertical lines at intevals of width/50
    	for i in range(0, self.w, self.gridSize):
    	    self.c.create_line([(i, 0), (i, self.h)], tag='grid_line')
    	# Creates all horizontal lines at intevals of length/50
    	for i in range(0, self.h,self.gridSize):
    	    self.c.create_line([(0, i), (self.w, i)], tag='grid_line')

    

    def converToGridCoord(self,f):
	""" Takes in x and y coordinates and convert them to i and j """

    	a = int(f)/int(self.gridSize)
    	if f<a*self.gridSize+self.gridSize/3 and f> a*self.gridSize-self.gridSize/3:
	    return a
    	elif f<(a+1)*self.gridSize+self.gridSize/3 and f> (a+1)*self.gridSize-self.gridSize/3:
	    return a+1
    	else:
	    return -1
	
    
    
    def callback(self,event):

	""" Places the correct 'pawn' when a player clicks or the computer chooses a location"""	

    	i = self.converToGridCoord(event.x)
    	j = self.converToGridCoord(event.y)
    
    	if i > 0 and j > 0 and not self.isGameOver:
	    if not self.isAIPlaying: #Assuming two humans are playing
	        if self.currentPlayer.get() == 1:
	    	    self.c.create_image(i*self.gridSize,j*self.gridSize, image=self.star)
		    self.currentState[j][i] = 1
		    self.currentPlayer.set(2)

	        else:	  	
	  	    self.c.create_image(i*self.gridSize,j*self.gridSize, image=self.circle)
	   	    self.currentState[j][i] = 2
		    self.currentPlayer.set(1)
	    
	        utility = cf.getStateUtility(self.currentState)
	        if utility == -1*constants.GAME_OVER:
		    print 'player 1 (star) has won!!! Congratulations!'
		    self.isGameOver = True
	        elif utility == constants.GAME_OVER:
		    print 'Player 2 (filled circle) has won!!! Congratulations!'
		    self.isGameOver = True

	    else:
		self.c.create_image(i*self.gridSize,j*self.gridSize, image=self.star)
		self.master.update()
		self.currentState[j][i] = 1
		utility = cf.getStateUtility(self.currentState)
		#print utility
	        if utility == -1*constants.GAME_OVER:
		    print 'Human Player (star) has won!!! Congratulations!'
		    self.isGameOver = True
		else:
		    print 'Calculating best move...'
		    i,j = ai.play(self.currentState)
		    self.c.create_image(j*self.gridSize,i*self.gridSize, image=self.circle)
		    self.currentState[i][j] = 2
		    utility = cf.getStateUtility(self.currentState)
		    #print utility
	            if utility == constants.GAME_OVER:
		        print 'Computer (filled circle) has won!!! Congratulations!'
		        self.isGameOver = True

    	elif not self.isGameOver:
	    print 'Invalid location. Click close to a grid intersection.'
	
	print 'Player ',self.currentPlayer.get(),', it is your turn!'




root = tk.Tk()
gui = ConnectFive(root)
root.mainloop()

