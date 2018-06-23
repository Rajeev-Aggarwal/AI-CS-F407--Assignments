
#Author: Kabir Ahuja
#ID: 2015A1PS0791P

from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import copy
from collections import defaultdict
from io import open
from itertools import imap


def gen_permut(expr):
    if len(expr) == 0:
        return []
    if len(expr) == 1:
        return [[False],[True]]
        
    rest = gen_permut(expr[1:])
    poss1 = [[False]+i for i in rest]
    poss2 = [[True]+i for i in rest]
    return poss1+poss2

class Node(object):
    
    def __init__(self,name,parents,probs,gen_permut):
        self.name = name
        self.parents = parents
        self.prior = None
        self.conds = {}
        self.negconds = {}
        self.gen_permut = gen_permut
        if len(parents) == 0:
            self.prior = probs[0]
        else:
            self.fill_probs(probs)
        

    
    def fill_probs(self,probs):
        vals = [False]*len(self.parents)
        self.conds[tuple(vals)] = probs[0]
        self.negconds[tuple(vals)] = 1 - probs[0]
        j = 1
        for i in xrange(1,len(self.parents)+1):
            vals_copy = copy.copy(vals)
            vals_copy[-i] = True
            perms = self.gen_permut([False]*(len(vals_copy) - len(vals_copy[:-i]) - 1))
            if perms == []:
                self.conds[tuple(vals_copy)] = probs[j]
                self.negconds[tuple(vals_copy)] = 1 - probs[j]
                j += 1
            else:
                for perm in perms:
                    val = vals_copy[:-i+1] + perm
                    self.conds[tuple(val)] = round(probs[j],4)
                    self.negconds[tuple(val)] = 1 - round(probs[j],4)
                    j += 1
                    
    def get_prob(self,val,cond):
        if cond == []:
            if val:
                return self.prior
            else:
                return 1 - self.prior
        if val:
            return self.conds[tuple(cond)]
        
        return 1 - self.conds[tuple(cond)]
                    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name
            
            

def create_bayes_net(file):
    bayes_net = defaultdict(list)
    nodes = {}
    bn_vars = []
    with open(file) as fp:
        lines = fp.readlines()
        for line in lines:
            if line == u'$$':
                continue
            line = line.replace(u'\n',u'')
            l = line.split(u'>>')
            name = l[0][0]
            parents = l[1].replace(u'[',u'').replace(u']', u'').replace(u',',u' ').split()
            probs = list(imap(float,l[2].split()))
            node = Node(name,parents,probs,gen_permut)
            nodes[name] = node
            bn_vars.append(node)
    
    for name,node in nodes.items():
        parents = node.parents
        for parent in parents:
            bayes_net[nodes[parent]].append(node)
            
    return bayes_net,nodes,bn_vars



def compute_markov_blanket(bayes_net,node,nodes):
    if isinstance(node,unicode):
        node = nodes[node]
    markov_blanket = bayes_net[node]
    markov_blanket.append(node)
    parents = node.parents
    for parent in parents:
        parent_node = nodes[parent]
        markov_blanket.append(parent_node)
        parent_children = bayes_net[parent_node]
        markov_blanket += parent_children
        
    markov_blanket = list(set(markov_blanket))
        
    return markov_blanket



def Normalize(Q):
    norm = 0
    for key,value in Q.items():
        norm += value
    for key,value in Q.items():
        Q[key] = Q[key]/norm
        
    return Q

def Enumeration_Ask(X,e,mblank,nodes):
    Q = {}
    xs = gen_permut([False]*len(X))
    for i,x in enumerate(X):
        if x in e:
            if e[x] == False:
                for xss in xs:
                    if xss[i] == True:
                        Q[tuple(xss)] = 0
                        
            else:
                for xss in xs:
                    if xss[i] == False:
                        Q[tuple(xss)] = 0
    for x in xs:
        #extend e with the value of xi for X
        if tuple(x) in Q:
        	continue
        for i in xrange(len(x)):
            #print(X[i])
            e[X[i]] = x[i]
            
        Q[tuple(x)] = Enumerate_All(mblank,e,nodes)
        
    return Normalize(Q)

def extend(e,Y,y):
    e_copy = copy.copy(e)
    e_copy[Y] = y
    return e_copy

def Enumerate_All(mblank,e,nodes):
    
    if len(mblank) == 0:
        return 1
    mblank_copy = copy.copy(mblank)
    while True:
        Y = mblank_copy.pop(0)
        parents_y = Y.parents
        parent_nodes = [nodes[i] for i in parents_y]
        flag = False
        for parent in parent_nodes:
            if parent not in e:
                flag = True
                mblank_copy.append(Y)
                break
        if flag == False:
            break
            
    y = None
    if Y in e:
        y = e[Y]
    probs = [e[node] for node in parent_nodes]
    if y!=None:
        return Y.get_prob( y,probs)*Enumerate_All(mblank_copy,e,nodes)
        
    else:
        return sum([Y.get_prob(i,probs)*Enumerate_All(mblank_copy,extend(e,Y,i),nodes) for i in [True,False]])


# In[690]:


def create_expressions(q,conds,nodes):
    e = {}
    X = []
    for x in q:
    	if u'~' in x:
    		X.append(nodes[x[1]])
    	else:
    		X.append(nodes[x])

    for cond in conds:
        if u'~' in cond:
            e[nodes[cond[1]]] = False
        else:
            e[nodes[cond]] = True
            
    return X,e
    





