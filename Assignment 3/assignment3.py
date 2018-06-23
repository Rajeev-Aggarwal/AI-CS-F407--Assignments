
# coding: utf-8

# In[748]:


import itertools
import csv
import numpy as np
from collections import defaultdict
import copy
import time


# In[2]:


def generate_packages(testcasefile):
    A_DC = []
    A_DE = []
    A_GE = []
    B_DC = []
    B_DE = []
    B_GE = []
    C_DC = []
    C_DE = []
    C_GE = []
    with open(testcasefile) as file:
        reader = csv.reader(file)
        i = 0
        for row in reader:
            if i==0:
                i+=1
                continue
            if row[1]=='DC':
                A_DC.append(row[0])
            elif row[1] == 'DE':
                A_DE.append(row[0])
            elif row[1] == 'GE':
                A_GE.append(row[0])
            if row[2]=='DC':
                B_DC.append(row[0])
            elif row[2] == 'DE':
                B_DE.append(row[0])
            elif row[2] == 'GE':
                B_GE.append(row[0])
            if row[3]=='DC':
                C_DC.append(row[0])
            elif row[3] == 'DE':
                C_DE.append(row[0])
            elif row[3] == 'GE':
                C_GE.append(row[0])
    
    A_DC = list(itertools.combinations(A_DC,3))
    A_DE = list(itertools.combinations(A_DE,2))
    A_GE = list(itertools.combinations(A_GE,1))
    B_DC = list(itertools.combinations(B_DC,3))
    B_DE = list(itertools.combinations(B_DE,2))
    B_GE = list(itertools.combinations(B_GE,1))
    C_DC = list(itertools.combinations(C_DC,3))
    C_DE = list(itertools.combinations(C_DE,2))
    C_GE = list(itertools.combinations(C_GE,1))
    A = []
    for i in range(len(A_DC)):
        for j in range(len(A_DE)):
            for k in range(len(A_GE)):
                A.append([A_DC[i],A_DE[j],A_GE[k]])
                
    B = []
    for i in range(len(B_DC)):
        for j in range(len(B_DE)):
            for k in range(len(B_GE)):
                B.append([B_DC[i],B_DE[j],B_GE[k]])
    C = []
    for i in range(len(C_DC)):
        for j in range(len(C_DE)):
            for k in range(len(C_GE)):
                C.append([C_DC[i],C_DE[j],C_GE[k]])
    programs = [A_DC,A_DE,A_GE,B_DC,B_DE,B_GE,C_DC,C_DE,C_GE]
            
    return A,B,C,programs


# In[214]:


A,B,C,programs = generate_packages('courses.csv')


# In[215]:


c  = [list(itertools.chain(*c)) for c in C]


# In[216]:



def read_profs(profs_file):
    profs = []
    with open(profs_file) as file:
        reader= csv.reader(file)
        for row in reader:
            a = []
            for i in range(1,len(row)):
                if row[i]=='NA':
                    break
                a.append(row[i])
            profs.append(a)
    return profs
            


def constraint_graph(packages,profs=None):
    A,B,C = packages
    graph = defaultdict(list)
    A = [list(itertools.chain(*c)) for c in A]
    B = [list(itertools.chain(*c)) for c in B]
    C = [list(itertools.chain(*c)) for c in C]
    packages = [A,B,C]
    for A in packages:
        for i in range(len(A)):
            for j in range(len(A[0])):
                for k in range(len(A[0])):
                    graph[A[i][j]].append(A[i][k])
                graph[A[i][j]] = list(set(graph[A[i][j]]))
    for prof in profs:
        for i in range(len(prof)):
            for j in range(len(prof)):
                if prof[j] not in graph[prof[i]]:
                    graph[prof[i]].append(prof[j])
    
    return graph


# In[219]:


profs = read_profs('profs.csv')

graph = constraint_graph([A,B,C],profs)



def read_courses(courses_file):
    courses = []
    with open(courses_file) as file:
        reader = csv.reader(file)
        j = 0
        for row in reader:
            if j ==0:
                j+=1
                continue
            L,T,P = list(map(int,row[4].split()))
            for i in range(P):
                courses.append(row[0]+'P'+str(i+1)+'_'+str(1))
                courses.append(row[0]+'P'+str(i+1)+'_'+str(2))   

    with open(courses_file) as file:
        reader = csv.reader(file)
        j = 0
        for row in reader:
            if j ==0:
                j+=1
                continue
            L,T,P = list(map(int,row[4].split()))  
            for i in range(L):
                courses.append(row[0]+'L'+str(i+1))
            for i in range(T):
                courses.append(row[0]+'T'+str(i+1))
             
    return courses
                

courses = read_courses('courses.csv')


def lab_constraint1(course,assignment):
    if 'P' not in course:
        return True
    slot,day,_ = assignment
    if slot >=5:
        return False
    return True


# In[505]:


def lab_constraint2(course,assignment,CSP):
    if 'P' not in course:
        return True
    slot,day,hall = assignment
    if course[-4:]=='P2_1':
        prev_slot,prev_day,prevhall = CSP[course[0:-4]+str('P1_1')]
        if prev_day!=day:
            return False
        if prev_slot != slot -1:
            return False
        return True
    if course[-4:] == 'P3_1':
        prev_slot,prev_day,prevhall = CSP[course[0:-4]+str('P2_1')]
        if prev_day!=day:
            return False
        if prev_slot != slot -1:
            return False
        return True
    if course[-4:]=='P2_2':
        prev_slot,prev_day,prevhall = CSP[course[0:-4]+str('P1_2')]
        if prev_day!=day:
            return False
        if prev_slot != slot -1:
            return False
        return True
    if course[-4:] == 'P3_2':
        prev_slot,prev_day,prevhall = CSP[course[0:-4]+str('P2_2')]
        if prev_day!=day:
            return False
        if prev_slot != slot -1:
            return False
        return True
    return True
        


# In[506]:


def tut_constraint3(course,assignment,CSP):
    if 'T' not in course:
        return True
    slot,day,_ = assignment
    l1 = course[0:-2]+str('L1')
    l2 = course[0:-2]+str('L2')
    l3 = course[0:-2]+str('L3')
    if CSP[l1]!=() and day==CSP[l1][1]:
        return False
    if CSP[l2]!=() and day==CSP[l2][1]:
        return False
    if CSP[l3]!=() and day == CSP[l3][1]:
        return False
    return True



def disc_constraint4(course,assignment,CSP,disc_courses):
    A_DC,B_DC,C_DC = disc_courses
    if 'P' in course:
        code = course[0:-4]
    else:
        code = course[0:-2]
    if code not in A_DC and code not in B_DC and code not in C_DC:
        return True
    slot,day,_ = assignment
    flag = True
    for program in [A_DC,B_DC,C_DC]:
        if code in program:
            for c in program:
                for l in ['L1','L2','L3']:
                    other_course = c+l
                    if course == other_course:
                        continue
                    if CSP[other_course]==():
                        continue
                    other_slot,other_day,_ = CSP[other_course]
                    if other_day==day:
                        if abs(other_slot-slot)==1:
                            flag = False
                            break
                if flag == False:
                    break
            if flag == False:
                break
    return flag


# In[510]:


def gen_constraint5(course,assignment,CSP,gen_courses):
    slot,day,_ = assignment
    if 'P' in course:
        code = course[0:-4]
    else:
        code = course[0:-2]    
    flag = True
    if code in gen_courses:
        for c in gen_courses:
            for l in ['L1','L2','L3']:
                other_course = c+l
                if course == other_course:
                    continue
                if CSP[other_course]==():
                    continue
                other_slot,other_day,_ = CSP[other_course]
                if other_day == day:
                    flag = False
                    break
            if flag==False:
                break

    return flag
                


# In[511]:


def lec_constraint6(course,assignment,CSP):
    if 'L' not in course:
        return True
    slot,day,_ = assignment
    flag = True
    for l in ['L1','L2','L3']:
        c = course[0:-2]+l
        if c == course[0:-2]:
            continue
        if CSP[c] == ():
            continue
        if CSP[c][1] == day:
            flag = False
            break
    return flag


# In[512]:


def prof_constraint8(course,assignment,profs):
    slot,day,_ = assignment
    if 'P' in course:
        code = course[0:-4]
    else:
        code = course[0:-2]
    if code in profs[3]:
        if day == 4:
            return False
    if code in profs[0]:
        if slot > 3:
            return False
    return True
        


# In[513]:


def prof_constraint9(course,assignment,profs,CSP):
    slot,day,_ = assignment
    if 'P' in course:
        return True
    else:
        code = course[0:-2]
    flag = True
    for prof in profs:
        if code in prof:
            for c in prof:
                for l in ['L1','L2','L3']:
                    other_course =c+l
                    if course == other_course:
                        continue
                    if CSP[other_course] == ():
                        continue
                    other_slot,other_day,_ = CSP[other_course]
                    if other_day == day:
                        if abs(other_slot - slot) == 1:
                            flag = False
                            break
                if flag == False:
                    break
            if flag == False:
                break
    return flag


# In[514]:


def clash_constraint10_11(course,assignment,CSP,graph):
    slot,day,_ = assignment
    if 'P' not in course:
        constraints = graph[course[0:-2]]
        
    else:
        constraints = graph[course[0:-4]]

    types = ['L1','L2','L3','T1','T2','T3','P1','P2','P3']
    flag = True
    for c in constraints:
        for l in types:
            if l[0] != 'P':
                other_course = c+l
                if other_course == course:
                    continue
                if CSP[other_course]==():
                    continue
                if CSP[other_course][0] == assignment[0] and CSP[other_course][1] == assignment[1]:
                    flag = False
                    break
            else:
                other_course1 = c+l+'_1'
                other_course2 = c+l+'_2'
                if course == other_course1 or course == other_course2:
                    continue
                if CSP[other_course1] == ():
                    continue
                if CSP[other_course2] == ():
                    continue
                if (CSP[other_course1][0] == assignment[0] and CSP[other_course1][1] == assignment[1]) and (CSP[other_course2][0] == assignment[0] and CSP[other_course2][1] == assignment[1]):
                    flag = False
                    break
        if flag == False:
            break
    return flag
                


# In[807]:



CSP = defaultdict(tuple)
halls = defaultdict(int)
labs = defaultdict(int)
DCs = [programs[0],programs[3],programs[6]]
GEs = [programs[2],programs[5],programs[8]]


# In[808]:


a = []

for program in GEs:
    for p in program:
        a.append(p[0])
        
GEs = list(set(a))
slots = list(range(1,8))
days = list(range(1,7))
DCs  = [list(itertools.chain(*c)) for c in DCs]


# In[809]:


def create_domains(courses,slots,days,graph=graph,profs=profs,halls=halls,DCs=DCs,GEs=GEs):
    domains = defaultdict(list)
    for course in courses:
        for slot in slots:
            for day in days:
                if day == 6 and slot > 4:
                    continue
                assignment = (slot,day,None)
                if lab_constraint1(course,assignment)==False:
                    continue
                if prof_constraint8(course,assignment,profs)==False:
                    continue
                domains[course].append([slot,day])
    return domains


# In[810]:


domains = create_domains(courses,slots,days)
domain_lengths =[]
for key,domain in domains.items():
    domain_lengths.append(len(domain))
def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)
domain_inds = argsort(domain_lengths)


# In[811]:


def DFS(courses,slots,days,CSP,domains=domains,graph=graph,profs=profs,halls=halls,DCs=DCs,GEs=GEs,depth=0):
    #print(courses[depth])
    if depth >= len(courses):
        return True
    course = courses[depth]
    flag = False
    domain = domains[course]
    for slot,day in domain:
        if day == 6:
            if slot >= 4:
                continue
        if course[-2] == 'L' or course[-2] == 'T':
            if halls[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'H'+str(halls[slot,day]+1))
        else:
            if labs[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'L'+str(labs[slot,day]+1))
        if lab_constraint1(course,assignment)==False:
            continue
        if lab_constraint2(course,assignment,CSP)==False:
            continue
        if tut_constraint3(course,assignment,CSP)==False:
            continue
        if disc_constraint4(course,assignment,CSP,DCs)==False:
            continue
        if gen_constraint5(course,assignment,CSP,GEs)==False:
            continue
        if lec_constraint6(course,assignment,CSP)==False:
            continue
        if prof_constraint8(course,assignment,profs)==False:
            continue
        if prof_constraint9(course,assignment,profs,CSP)==False:
            continue
        if clash_constraint10_11(course,assignment,CSP,graph)==False:
            continue
        CSP[course] = assignment
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] += 1
        else:
            labs[(slot,day)] += 1
        flag = DFS(courses,slots,days,CSP,depth = depth+1)
        if flag == True:
            break
        CSP[course] = ()
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] -= 1
        else:
            labs[(slot,day)] -= 1
    return flag


nodes = 0
maxdepth = 0
def DFS_MRV(courses,CSP,domains=domains,domain_inds=domain_inds, graph=graph,profs=profs,halls=halls,DCs=DCs,GEs=GEs,depth=0):
    global nodes
    global maxdepth
    nodes += 1
    if depth >= len(courses):
        maxdepth = depth
        return True
    course = courses[domain_inds[depth]]
    #print(course)
    flag = False
    domain = domains[course]
    for slot,day in domain:
        if day == 6:
            if slot >= 4:
                continue
        if course[-2] == 'L' or course[-2] == 'T':
            if halls[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'H'+str(halls[slot,day]+1))
        else:
            if labs[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'L'+str(labs[slot,day]+1))
        if lab_constraint1(course,assignment)==False:
            continue
        if lab_constraint2(course,assignment,CSP)==False:
            continue
        if tut_constraint3(course,assignment,CSP)==False:
            continue
        if disc_constraint4(course,assignment,CSP,DCs)==False:
            continue
       # if gen_constraint5(course,assignment,CSP,GEs)==False:
        #    continue
        if lec_constraint6(course,assignment,CSP)==False:
            continue
        if prof_constraint8(course,assignment,profs)==False:
            continue
        if prof_constraint9(course,assignment,profs,CSP)==False:
            continue
        if clash_constraint10_11(course,assignment,CSP,graph)==False:
            continue
        CSP[course] = assignment
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] += 1
        else:
            labs[(slot,day)] += 1
        flag = DFS_MRV(courses,CSP,depth = depth+1)
        if flag == True:
            break
        CSP[course] = ()
        if 'C_11' in course:
            print(course)
            print(CSP[course])
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] -= 1
        else:
            labs[(slot,day)] -= 1
    return flag    
    

days = {}
days[1] = 'Monday'
days[2] = 'Tuesday'
days[3] = 'Wednesday'
days[4] = 'Thursday'
days[5] = 'Friday'
days[6] = 'Saturday'
def write_csv(filename,CSP,days=days):
    with open(filename,"w") as file:
        writer = csv.writer(file)
        writer.writerow(['Course','Time','Day','Room'])
        for key,value in CSP.items():
            if value == ():
                continue
            time = str(value[0]) +":00"
            day = days[value[1]]
            writer.writerow([key,time,day,value[2]])

def read_csv(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def forward_checking(course,assignment,domains,graph,DCs=DCs,GEs=GEs,profs=profs):
    neighours = graph[course]
    new_domains = copy.deepcopy(domains)
    suffices = ['L1','L2','L3','T1','T2','T3','P1','P2','P3']
    flag = True
    slot,day,_ = assignment
    if 'P' in course:
        code = course[0:-4]
    else:
        code = course[0:-2]
    for neighour in neighours:
        for l in suffices:
            other_course = neighour + l
            if other_course == course:
                continue
            new_domains[other_course].remove([assignment[0],assignment[1]])
            if len(new_domains[other_course] == 0):
                flag = False
                break
        if flag == False:
            break
    if flag == False:
        print("hi")
        return flag,domains
    
    #Propogating Lecture Tut Constraint
    if 'L' in course:
        for t in ['T1','T2','T3']:
            other_course = code + t
            if other_course not in courses:
                break
            domain = new_domains[other_course]
            for new_slot,new_day in domain:
                if new_day == day:
                    new_domains[other_course].remove([new_slot,new_day])
            if len(new_domains[other_course])==0:
                flag = False
                break
    
    if flag == False:
        print("hi")
        return flag,domains
    #Propogating Tut Lecture Constraint
    if 'T' in course:
        for l in ['L1','L2','L3']:
            other_course = code + l
            if other_course not in courses:
                break
            domain = new_domains[other_course]
            for new_slot,new_day in domain:
                if new_day == day:
                    new_domains[other_course].remove([new_slot,new_day])
            if len(new_domains[other_course])==0:
                flag = False
                break
    
    if flag == False:
        print("hi")
        return flag,domains
            
    #Propogating one lec per day constraint
    if 'L' in course:
        for l in ['L1','L2','L3']:
            other_course = code + l
            if other_course not in courses:
                break
            if other_course == course:
                continue
            domain = new_domains[other_course]
            for new_slot,new_day in domain:
                if day == new_day:
                    new_domains[other_course].remove([new_slot,new_day])
            if len(new_domains[other_course])==0:
                flag = False
                break
    if flag == False:
        print("hi")
        return flag,domains

                    
    if flag==True:
        domains = new_domains
    return flag,new_domains
    


nodes = 0
maxdepth = 0
def DFS_forward_checking(courses,CSP,domains=domains,domain_inds=domain_inds, graph=graph,profs=profs,halls=halls,DCs=DCs,GEs=GEs,depth=0):
    global nodes
    global maxdepth
    nodes += 1
    if depth >= len(courses):
        maxdepth = depth
        return True
    course = courses[domain_inds[depth]]
    if 'C_12' in course:
        print(domains[course])
    #print(course)
    flag = False
    domain = domains[course]
    for slot,day in domain:
        if day == 6:
            if slot >= 4:
                continue
        if course[-2] == 'L' or course[-2] == 'T':
            if halls[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'H'+str(halls[slot,day]+1))
        else:
            if labs[(slot,day)] >= 5:
                continue
            assignment = (slot,day,'L'+str(labs[slot,day]+1))
        if lab_constraint1(course,assignment)==False:
            continue
        if lab_constraint2(course,assignment,CSP)==False:
            continue
        if tut_constraint3(course,assignment,CSP)==False:
            continue
        if disc_constraint4(course,assignment,CSP,DCs)==False:
            continue
        #if gen_constraint5(course,assignment,CSP,GEs)==False:
        #    continue
        if lec_constraint6(course,assignment,CSP)==False:
            continue
        if prof_constraint8(course,assignment,profs)==False:
            continue
        if prof_constraint9(course,assignment,profs,CSP)==False:
            continue
        if clash_constraint10_11(course,assignment,CSP,graph)==False:
            continue
        prev_domains = copy.deepcopy(domains)
        flag0,domains = forward_checking(course,assignment,domains,graph)
        if flag0 == False:
            continue
            
        CSP[course] = assignment
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] += 1
        else:
            labs[(slot,day)] += 1
        flag = DFS_forward_checking(courses,CSP,domains,depth = depth+1)
        if flag == True:
            break
        CSP[course] = ()
        domains = prev_domains
        if course[-2] == 'L' or course[-2] == 'T':
            halls[(slot,day)] -= 1
        else:
            labs[(slot,day)] -= 1
    return flag    

    
while True:
    print("Options:")
    print("Option 1: Display the packages.")
    print("Option 2: Display the constraint graph.")
    print("Option 3: Run using DFS_BT using MRV heuristic")
    print("Option 4: Run using DFS_BT_CP using MRV heuristic")

    option = int(input())
    if option == 1:
        print("Packages of Program A")
        for a in A:
            print(a)
        print("Packages of Program B")
        for a in B:
            print(a)
        print("Packages of Program C")
        for a in C:
            print(a)

    elif option == 2:
        for key,value in graph.items():
            print(key,str(":"),value)


    elif option == 3:
        CSP = defaultdict(tuple)
        halls = defaultdict(int)
        labs = defaultdict(int)
        start = time.time()
        DFS_MRV(courses,CSP)
        time_taken = time.time() - start
        write_csv("DFS_BT.csv",CSP)
        read_csv("DFS_BT.csv")
        print("Number of nodes created",nodes)
        print("Max recursion depth",maxdepth)
        print("Time Taken",time_taken)

    elif option == 4:
        CSP = defaultdict(tuple)
        halls = defaultdict(int)
        labs = defaultdict(int)
        start = time.time()
        DFS_forward_checking(courses,CSP)
        time_taken = time.time() - start
        write_csv("DFS_BT_CP.csv",CSP)
        read_csv("DFS_BT_CP.csv")
        print("Number of nodes created",nodes)
        print("Max recursion depth",maxdepth)
        print("Time Taken",time_taken)


