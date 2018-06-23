

import random
import copy
from collections import defaultdict
import sys
sys.setrecursionlimit(10000)



class tiled_floor():
    def __init__(self,n=20):
        self.n = n
        self.mat = [[0 for i in range(n)] for j in range(n)]
    
    def generate_dirt(self,p):
        total_dirt = int(((self.n)**2)*p)
        inds = random.sample(range((self.n)**2),k=total_dirt)
        for ind in inds:
            self.mat[ind//self.n][ind%self.n] = 1
            #board.adddirt("dirt"+str(ind), photo, ind//self.n,ind%self.n)
        #root.mainloop()
    
    def clean(self,i,j):
        self.mat[i][j] = 0
    
    def isclean(self):
        total_dirt = 0
        for i in self.mat:
            total_dirt += sum(i)
        return total_dirt == 0

    def get_totaldirt(self):
        total_dirt = 0
        for i in self.mat:
            total_dirt += sum(i)
        return total_dirt

class Intelligent_Agent():
    def __init__(self,env,initial_state):
        self.initial_state = initial_state
        self.cost = 0
        self.n = env.n
        self.path = []
        self.depth = 0
        self.positions = []
        self.reached_goal = False
        self.num_nodes = 0
        self.visited_states = defaultdict(bool)
        self.fails = 0
    

    def move_left(self,state):
        if state[1] == 0:
            return state
        else:
            self.cost += 2
            return (state[0],state[1]-1,state[2])
            
    def move_right(self,state):
        if state[1] == self.n - 1:
            return state
        else:
            self.cost += 2
            return (state[0],state[1]+1,state[2])
            
    def move_up(self,state):
        if state[0] == 0:
            return state
        else:
            self.cost += 2
            return (state[0]-1,state[1],state[2])
    def move_down(self,state):
        if state[0] == self.n - 1:
            return state
        else:
            self.cost += 2
            return (state[0]+1,state[1],state[2])

    def suck_dirt(self,state):
        if state[2].mat[state[0]][state[1]] == 0:
            return state
        else:
            #print("Cleaning......")
            x = copy.deepcopy(state[2])
            x.clean(state[0],state[1])
            self.cost += 1
            return (state[0],state[1],x)
            
        if state[1] == self.n - 1:
            a = ['L','U','D']
            #random.shuffle(a)
            return a
        a = ['L','R','U','D']
        #random.shuffle(a)
        return a
    
    def stuck(self,limit = 10000000):
        return self.fails >= limit
        
                    
    def possible_actions(self,state):
        if state[2].mat[state[0]][state[1]] == 1:
            return ['S']
        
        if state[0]==0 and state[1] == 0:
            a = ['R','D']
            #random.shuffle(a)
            return a
        
        if state[0]==self.n - 1 and state[1] == self.n-1:
            a = ['L','U']
            #random.shuffle(a)
            return a
        
        if state[0] == 0 and state[1] == self.n - 1:
            a = ['L','D']
            #random.shuffle(a)
            return a
        
        if state[0] == self.n - 1 and state[1] == 0:
            a = ['R','U']
            #random.shuffle(a)
            return a
        
        if state[0] == 0:
            a = ['L','R','D']
            #random.shuffle(a)
            return a
        
        if state[1] == 0:
            a = ['R','U','D']
            #random.shuffle(a)
            return a
        
        if state[0] == self.n-1:
            a = ['L','R','U']
            #random.shuffle(a)
            return a
        
        if state[1] == self.n - 1:
            a = ['L','U','D']
            #random.shuffle(a)
            return a
        a = ['L','R','U','D']
        #random.shuffle(a)
        return a
    

        
    def take_action(self,state,action):
        if action == 'S':
            return self.suck_dirt(state)
        if action == 'L':
            return self.move_left(state)
        if action == 'R':
            return self.move_right(state)
        if action == 'U':
            return self.move_up(state)
        if action =='D':
            return self.move_down(state)
        return state
                
    def is_terminal(self,i,j):
        if i==0 and j==0:
            return True
        if i==0 and j==self.n - 1:
            return True
        if i==self.n-1 and j == 0:
            return True
        if i == self.n-1 and j == self.n - 1:
            return True
        
        
    def search(self,state,depth,maxdepth):
        self.num_nodes += 1
        self.visited_states[state] = True
        self.depth = max(depth,self.depth)
        if state[2].isclean() and self.is_terminal(state[0],state[1]):
            self.reached_goal = True
            self.positions.append((state[0],state[1]))
            return
        
        if depth >= maxdepth:
            self.fails += 1
            if self.stuck() and self.is_terminal(state[0],state[1]):
                self.reached_goal = True
                self.positions.append((state[0],state[1]))
            return
        
        actions = self.possible_actions(state)
        for action in actions:
            new_state = self.take_action(state,action)
            if self.visited_states[new_state] == True:
                continue
            #state = new_state
            self.search(new_state,depth+1,maxdepth)
            if self.reached_goal == True:
                self.path.append(action)
                self.positions.append((state[0],state[1]))
                break
        return
    
    def follow_path(self):
        path = self.path[::-1]
        self.cost = 0
        state = self.initial_state
        for action in path:
            new_state = self.take_action(state,action)
            state = new_state
            
# In[263]:            
        
class Intelligent_Agent2(Intelligent_Agent):
    def __init__(self,env,initial_state):
        Intelligent_Agent.__init__(self,env,initial_state)

    def heuristic(self,state):
        i,j,_ = state
        if state[2].mat[i][j] == 1:
            return ['S']
        if state[0]==0 and state[1] == 0:
            a =[]
            if state[2].mat[i][j+1] == 1:
                a.append('R')
            if state[2].mat[i+1][j] == 1:
                a.append('D')
            if a == []:
                a = ['R','D']
            #random.shuffle(a)
            return a
        
        if state[0]==self.n - 1 and state[1] == self.n-1:
            a = []
            if state[2].mat[i][j-1] == 1:
                a.append('L')
            if state[2].mat[i-1][j] == 1:
                a.append('U')
            if a == []:
                a = ['L','U']
            #random.shuffle(a)
            return a
        
        if state[0] == 0 and state[1] == self.n - 1:
            a = []
            if state[2].mat[i][j-1] == 1:
                a.append('L')
            if state[2].mat[i+1][j] == 1:
                a.append('D')
            if a == []:
                a = ['L','D']
            #random.shuffle(a)
            return a
        
        if state[0] == self.n - 1 and state[1] == 0:
            a = []
            if state[2].mat[i][j+1] == 1:
                a.append('R')
            if state[2].mat[i-1][j] == 1:
                a.append('U')
            if a == []:
                a = ['R','U']
            #random.shuffle(a)
            return a
        
        if state[0] == 0:
            a = []
            if state[2].mat[i][j-1] == 1:
                a.append('L')
            if state[2].mat[i][j+1] == 1:
                a.append('R')
            if state[2].mat[i+1][j] == 1:
                a.append('D')
            if a == []:
                a = ['L','R','D']
            #random.shuffle(a)
            return a
        
        if state[1] == 0:
            a = []
            if state[2].mat[i][j+1] == 1:
                a.append('R')
            if state[2].mat[i-1][j] == 1:
                a.append('U')
            if state[2].mat[i+1][j] == 1:
                a.append('D')
            if a == []:
                a = ['R','U','D']
            #random.shuffle(a)
            return a
        
        if state[0] == self.n-1:
            a = []
            if state[2].mat[i][j-1] == 1:
                a.append('L')
            if state[2].mat[i][j+1] == 1:
                a.append('R')
            if state[2].mat[i-1][j] == 1:
                a.append('U')
            if a == []:
                a = ['L','R','U']
            #random.shuffle(a)
            return a
        
        if state[1] == self.n - 1:
            a = []
            if state[2].mat[i][j-1] == 1:
                a.append('L')
            if state[2].mat[i-1][j] == 1:
                a.append('U')
            if state[2].mat[i+1][j] == 1:
                a.append('D')
            if a == []:
                a = ['L','U','D']
            #random.shuffle(a)
            return a
        a = []
        if state[2].mat[i][j+1] == 1:
            a.append('R')
        if state[2].mat[i][j-1] == 1:
            a.append('L')
        if state[2].mat[i-1][j] == 1:
            a.append('U')
        if state[2].mat[i+1][j] == 1:
            a.append('D')
        if a == []:
            a = ['L','R','U','D']
        #random.shuffle(a)
        return a
    
    def heuristic2(self,state):
        i,j = state[0:2]
        if state[2].mat[i][j] == 1:
            return ['S']
        if i == 0 and j == 0:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j+1] == 1:
                a['R'] += 1
            if state[2].mat[i+1][j] == 1:
                a['D'] += 1
            if state[2].mat[i+1][j+1] == 1:
                a['R'] += 1/2
                a['D'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        if i==0 and j == self.n-1:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j-1] == 1:
                a['L'] += 1 
            if state[2].mat[i+1][j] == 1:
                a['D'] += 1
            if state[2].mat[i+1][j-1] == 1:
                a['L'] += 1/2
                a['D'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        if i == self.n-1 and j==0:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j+1] == 1:
                a['R'] += 1
            if state[2].mat[i-1][j] == 1:
                a['U'] += 1
            if state[2].mat[i-1][j+1] == 1:
                a['R'] += 1/2
                a['U'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        if i == self.n-1 and j == self.n -1:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i-1][j] == 1:
                a['U'] += 1
            if state[2].mat[i][j-1] == 1:
                a['L'] += 1
            if state[2].mat[i-1][j-1] == 1:
                a['L'] += 1/2
                a['U'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        if i == 0:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i+1][j] == 1:
                a['D'] += 1
            if state[2].mat[i][j+1] == 1:
                a['R'] += 1
            if state[2].mat[i][j-1] == 1:
                a['L'] += 1
            if state[2].mat[i+1][j-1] == 1:
                a['L'] += 1/2
                a['D'] += 1/2
            if state[2].mat[i+1][j+1] == 1:
                a['R'] += 1/2
                a['D'] += 1 /2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        if j == 0:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j+1] == 1:
                a['R'] += 1
            if state[2].mat[i-1][j] == 1:
                a['U'] += 1
            if state[2].mat[i+1][j] == 1:
                a['D'] += 1
            if state[2].mat[i+1][j+1] == 1:
                a['R'] += 1/2
                a['D'] += 1/2
            if state[2].mat[i-1][j+1] == 1:
                a['R'] += 1/2
                a['U'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        
        if state[0] == self.n-1:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j-1] == 1:
                a['L'] += 1
            if state[2].mat[i][j+1] == 1:
                a['R'] += 1
            if state[2].mat[i-1][j] == 1:
                a['U'] += 1
            if state[2].mat[i-1][j+1] == 1:
                a['R'] += 1/2
                a['U'] += 1/2
            if state[2].mat[i-1][j-1] == 1:
                a['L'] += 1/2
                a['U'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        
        if state[1] == self.n - 1:
            a = {'L':0,'R':0,'U':0,'D':0}
            if state[2].mat[i][j-1] == 1:
                a['L'] += 1
            if state[2].mat[i-1][j] == 1:
                a['U'] += 1
            if state[2].mat[i+1][j] == 1:
                a['D'] += 1
            if state[2].mat[i+1][j-1] == 1:
                a['D'] += 1/2
                a['L'] += 1/2
            if state[2].mat[i-1][j-1] == 1:
                a['U']+=1/2
                a['L'] += 1/2
            a = list(a.items())
            #random.shuffle(a)
            a.sort(key = lambda x: x[1],reverse=True)
            return a
        a = {'L':0,'R':0,'U':0,'D':0}
        if state[2].mat[i][j+1] == 1:
            a['R'] += 1
        if state[2].mat[i][j-1] == 1:
            a['L'] += 1
        if state[2].mat[i-1][j] == 1:
            a['U'] += 1
        if state[2].mat[i+1][j] == 1:
            a['D'] += 1
        if state[2].mat[i+1][j-1] == 1:
            a['D'] += 1/2
            a['L'] += 1/2
        if state[2].mat[i-1][j-1] == 1:
            a['U'] += 1/2
            a['L'] += 1/2
        if state[2].mat[i+1][j+1] == 1:
            a['R'] += 1/2
            a['D'] += 1/2
        if state[2].mat[i-1][j+1] == 1:
            a['R'] += 1/2
            a['U'] += 1/2
        a = list(a.items())
        #random.shuffle(a)
        a.sort(key = lambda x: x[1],reverse=True)
        return a

    def search(self,state,depth,maxdepth,h):
        self.num_nodes += 1
        self.visited_states[state] = True
        self.depth = max(depth,self.depth)
        if state[2].isclean() and self.is_terminal(state[0],state[1]):
            self.reached_goal = True
            self.positions.append((state[0],state[1]))
            return
        if depth > maxdepth:
            return
        if h=='h1':    
            actions = self.heuristic(state)
        else:
            actions = self.heuristic2(state)
        actions = [a[0] for a in actions]
        for action in actions:
            new_state = self.take_action(state,action)
            if self.visited_states[new_state] == True:
                continue
            #state = new_state
            self.search(new_state,depth+1,maxdepth,h)
            if self.reached_goal == True:
                self.path.append(action)
                self.positions.append((state[0],state[1]))
                break
        return
            

