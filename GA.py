import time
#import Individual
from copy import deepcopy
from itertools import izip
import csv
from scipy.spatial import distance
import random
from Individual import Individual

def print_all_current(all_ind): # passed population

    for individuals in all_ind.current_ind_instances:
        print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid

def print_all_current(all_ind): # passed population
    print "Entire History of Individuals in the order of their creation"

    for individuals in all_ind.indinstanceshistory:
        print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid , "Generation ", Individuals.gen


def calc_euclid(individual):
    file_str = "Results/Sim/ind%sgen%s.csv" % ((individual.indnum), (individual.gen))
    print "file String looks like",file_str
    #currently zeros, will be real data 
    other_file_str = "Results/Real/allZero.csv" 
    print "Opening file to evaluate",file_str


    with open(file_str,'rb') as textfile1, open(other_file_str,'rb') as textfile2: 
        csvreader1=csv.reader(textfile1,delimiter=',') # Careful to check csv type file 
        csvreader2=csv.reader(textfile2,delimiter=',')
        print "list Method"
        # Simulation data 
        xyz = list(izip(*csvreader1))
        valsX = xyz[0] # Zero all X 
        valsY = xyz[1] # Zero all X 
        valsZ = xyz[2] # Zero all X 
        #Will be real data currently zeros
        zero = list(izip(*csvreader2))
        compX = zero[0] # careful to change later 
        compY = zero[0]
        compZ = zero[0]

        for i in range(len(valsX)):
            #print(colors[i])
            #print "NUmbers look like"
            #print valsX[i]
            #print valsY[i]
            #print valsZ[i]
            x = float(valsX[i])
            y = float(valsY[i])
            z = float(valsZ[i])
            p1 = (x,y,z)#(float(valsZ[i])))
            p2 = (0.0,0.0,0.0)
            #print p2
            individual.euclid = individual.euclid + distance.euclidean(p1,p2)
        print "Euclidean Composite from 0,0,0 to every point at 10hz recording frequency", individual.euclid
        
        file_ind = "Results/Individuals/ind%sgen%s.csv" % ((individual.indnum),(individual.gen))
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([individual.euclid])
            writer.writerow([individual.success])

def evaluate_pop(all_ind): # recall the whole pop
    #### ENTRY POINT OF GA 
    ### note all_ind is the entire population, all individuals ever created
    ## We sort them into generations with a gen number 
    worst_to_remove = ((all_ind.numberinds)/2)
    #Generate the Eucideans from two csv files
    for individuals in all_ind.current_ind_instances:
        if (individuals.success == True) and (individuals.alive == True): # plan returned without error and we ran the simulation
            calc_euclid(individuals)
    # sorts best to worst Euclidean 
    all_ind.current_ind_instances.sort(key=lambda x: x.euclid,reverse=False)

    for i in range(0,worst_to_remove):# kill bottom half NOTE must be less than pop number of crash
        print "popping an ind"
        topop = all_ind.current_ind_instances[i]
        topop.alive = False # this way the historical population can still be sorted for alive True/False 
        all_ind.current_ind_instances.pop(0) # remove the individual from the current list 
    print "New pop of X Elites with X Weaker removed "    
    #print_all_current(all_ind)
    generate_new_gen(all_ind)

def generate_new_gen(remain_ind):
    # recall remain_ind is the entire population 
    #remain_ind.current_ind_instances holds X number of Elites 
    remain_ind.gencount = remain_ind.gencount + 1
    print "The new Generation number is ", remain_ind.gencount
    worst_to_remove = ((remain_ind.numberinds)/2)
    newnum = 20 # this is how many new individuals to generate
    numpoints = []
    sortnumpoints = [] # list if two min max
    for individuals in remain_ind.current_ind_instances:
        print "Chosen Alive Individuals",individuals.indnum
    # Randomly Select who will populate out new parents who will pass on genetics
    # To make the Fitest of the Elites most likely to reproduce we will pop each iteration so best have most chance of generating a child
    individuals_to_reproduce = []
    for i in range (0,worst_to_remove):
        print i, "evaluating"
        #Twice so we end up with a list of 20 (10 pairs to create 20 children) from out best 10 
        choice = random.choice(remain_ind.current_ind_instances)
        individuals_to_reproduce.append(choice)
        choice_two = random.choice(remain_ind.current_ind_instances)
        #max_loop = 0
        while choice_two == choice:
            print "woops we had to choose again"
            choice_two = random.choice(remain_ind.current_ind_instances)
            #max_loop = max_loop + 1
        individuals_to_reproduce.append(choice_two)
        if i < (worst_to_remove-2): # to make sure we dont end up with just one value in the list and therefore self replicating
            remain_ind.current_ind_instances.pop(0)

    # results in a list 20 parents long, that can have repeats of the best parents
    
    remain_ind.current_ind_instances.pop(0) # pop the last one in the list ready fro the next iteration 

    for individuals in individuals_to_reproduce:
        print "Luck Individual",individuals.indnum
    ### Above has generated 10 Pairs of Parents, they will may repeat but Superior fitness gives a better opportunity to repopulate. 
    for  i in range (0,10):
        # generate the new individuals 
        generate_new_children(remain_ind,individuals_to_reproduce[0], individuals_to_reproduce[1])
        individuals_to_reproduce.pop[0]
        individuals_to_reproduce.pop[0]
    
    #Mutate the Children randomly 

    # Generate the WP for children
    remain_ind.gen_wp()


def generate_new_children(remain_ind,parent_1, parent_2):
    #Passed the entire population and specificially the two parents that will generate two children. 
    #Individuals
        # self.indnum = indnum
        # self.xpos = deepcopy(xpos)
        # self.ypos = deepcopy(ypos)
        # self.zpos = deepcopy(zpos)
        # self.vmax = deepcopy(vmax)
        # self.num_points = number_points
        #send the new min max for each coordinate point to the new population generator. 
    #Population 
        # indcount = 1
        # gencount = 1
        # current_ind_instances = []
        # indinstanceshistory = []
    # grab the lowest number of point 

    crossover_point = 0
    #short_parent = 0 
    if parent_1.num_points < parent_2.num_points:
        crossover_point = parent_1.num_points
        print "Case 1"
        short_parent = parent_1
        long_parent = parent_2
    if parent_1.num_points > parent_2.num_points:
        crossover_point = parent_2.num_points
        print "Case 2"
        short_parent = parent_2
        long_parent = parent_1

    print "Cross Over Point",crossover_point," short parent == ", short_parent
    print "Long Parent X" , str(long_parent.xpos)[1:-1]
    print "Long Parent Y" , str(long_parent.ypos)[1:-1]
    print "Long Parent Z" , str(long_parent.zpos)[1:-1]
    # cross over point represnets the number of points avilable in the smallest parent 
    child_1num = long_parent.num_points
    child_1x = []
    child_1y = []
    child_1z = []
    child_1v = []
    child_1num = short_parent.num_points
    child_2x = []
    child_2y = []
    child_2z = []
    child_2v = []
    # Grab First part of Geneome
    for val in short_parent.xpos:
        child_1x.append(val)
    for val in short_parent.ypos:
        child_1y.append(val)
    for val in short_parent.zpos:
        child_1z.append(val)
    for val in short_parent.vmax:
        child_1v.append(val)

    # Grab Second part of Geneome 
    for val in long_parent.xpos[crossover_point:-1]: 
        child_1x.append(val)
    for val in long_parent.ypos[crossover_point:-1]: 
        child_1y.append(val)
    for val in long_parent.zpos[crossover_point:-1]: 
        child_1z.append(val)
    for val in long_parent.vmax[crossover_point:-1]: 
        child_1v.append(val)        
    #Only take a portion of the long parents DNA for the new shorter 2nd child 
    for val in long_parent.xpos[1:crossover_point]:
        child_2x.append(val)
    for val in long_parent.ypos[1:crossover_point]:
        child_2y.append(val)
    for val in long_parent.zpos[1:crossover_point]:
        child_2z.append(val)
    for val in long_parent.vmax[1:crossover_point]:
        child_2v.append(val)

    print "Child 2 X", str(child_2x)[1:-1]
    print "Child 2 Y", str(child_2y)[1:-1]
    print "Child 2 Z", str(child_2z)[1:-1]

    raw_input()
    remain_ind.indcount = remain_ind.indcount + 1

    ## First Child 
    #Note we dont use generate_inds(self,num,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,gen): as this is a random initializer only 

    add = Individual(remain_ind.indcount,number_points,x_pos,y_pos,z_pos,v_max,gen)
    remain_ind.current_ind_instances.append(add)
    remain_ind.indinstanceshistory.append(add)




    remain_ind.indcount = remain_ind.indcount + 1




    print "generating new child of ", newnum
    remain_ind.gencount = remain_ind.gencount +1
    #remain_ind.generate_inds(newnum,numpoints,new_xmin,new_xmax,new_ymin,new_ymax,new_zmin,new_zmax,new_vmin,new_vmax,remain_ind.gencount)
    for individuals in remain_ind.current_ind_instances:
        if individuals.evaluated == False:
            remain_ind.gen_wp()

    # for individuals in remain_ind.current_ind_instances:
    #     #get all of the possible min max num points and put them in a list 
    #     #individuals.printIndnum()
    #     #print "h"
    #     val = deepcopy(individuals.returnnumpoints())
    #     #print val
    #     #print "e"
    #     sortnumpoints.append(val)
    #     #print "re"
    # sortnumpoints.sort()
    # numpoints.append(sortnumpoints[0])    # new minimum
    # numpoints.append(sortnumpoints[-1])   # new maximum
    # print "new min max number points", numpoints
            

    # new_xmin = [] # list if 10ish min max
    # new_xmax= [] # list if 10ish min max
    # new_ymin= [] # list if 10ish min max
    # new_ymax= [] # list if 10ish min max
    # new_zmin= [] # list if 10ish min max
    # new_zmax= [] # list if 10ish min max
    # new_vmin= [] # list if 10ish min max
    # new_vmax= [] # list if 10ish min max

    # for i in range(0,9):# CHANGE FOR POSSIBLE POINTS CHAANGE
    #     #create a list to sort for min max
    #     xold = []
    #     yold =[]
    #     zold = []
    #     vold = []
    #     #for each lasting individual
    #     for individuals in remain_ind.current_ind_instances:
    #         try:
    #             #Get the historical target x y z for each point

    #             xold.append((individuals.returnx())[i])
    #             yold.append((individuals.returny())[i])
    #             zold.append((individuals.returnz())[i])
    #             vold.append((individuals.returnv())[i])
    #         except:
    #             print "may be no points to copy ie shorter array"
    #     #for each point Take each and sort to find new min max
    #     xold.sort()
    #     yold.sort()
    #     zold.sort()
    #     vold.sort()   
    #     # for each point add a new min and max
    #     try:
    #         new_xmin.append(xold[0]) # list if 10ish min max
    #         new_xmax.append(xold[-1]) # list if 10ish min max
    #         new_ymin.append(yold[0]) # list if 10ish min max
    #         new_ymax.append(yold[-1]) # list if 10ish min max
    #         new_zmin.append(zold[0]) # list if 10ish min max
    #         new_zmax.append(zold[-1]) # list if 10ish min max
    #         new_vmin.append(vold[0]) # list if 10ish min max
    #         new_vmax.append(vold[-1]) # list if 10ish min max
    #     except:
    #         print "Out of points"
        
    #     print "New Version Ind"
    #     print "Number Points",numpoints[0],numpoints[1]
    #     print new_xmin#.append(xold[0]) # list if 10ish min max
    #     print new_xmax#.append(xold[-1]) # list if 10ish min max
    #     print new_ymin#.append(yold[0]) # list if 10ish min max
    #     print new_ymax#.append(yold[-1]) # list if 10ish min max
    #     print new_zmin#.append(zold[0]) # list if 10ish min max
    #     print new_zmax#.append(zold[-1]) # list if 10ish min max
    #     print new_vmin#.append(vold[0]) # list if 10ish min max
    #     print new_vmax#.append(vold[-1]) # list if 10ish min max        


    #######pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax)
    # reverse false fiv