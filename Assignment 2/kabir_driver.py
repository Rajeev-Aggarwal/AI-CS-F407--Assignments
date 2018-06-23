#Kabir Ahuja
#2015A1PS0791P

import turtle
import time
import sys
from kabir_assignment2 import *
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Floor")
wn.setup(400,400)



class Printer(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.color("red")


class Pen(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("square")
		self.color("white")
		self.penup()
		self.speed(0)

class Line(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape('arrow')
		self.color('blue')
		self.penup()
		self.pensize(8)

class Pointer(turtle.Turtle):
	def __init__(self,color):
		turtle.Turtle.__init__(self)
		self.shape("triangle")
		self.pensize(8)
		self.color(color)
		self.penup()
		self.speed(0)

def draw_board(m=4,n=4,xcor=100,ycor=100):
	for y in range(m):
		for x in range(n):
			screen_x = -xcor + (x*50)
			screen_y = ycor- (y*50)
			pen.turtlesize(2,2)
			pen.goto(screen_x,screen_y)
			pen.stamp()
	line = Line()
	line.goto(-150,150)
	line.pendown()
	line.forward(300)
	line.stamp()

def trace_path(x,y,trace,color,xcor=100,ycor=100):
	screen_x = -xcor + (x*50)
	screen_y = ycor- (y*50)
	trace.goto(screen_x,screen_y)
	trace.stamp()

def get_row_col(x,y,xcor=100,y_cor = 100):
	col = (x+xcor)//50
	row = (y_cor-y)//50
	return col,row

def play(mode='ab'):
	
	mat = [[0 for i in range(4)] for j in range(4)]
	game = align3(mat)
	node = Node(game)
	node.state.display()
	draw_flag = True
	start = time.time()
	i = 0
	while node.state.done == False:
		action = None
		if i%2 == 0:
			if mode=='ab':
				action = minimax_fast(node,alpha,beta)
			elif mode == 'ab++':
				action = minimax_fast(node,alpha,beta,ultrafast=True)
			else:
				action = minimax(node)
			col = action
			row = game.find_first_vacant(col)
			trace_path(col,row,trace1,color='blue')
			node.state.move(1,action)
			if node.state.done:
				print("You Lose")			
				printer.write("You Lose", font=("Arial", 25, "bold"))
				draw_flag = False
		else:
			action = int(input("Your Turn, Enter your move"))
			while action-1 not in game.possible_actions():
				action = int(input("Invalid Move, Enter move again"))
			col = action-1
			row = game.find_first_vacant(col)   
			trace_path(col,row,trace2,color='red')
			node.state.move(2,col)
			if node.state.done:
				print("You Win")
				printer.write("You Win", font=("Arial", 16, "normal"))
				draw_flag = False
		node.state.display()
		i += 1

	if draw_flag:
		print("DRAW")
		printer.write("DRAW", font=("Arial", 16, "normal"))
	end = time.time()
	num_nodes = get_total_nodes()
	print("Total Nodes Generated",num_nodes)
	print("Total Time taken",end-start)
	print("Max Recursion depth",get_maxdepth())
	print("Memory occupied",73*num_nodes/(1024*1024),"MB")
flag = False
printer = Printer()
while True:
	mode = 'ab'
	option = input("Select options\n 1: To display Board \n 2: To play the game with minimax \n 3: To play the game with alphabeta \n 4: To play game with alphabeta++(my modification) \n 5: For the rules and controls of the game \n 6: To print the analysis\n")
	if option == '1':
		pen = Pen()
		draw_board()
		continue
	if option == '5':
		print("Rules:")
		print("You have to put coins in the square grids. You can only put the coins in the row nearest to the baseline. Three coins in a row,column or diagonal will win the game.")
		print("")
		print("Controls:")
		print("1: To put the coin in first column")
		print("2: To put the coin in second column")
		print("3: To put the coin in third column")
		print("4: To put the coin in fourth column")
		continue
	if option == '6':
		print_analysis()
		continue
	if option == '2':
		mode = 'mm'
	if option == '3':
		mode = 'ab'
	if option == '4':
		mode = 'ab++'
	while True:
		pen = Pen()
		trace1 = Pointer('blue')
		trace1.shape("circle")
		trace2 = Pointer('green')
		draw_board()
		play(mode)
		choice = input('TryAgain: t  Main menu: m To exit: Ctrl+D')
		if choice == 'm':
			flag = True
			printer.clear()
			break
		printer.clear()
while True:
	pass