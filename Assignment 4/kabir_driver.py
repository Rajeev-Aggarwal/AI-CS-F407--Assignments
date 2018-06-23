#Author: Kabir Ahuja
#ID: 2015A1PS0791P

from __future__ import absolute_import
import Tkinter as tk
from kabir_bnet import *

window = tk.Tk()

window.title(u'My App')
window.geometry(u'900x900')
buttons_query = []
buttons_negquery = []
buttons_cond = []
buttons_negcond = []
query_variables = []
cond_variables = []
done = False

bayes_net,nodes,bn_vars = create_bayes_net(u'input1.txt')
#print(bayes_net)
#print(nodes)
#print(bn_vars)
L = [key for key,_ in nodes.items()]



def inference(query_variables,cond_variables):

	query_vals = []
	for query in query_variables:
		if u'~' in query:
			query_vals.append(False)
		else:
			query_vals.append(True)
	print u"hi"
	print query_vals
	q,e = create_expressions(query_variables,cond_variables,nodes)
	mblank = []
	for i in q:
		mblank += compute_markov_blanket(bayes_net,i,nodes)
	for i,_ in e.items():
		mblank += compute_markov_blanket(bayes_net,i,nodes)
	mblank = list(set(mblank))
	mblank.sort(key = lambda x: bn_vars.index(x))

	Q = Enumeration_Ask(q,e,bn_vars,nodes)

	return Q[tuple(query_vals)]


def pressed_querybutton(ind):
	if done:
		return
	name = L[ind]
	buttons_query[ind].config(bg = u'yellow')
	print name
	query_variables.append(name)
	
def pressed_negquerybutton(ind):
	if done:
		return
	name = u'~'+L[ind]
	buttons_negquery[ind].config(bg = u'yellow')
	print name
	query_variables.append(name)
	
def pressed_condbutton(ind):
	if done:
		return
	name = L[ind]
	buttons_cond[ind].config(bg = u'yellow')
	print name
	cond_variables.append(name)
	
def pressed_negcondbutton(ind):
	if done:
		return
	name = u'~'+L[ind]

	buttons_negcond[ind].config(bg = u'yellow')
	print name
	cond_variables.append(name)

def pressed_markov_button(entry):
	mblankA = compute_markov_blanket(bayes_net,unicode(entry),nodes)
	print "Markov Blanket of A", mblankA
	result = tk.Text(master = window,height = 2, width = 50)
	result.place(x = 550, y = 150)
	result.insert(tk.END, unicode(mblankA))


	
def pressed_donebutton():
	done = True
	done_button.config(bg = u'pink')
	prob_str = u'P('
	for i,q in enumerate(query_variables):
		prob_str += q
		if i < len(query_variables) - 1:
			prob_str += u','
	prob_str += u'|'
	for i,c in enumerate(cond_variables):
		prob_str += c
		if i < len(cond_variables) - 1:
			prob_str += u','	
	prob_str += u')'
	
	display_prob = tk.Text(master = window,height = 3,width = 50)
	display_prob.place(x= 600, y = 500)
	display_prob.insert(tk.END,u'Generated Query:' + prob_str)
	
	label = tk.Button(text = u"Calculating Probability",bg = u'yellow')
	label.place(x = 700, y = 600)

	Q = inference(query_variables,cond_variables)

	label.config(text = u"Done Calculating Probability", bg = u"grey")

	result = tk.Text(master = window,height = 2, width = 50)
	result.place(x = 600, y = 650)
	result.insert(tk.END,u'Answer: '+ unicode(Q))
	

#Button
b1 = tk.Button(text = u'Query Variables',bg = u'skyblue')
b1.config(height = 2,width = 40)
b1.place(x=0,y=0)
#button1.grid(column = 0,row = 0)

button2 = tk.Button(text = u'Condition Variables',bg = u'skyblue')
button2.config(height = 2,width = 40)
button2.place(x=300,y=0)
j = 5
for i,l in enumerate(L):
	buttons_query.append(tk.Button(text = l, bg = u'lightgreen',command = lambda a=i :pressed_querybutton(a)))
	buttons_query[i].place(x = 10,y = 50*(i+1))
	buttons_query[i].config(height = 2,width = 10)
	
	buttons_negquery.append(tk.Button(text = u'~'+l, bg = u'lightgreen',command = lambda a=i :pressed_negquerybutton(a)))
	buttons_negquery[i].place(x = 100,y = 50*(i+1))
	buttons_negquery[i].config(height = 2,width = 10)


	buttons_cond.append(tk.Button(text = l, bg = u'lightgreen',command = lambda a=i :pressed_condbutton(a)))
	buttons_cond[i].config(height = 2,width = 10)
	buttons_cond[i].place(x = 350,y = 50*(i+1))
	buttons_negcond.append(tk.Button(text = u'~'+l, bg = u'lightgreen',command = lambda a=i :pressed_negcondbutton(a)))
	buttons_negcond[i].config(height = 2,width = 10)
	buttons_negcond[i].place(x = 440,y = 50*(i+1))
	
	j += 2
	
done_button = tk.Button(text = u'Done', command = lambda : pressed_donebutton())
done_button.place(x = 700, y =400)
done_button.config(height = 4, width = 10)

markov_entry = tk.Entry(master = window)
markov_entry.place(x = 700, y = 100)

markov_button = tk.Button(text = u'Generate Markov Blanket', command = lambda : pressed_markov_button(markov_entry.get()))
markov_button.place(x = 700, y = 120)


#Runs everything inside the window
window.mainloop()