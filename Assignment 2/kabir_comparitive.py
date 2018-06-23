#Kabir Ahuja
#2015A1PS0791P

import time
from assignment2 import *




#MiniMax Algorithm Based Analysis
def mini_max_analysis():
	print("MiniMax Algorithm Based Analysis")
	i = 0
	game = align3()
	node = Node(game)
	node.state.display()
	draw_flag = True
	start = time.time()
	oponents_time = 0
	while node.state.done == False:
		action = None
		if i%2 == 0:
			action = minimax(node)
			col = action
			row = game.find_first_vacant(col)
			node.state.move(1,action)
			if node.state.done:
				print("You Lose")
				draw_flag = False
		else:
			a = time.time()
			action = int(input("Your Turn, Enter your move"))
			while action not in game.possible_actions():
				action = int(input("Invalid Move, Enter move again"))
			col = action
			row = game.find_first_vacant(col)   
			node.state.move(2,col)
			if node.state.done:
				print("You Win")
				draw_flag = False
			oponents_time += time.time() - a
		node.state.display()
		i += 1
	end = time.time()
	R1 = get_total_nodes()
	R2 = 73
	R3 =  get_maxdepth()
	R4 = end-start
	R5 = (R1/(R4-oponents_time))*(10**(-6))

	print("Total Number of nodes created:",R1)
	print("Memory Occupied by one node:",R2,"bytes")
	print("Maximum growth of Implicit stack:",R3)
	print("Total time Taken:",R4)
	print("Number of nodes created in 1 micro second",R5)

	return (R1,R2,R3,R4,R5)

#Alpha Beta Prunning Algorithm Based Analysis
def alpha_beta_analysis(R1):
	print("Alpha Beta Prunning Algorithm Based Analysis")
	i = 0
	game = align3()
	node = Node(game)
	node.state.display()
	draw_flag = True
	start = time.time()
	oponents_time = 0
	while node.state.done == False:
		action = None
		if i%2 == 0:
			action = minimax_fast(node,alpha,beta)
			col = action
			row = game.find_first_vacant(col)
			node.state.move(1,action)
			if node.state.done:
				print("You Lose")
				draw_flag = False
		else:
			a = time.time()
			action = int(input("Your Turn, Enter your move"))
			while action not in game.possible_actions():
				action = int(input("Invalid Move, Enter move again"))
			col = action
			row = game.find_first_vacant(col)   
			node.state.move(2,col)
			if node.state.done:
				print("You Win")
				draw_flag = False
			oponents_time += time.time() - a
		node.state.display()
		i += 1
	end = time.time()
	R6 = get_total_nodes()
	R7 = (R1 - R6)/R1
	R8 = end-start

	print("Total Number of Nodes created",R6)
	print("Fraction improvement by alpha beta",R7)
	print("Total time taken",R8)

	return R6,R7,R8


R1,R2,R3,R4,R5 = mini_max_analysis()
R6,R7,R8 = alpha_beta_analysis(R1)

mem_minimax = R1*R3/(1024*1024)
mem_alphabeta = R6*R3/(1024*1024)

R9 = (mem_minimax,mem_alphabeta)
print("Memory taken by minimax",mem_minimax,"MB")
print("Memory taken by minimax",mem_alphabeta,"MB")

avg_time = 0
for _ in range(10):
	i = 0
	game = align3()
	node = Node(game)
	node.state.display()
	draw_flag = True
	start = time.time()
	oponents_time = 0
	wins = 0 
	while node.state.done == False:
		action = None
		if i%2 == 0:
			action = minimax_fast(node,alpha,beta)
			col = action
			row = game.find_first_vacant(col)
			node.state.move(1,action)
			if node.state.done:
				print("You Lose")
				wins += 1
				draw_flag = False
		else:
			a = time.time()
			action = int(input("Your Turn, Enter your move"))
			while action not in game.possible_actions():
				action = int(input("Invalid Move, Enter move again"))
			col = action
			row = game.find_first_vacant(col)   
			node.state.move(2,col)
			if node.state.done:
				print("You Win")
				draw_flag = False
			oponents_time += time.time() - a
		node.state.display()
		i += 1
	end = time.time()
	avg_time += end-start

R10 = avg_time/10
R11 = wins
print("Average Time Taken to play 10 games",R10,"seconds")
