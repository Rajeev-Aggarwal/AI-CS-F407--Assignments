
#Kabir Ahuja
#2015A1PS0791P

import random
import copy
import sys


# In[27]:
alpha = -sys.maxsize
beta = sys.maxsize
max_depth = 0
num_nodes = 0
class align3():
	def __init__ (self,mat):
		self.n = 4
		self.mat = mat
		self.vacant = 4*4
		self.done = False

	
	def reset(self):
		self.mat = [[0 for i in range(self.n)] for j in range(self.n)]
		self.vacant = 4*4
		self.done = False
		
	def find_first_vacant(self,col):
		first = None
		for i in range(self.n):
			if self.mat[i][col] == 0:
				first = i
				break
		return first
	
	def display(self):
		for a in self.mat:
			print(a)
		print("")
		
	def Terminal_test(self,player,row,col):
		if self.vacant == 0:
			self.done = True
			#print("DRAW")
			return
		if col < 2:
			if self.mat[row][col+1] == player and self.mat[row][col+2]==player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
				
		if col >=2:
			if self.mat[row][col-1]==player and self.mat[row][col-2]==player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if col ==2 or col==1:
			if self.mat[row][col-1]==player and self.mat[row][col+1]==player:
				self.done = True
				return
		if row >=2:
			if self.mat[row-1][col]==player and self.mat[row-2][col]==player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if col < 2 and row < 2:
			if self.mat[row+1][col+1] == player and self.mat[row+2][col+2] == player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if col < 2 and row >= 2:
			if self.mat[row-1][col+1] == player and self.mat[row-2][col+2] == player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if col >= 2 and row < 2:
			if self.mat[row+1][col-1] == player and self.mat[row+2][col-2] == player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if col >= 2 and row >= 2:
			if self.mat[row-1][col-1] == player and self.mat[row-2][col-2] == player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
		if (col==1 or col==2) and (row==1 or row==2):
			if self.mat[row-1][col-1] == player and self.mat[row+1][col+1] == player:
				self.done = True
				#print("Player "+ str(player) +" Wins")
				return
			if self.mat[row-1][col+1]==player and self.mat[row+1][col-1]==player:
				self.done = True
				return           
			
				
	def move(self,player,col):
		first = self.find_first_vacant(col)
		self.mat[first][col] = player
		self.vacant -= 1
		#self.display()
		self.Terminal_test(player,first,col)
		
	def possible_actions(self):
		actions = []
		for i in range(self.n):
			flag = False
			for j in range(self.n):
				if self.mat[j][i] == 0:
					flag = True
					break
			if flag:
				actions.append(i)
		return actions
	
	def random_gameplay(self):
		player = 0
		while self.done == False:
			player = player%2 + 1
			actions = self.possible_actions()
			action = random.choice(actions)
			self.move(player,action)
		self.reset()
			
		
class Node():
	def __init__(self,state):
		self.state = state

def successor_function(node,action,player):
	new_node = copy.deepcopy(node)
	new_node.state.move(player,action)
	return new_node


# In[56]:
won = False
def minimax(node):
	global won
	won = False
	actions = node.state.possible_actions()
	v = []
	for action in actions:
		n = successor_function(node,action,1)
		x = MinVal(n,1)
		v.append((x,action))
		if x == 1:
			break
	return max(v)[1]

def MinVal(node,depth):
	global won 
	global num_nodes
	global max_depth
	max_depth = max(depth,max_depth)
	num_nodes += 1
	if node.state.done == True:
		if node.state.vacant == 0:
			return 0
		else:
			won = True
			return 1
	actions = node.state.possible_actions()
	v = []
	for action in actions:
		n = successor_function(node,action,2)
		v.append(MaxVal(n,depth+1))
	return min(v)

def MaxVal(node,depth):
	global won
	global num_nodes
	global max_depth
	max_depth = max(depth,max_depth)
	num_nodes += 1
	if node.state.done == True:
		if node.state.vacant == 0:
			return 0
		else:
			return -1
	
	actions = node.state.possible_actions()
	v = []
	for action in actions:
		if won:
			break
		n = successor_function(node,action,1)                
		v.append(MinVal(n,depth+1))
	won = False
	return max(v)


def minimax_fast(node,alpha,beta,depth=0,ultrafast = False):
	global won
	won = False
	actions = node.state.possible_actions()
	v = []
	for action in actions:
		n = successor_function(node,action,1)
		val = MinVal_fast(n,alpha,beta,depth+1)
		v.append((val,action))
		if val == 1 and ultrafast:
			break
	return max(v)[1]

def MinVal_fast(node,aplha,beta,depth):
	global won
	global num_nodes
	global max_depth
	max_depth = max(depth,max_depth)
	num_nodes += 1
	if node.state.done == True:
		if node.state.vacant == 0:
			return 0
		else:
			won = True
			return 1
	actions = node.state.possible_actions()
	v = sys.maxsize
	for action in actions:
		n = successor_function(node,action,2)
		v = min(v,MaxVal_fast(n,alpha,beta,depth+1))
		if v <= alpha:
			break
		beta = min(beta,v)
	return v

def MaxVal_fast(node,alpha,beta,depth):
	global num_nodes
	global max_depth
	max_depth = max(depth,max_depth)
	num_nodes += 1
	if node.state.done == True:
		if node.state.vacant == 0:
			return 0
		
		else:
			return -1
	actions = node.state.possible_actions()
	v = -sys.maxsize
	for action in actions:
		n = successor_function(node,action,1)
		v = max(v,MinVal_fast(n,alpha,beta,depth+1))
		if v >= beta:
			break
		alpha = max(alpha,v)
	return v

def get_total_nodes():
	global num_nodes
	a = num_nodes
	num_nodes = 0
	return a

def get_maxdepth():
	global max_depth
	a = max_depth
	max_depth = 0
	return a

#This function prints values based on the previous experience. For realtime analysis see comparitive.py
def print_analysis():
	print("MiniMax Based Analysis:")
	print("R1: Total Number of nodes created:",611385)
	print("R2: Memory Occupied by one node:",73,"bytes")
	print("R3: Maximum growth of Implicit stack:",16)
	print("R4: Total time Taken:",48.84042716026306,'seconds')
	print("R5: Number of nodes created in 1 micro second",0.015696351)
	print("")
	print("Alpha Beta Based Analysis: ")
	print("R6: Total Number of Nodes created",122500)
	print("R7: Fraction improvement by alpha beta",0.7996352543814454)
	print("R8: Total time taken",17.06990122795105,'seconds')
	print("")
	print("Comparitive Analysis:")
	print("R9 a: Memory taken by minimax", 9.328994750976562,"MB")
	print("R9 b: Memory taken by alphabeta",1.86920166015625,"MB")
	print("R10: Average Time Taken to play 10 games",22.17881123456777,"seconds")
	print("R11: Wins in 10 games:",10)
	print("R12: Wins in 20 games:",20)
	print("")
	print("Note: This analysis is based on some previous gameplay, for real time analysis see comparitive.py")



