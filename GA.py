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
            writer.writerow([individual.euclid,",",'Euclidean'])
            writer.writerow([individual.success,",",'Sucess'])

def evaluate_pop(all_ind): # recall the whole pop
    #### ENTRY POINT OF GA 
    ### note all_ind is the entire population, all individuals ever created
    ## We sort them into generations with a gen number 
    worst_to_remove = ((all_ind.numberinds)/2)
    #Generate the Eucideans from two csv files
    for individuals in all_ind.current_ind_instances:
        if (individuals.success == True) and (individuals.alive == True): # plan returned without error and we ran the simulation
            calc_euclid(individuals)
            print "Individual number",individuals.indnum," has a euclidean of ",individuals.euclid
        if (individuals.success == False) and (individuals.alive == False):
            individuals.euclid = 0 # ensure set to zero 
            print "Individual number",individuals.indnum," FAILED and has a euclidean of Zero ",individuals.euclid

    # sorts best to worst Euclidean 
    all_ind.current_ind_instances.sort(key=lambda x: x.euclid,reverse=False)

    for i in range(0,worst_to_remove):# kill bottom half NOTE must be less than pop number of crash
        print "popping an ind"
        topop = all_ind.current_ind_instances[i]
        topop.alive = False # this way the historical population can still be sorted for alive True/False 
        all_ind.current_ind_instances.pop(0) # remove the individual from the current list 
    print "New pop of X Elites with X Weaker removed "    
    #print_all_current(all_ind)
    for individuals in all_ind.current_ind_instances:
        print "Surviving individual", individuals.indnum, "Euclid", individuals.euclid
    generate_new_gen(all_ind)

def generate_new_gen(remain_ind):
    # recall remain_ind is the entire population 
    numpoints = [2,9]
    xmin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]
    xmax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]
    ymin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]#[-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
    ymax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]#[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    zmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    zmax = [1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8]
    vmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    vmax = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]

    #remain_ind.current_ind_instances holds X number of Elites 
    remain_ind.gencount = remain_ind.gencount + 1
    print "The new Generation number is ", remain_ind.gencount
    worst_to_remove = ((remain_ind.numberinds)/2)
    newnum = 20 # this is how many new individuals to generate
    #numpoints = []
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
        if choice.euclid == 0:
            print "This was a bad choice because its euclid was zero, generate a new random ind"        
            remain_ind.generate_inds(1,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,remain_ind.gencount)
        else: individuals_to_reproduce.append(choice)
        choice_two = random.choice(remain_ind.current_ind_instances)
        #max_loop = 0
        while choice_two == choice: # ensures we dont have double ups
            print "woops we had to choose again because we doubled up"
            choice_two = random.choice(remain_ind.current_ind_instances)
            #max_loop = max_loop + 1
        if choice_two.euclid == 0:
            print "This was a bad choice_two because its euclid was zero, generate a new random ind"   
            remain_ind.generate_inds(1,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,remain_ind.gencount)
        else: individuals_to_reproduce.append(choice_two)
        if i < (worst_to_remove-2): # to make sure we dont end up with just one value in the list and therefore self replicating
            remain_ind.current_ind_instances.pop(0)

    # results in a list 20 parents long, that can have repeats of the best parents
    
    remain_ind.current_ind_instances.pop(0) # pop the last one in the list ready fro the next iteration 

    for individuals in individuals_to_reproduce:
        print "Luck Individual",individuals.indnum
        file_ind = "Results/Population/gen%s.csv" % (individual.gen)
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([individual.gen,",",'Generation'])
            writer.writerow([individual.num_points,",",'NumberPoints'])
            writer.writerow([individual.vmax,",",'Vmax'])
            writer.writerow([individual.xpos,",",'Xpos'])
            writer.writerow([individual.ypos,",",'Ypos'])
            writer.writerow([individual.zpos,",",'Zpos'])
            writer.writerow([individual.vmax,",",'Vmax'])
            #writer.writerow([individual.success,",",'Sucess'])

    raw_input()
    ### Above has generated 10 Pairs of Parents, they will may repeat but Superior fitness gives a better opportunity to repopulate. 
    for  i in range (0,10):
        # generate the new individuals 
        generate_new_children(remain_ind,individuals_to_reproduce[0], individuals_to_reproduce[1])
        individuals_to_reproduce.pop(0)
        individuals_to_reproduce.pop(0)
    
    #Mutate the Children randomly 
    mutate(remain_ind)
    # Generate the WP for children
    remain_ind.gen_wp()

def mutate(remain_ind):

    for individuals in remain_ind.current_ind_instances:
        will_mutate = random.randint(0, 10) # one in 10 chance to mutate
        individuals.printIndnum()
        #print "Mutating"

        if will_mutate >= 5:
            print "This individual", individuals.indnum, "will be mutated "
            number_genes_to_mutate = random.randint(1, 10) # how many genes might be mutated
            print "Number of Genes to mutate", number_genes_to_mutate
            max_wp_length = individuals.num_points # this is the max number of points
            #waypoints_to_mutate = []
            if number_genes_to_mutate > max_wp_length:
                number_genes_to_mutate = max_wp_length

            for i in range(0,number_genes_to_mutate):

                #print "In mutating wp"
                gene_to_mutate = random.randint(0,max_wp_length-1)
                sigma = 0.1
                #print "Gene",gene_to_mutate
                value = individuals.xpos[gene_to_mutate] 
                #print "Value",value
                ######################################################################################
                individuals.xpos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
                #print "New Value ",individuals.xpos[gene_to_mutate]
                #gene_to_mutate = random.randint(0,max_wp_length)
                value = individuals.ypos[gene_to_mutate] 
                #print "Value",value
                individuals.ypos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
                #print "New Value ",individuals.ypos[gene_to_mutate]
                #gene_to_mutate = random.randint(0,max_wp_length)
                value = individuals.zpos[gene_to_mutate] 
                #print "Value",value
                individuals.zpos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
                #print "New Value ",individuals.zpos[gene_to_mutate]

        print "Finished Mutating"
        individuals.printIndnum()
        #raw_input()





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

    # check to make sure parent_1 and parent_2 

    crossover_point = 0
    equal = False
    #short_parent = 0 
    if parent_1.num_points < parent_2.num_points:
        crossover_point = parent_1.num_points
        #print "Case 1"
        short_parent = parent_1
        long_parent = parent_2
    if parent_1.num_points > parent_2.num_points:
        crossover_point = parent_2.num_points
        #print "Case 2"
        short_parent = parent_2
        long_parent = parent_1
    if parent_1.num_points == parent_2.num_points:
        if parent_2.num_points > 2:
            crossover_point = parent_2.num_points/2
        else: crossover_point = 1

        short_parent = parent_1
        long_parent = parent_2
        equal = True 

    # print "Cross Over Point",crossover_point," short parent == ", short_parent
    # print "Short Parent X" , str(short_parent.xpos)[1:-1]
    # print "Short Parent Y" , str(short_parent.ypos)[1:-1]
    # print "Short Parent Z" , str(short_parent.zpos)[1:-1]

    # print "Long Parent X" , str(long_parent.xpos)[1:-1]
    # print "Long Parent Y" , str(long_parent.ypos)[1:-1]
    # print "Long Parent Z" , str(long_parent.zpos)[1:-1]
    # cross over point represnets the number of points avilable in the smallest parent 
    
    child_1x = []
    child_1y = []
    child_1z = []
    child_1v = []
    
    child_2x = []
    child_2y = []
    child_2z = []
    child_2v = []
    if equal == False: # we are going to use the uneven part as the cross over point
        print "Uneven Cross Over "
        # Grab First part of Geneome
        child_1num = long_parent.num_points
        child_2num = short_parent.num_points

        for val in short_parent.xpos:
            child_1x.append(val)
        for val in short_parent.ypos:
            child_1y.append(val)
        for val in short_parent.zpos:
            child_1z.append(val)
        for val in short_parent.vmax:
            child_1v.append(val)

        # Grab Second part of Geneome 
        for val in long_parent.xpos[crossover_point:None]: 
            child_1x.append(val)
        for val in long_parent.ypos[crossover_point:None]: 
            child_1y.append(val)
        for val in long_parent.zpos[crossover_point:None]: 
            child_1z.append(val)
        for val in long_parent.vmax[crossover_point:None]: 
            child_1v.append(val)        
        #Only take a portion of the long parents DNA for the new shorter 2nd child 
        for val in long_parent.xpos[0:crossover_point]:
            child_2x.append(val)
        for val in long_parent.ypos[0:crossover_point]:
            child_2y.append(val)
        for val in long_parent.zpos[0:crossover_point]:
            child_2z.append(val)
        for val in long_parent.vmax[0:crossover_point]:
            child_2v.append(val)
    if equal == True: 
        child_1num = long_parent.num_points
        child_2num = short_parent.num_points
        print "Even Cross over from Half"

        for val in long_parent.xpos[0:crossover_point]: 
            child_1x.append(val)
        for val in long_parent.ypos[0:crossover_point]: 
            child_1y.append(val)
        for val in long_parent.zpos[0:crossover_point]: 
            child_1z.append(val)
        for val in long_parent.vmax[0:crossover_point]: 
            child_1v.append(val)     

        for val in short_parent.xpos[0:crossover_point]: 
            child_2x.append(val)
        for val in short_parent.ypos[0:crossover_point]: 
            child_2y.append(val)
        for val in short_parent.zpos[0:crossover_point]: 
            child_2z.append(val)
        for val in short_parent.vmax[0:crossover_point]: 
            child_2v.append(val)     

        for val in long_parent.xpos[crossover_point:None]: 
            child_2x.append(val)
        for val in long_parent.ypos[crossover_point:None]: 
            child_2y.append(val)
        for val in long_parent.zpos[crossover_point:None]: 
            child_2z.append(val)
        for val in long_parent.vmax[crossover_point:None]: 
            child_2v.append(val)   

        for val in short_parent.xpos[crossover_point:None]: 
            child_1x.append(val)
        for val in short_parent.ypos[crossover_point:None]: 
            child_1y.append(val)
        for val in short_parent.zpos[crossover_point:None]: 
            child_1z.append(val)
        for val in short_parent.vmax[crossover_point:None]: 
            child_1v.append(val)    

    # print "Child 1 X", str(child_1x)[1:-1]
    # print "Child 1 Y", str(child_1y)[1:-1]
    # print "Child 1 Z", str(child_1z)[1:-1]

    # print "Child 2 X", str(child_2x)[1:-1]
    # print "Child 2 Y", str(child_2y)[1:-1]
    # print "Child 2 Z", str(child_2z)[1:-1]
    
    add = Individual(remain_ind.indcount,child_1num,child_1x,child_1y,child_1z,child_1v,remain_ind.gencount)
    remain_ind.current_ind_instances.append(add)
    remain_ind.indinstanceshistory.append(add)

    remain_ind.indcount = remain_ind.indcount + 1
    add = Individual(remain_ind.indcount,child_2num,child_2x,child_2y,child_2z,child_2v,remain_ind.gencount)
    remain_ind.current_ind_instances.append(add)
    remain_ind.indinstanceshistory.append(add)
    remain_ind.indcount = remain_ind.indcount + 1
