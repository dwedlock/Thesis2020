import time
#import Individual
from copy import deepcopy
from itertools import izip
import csv
from scipy.spatial import distance
import random
from Individual import Individual

def print_all_current(population): # passed population

    for individuals in population.current_ind_instances:
        print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid

def print_all_current(population): # passed population
    print "Entire History of Individuals in the order of their creation"
    for individuals in population.indinstanceshistory:
        print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid , "Generation ", Individuals.gen

def calc_euclid(individual):
    file_str = "Results/Sim/ind%sgen%s.csv" % ((individual.indnum), (individual.gen))

    print "file String looks like",file_str
    #currently zeros, will be real data 
    other_file_str = "Results/Real/ind%sgen%s.csv" % ((individual.indnum), (individual.gen))
    print "Opening file to evaluate",file_str


    with open(file_str,'rb') as textfile1, open(other_file_str,'rb') as textfile2: 
        csvreader1=csv.reader(textfile1,delimiter=',') # Careful to check csv type file 
        csvreader2=csv.reader(textfile2,delimiter=',')
        print "list Method"
        # Simulation data 
        xyz = list(izip(*csvreader1))
        valsX = xyz[0] # sim x
        valsY = xyz[1] # sim Y 
        valsZ = xyz[2] # sim z 
        #Will be real data currently zeros
        realxyz = list(izip(*csvreader2))
        compX = realxyz[0] # real x
        compY = realxyz[1] # real y
        compZ = realxyz[2] # real z 
        lenR = len(valsX)
        lenS = len(compX)
        shorter = 0
        if lenR > lenS:
            shorter = lenS
        else:
            shorter = lenR
        for i in range(0,shorter):
            xS = float(valsX[i])
            yS = float(valsY[i])
            zS = float(valsZ[i])
            xR = float(compX[i])
            yR = float(compY[i])
            zR = float(compZ[i])

            p1 = (xS,yS,zS)#(float(valsZ[i])))
            p2 = (xR,yR,zR)
            #print p2
            individual.euclid = individual.euclid + distance.euclidean(p1,p2)
        print "Euclidean Composite from 0,0,0 to every point at 10hz recording frequency", individual.euclid
        
        file_ind = "Results/Individuals/ind%sgen%s.csv" % ((individual.indnum),(individual.gen))
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([individual.euclid,",",'Euclidean'])
            writer.writerow([individual.sim_success,",",'Sim Sucess'])
            writer.writerow([individual.real_success,",",'Real Sucess'])


def evaluate_pop(population): # recall the whole pop
    #### ENTRY POINT OF GA ###############
    ### note population is the entire population, all individuals ever created
    ## We sort them into generations with a gen number 
    cal_acc_euclid(population)
    #cal_vel_score(population)
    
    worst_to_remove = ((population.numberinds)/2)
    #Generate the Eucideans from two csv files
    for individuals in population.current_ind_instances:
        if (individuals.sim_success == True) and (individuals.alive == True): # plan returned without error and we ran the simulation
            if (individuals.calc_euclid == False):
                # This is to ensure we never call twice or add more to a euclidean that is already calculated
                calc_euclid(individuals)

                print "Individual number",individuals.indnum," has a euclidean of ",individuals.euclid
                individuals.calc_euclid == True
        if (individuals.sim_success == False) and (individuals.alive == False):
            individuals.euclid = 0 # ensure set to zero 
            print "Individual number",individuals.indnum," FAILED and has a euclidean of Zero ",individuals.euclid
    
    file_ind = "Results/Population/totalgens.csv"
    cal_ifElite(population)

    for individuals in population.current_ind_instances:
        if individuals.saved_to_gens == False:
            with open(file_ind, 'a') as csvfile:
                individuals.saved_to_gens = True
                writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
                #number_points,x_pos,y_pos,z_pos,v_max,gen
                writer.writerow([individuals.gen,",",'Generation',",",individuals.indnum,",","Euclid",",",individuals.euclid,",",individuals.num_points,",",individuals.gen,",",individuals.alive,",",individuals.sim_run,",",individuals.real_run,",",individuals.acc_euclid,",",individuals.sim_success,",",individuals.execute_success,",",individuals.parent_of_gen,",",individuals.saved_to_gens,",",individuals.mutated,",",individuals.calc_euclid,",",individuals.isElite,",",individuals.EliteMapPos,",",individuals.i_box_Elite,",",individuals.j_box_Elite])
        
    # calculate if its individual 
    
    
    #population.current_ind_instances.sort(key=lambda x: x.euclid,reverse=False)

    # for i in range(0,worst_to_remove):# kill bottom half NOTE must be less than pop number of crash
    #     print "popping an ind"
    #     topop = population.current_ind_instances[i]
    #     topop.alive = False # this way the historical population can still be sorted for alive True/False 
    #     population.current_ind_instances.pop(0) # remove the individual from the current list 
    #print "New pop of X Elites with X Weaker removed "    
    #print_all_current(population)
    for i in range (0,len(population.current_ind_instances)):
        if population.current_ind_instances[i].isElite == False:
            print "individual",population.current_ind_instances[i].indnum
            population.current_ind_instances.pop(i)


    for individuals in population.current_ind_instances:

        print "Surviving individual", individuals.indnum, "Euclid", individuals.euclid
        individuals.parent_of_gen = (population.gencount) + 1
        individuals.isElite = True
        file_ind = "Results/Individuals/ind%sgen%s.csv" % ((individuals.indnum),(individuals.gen))
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            #writer.writerow([individual.euclid,",",'Euclidean'])
            writer.writerow([individuals.sim_success,",",'Sim Sucess'])
            writer.writerow([individuals.real_success,",",'Real Sucess'])
            writer.writerow([individuals.parent_of_gen,",",'Parent of Generation'])
            writer.writerow([individuals.acc_euclid,",",'Acc Euclidean Generation'])
    print "      THE    CURRENT    POPULATION IS    ",   population.gencount      
    population.gencount = population.gencount + 1
    print "      THE    NEW   POPULATION IS    ",   population.gencount      
    generate_new_gen(population)

def generate_new_gen(remain_ind):
    # recall remain_ind is the entire population 
    #numpoints = [2,9]
    #xmin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]
    #xmax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]
    #ymin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]#[-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
    #ymax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]#[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    #zmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    #zmax = [1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8]
    #vmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    #vmax = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    #remain_ind.current_ind_instances holds X number of Elites 
    #remain_ind.gencount = remain_ind.gencount + 1
    print "The new Generation number is ", remain_ind.gencount
    worst_to_remove = ((remain_ind.numberinds)/2)
    #newnum = 20 # this is how many new individuals to generate
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
            remain_ind.generate_inds(1,remain_ind.numpoints,remain_ind.xmin,remain_ind.xmax,remain_ind.ymin,remain_ind.ymax,remain_ind.zmin,remain_ind.zmax,remain_ind.vmin,remain_ind.vmax,remain_ind.gencount)
        else: individuals_to_reproduce.append(choice)
        choice_two = random.choice(remain_ind.current_ind_instances)
        #max_loop = 0
        while choice_two == choice: # ensures we dont have double ups
            print "woops we had to choose again because we doubled up"
            choice_two = random.choice(remain_ind.current_ind_instances)
            #max_loop = max_loop + 1
        if choice_two.euclid == 0:
            print "This was a bad choice_two because its euclid was zero, generate a new random ind"   
            remain_ind.generate_inds(1,remain_ind.numpoints,remain_ind.xmin,remain_ind.xmax,remain_ind.ymin,remain_ind.ymax,remain_ind.zmin,remain_ind.zmax,remain_ind.vmin,remain_ind.vmax,remain_ind.gencount)
        else: individuals_to_reproduce.append(choice_two)
        if i < (worst_to_remove-2): # to make sure we dont end up with just one value in the list and therefore self replicating
            remain_ind.current_ind_instances.pop(0)

    # results in a list 20 parents long, that can have repeats of the best parents
    remain_ind.current_ind_instances.pop(0) # pop the last one in the list ready fro the next iteration 
    for individuals in individuals_to_reproduce:
        print "Luck Individual",individuals.indnum
        file_ind = "Results/Population/gen%s.csv" % (individuals.gen)
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([individuals.gen,",",'Generation'])
            writer.writerow([individuals.num_points,",",'NumberPoints'])
            writer.writerow([individuals.indnum,",",'Individual'])
            writer.writerow([individuals.vmax,",",'Vmax'])
            writer.writerow([individuals.xpos,",",'Xpos'])
            writer.writerow([individuals.ypos,",",'Ypos'])
            writer.writerow([individuals.zpos,",",'Zpos'])
            writer.writerow([individuals.vmax,",",'Vmax'])
            #writer.writerow([individual.sim_success,",",'Sim Sucess'])
            #writer.writerow([individual.sim_success,",",'Real Sucess'])

    ### Above has generated 10 Pairs of Parents, they will may repeat but Superior fitness gives a better opportunity to repopulate. 
    for  i in range (0, ((remain_ind.numberinds)/2)):
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
                gene_to_mutate = random.randint(0,max_wp_length-1)
                sigma = 0.1
                value = individuals.xpos[gene_to_mutate] 
                individuals.xpos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
                value = individuals.ypos[gene_to_mutate] 
                individuals.ypos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
                value = individuals.zpos[gene_to_mutate] 
                individuals.zpos[gene_to_mutate] = random.gauss(value,sigma)#(value * 20.0)
        print "Finished Mutating"
        individuals.printIndnum()
    # Make sure that mutations dont cause issues and check all valid waypoints
    check_valid_waypoints(remain_ind.current_ind_instances)

def check_valid_waypoints(remain_ind): 
    max_reach = 1.25 # Specs State 1.3m Reach
    for individuals in remain_ind:
        if individuals.sim_run == False:

            for i in range (0 , (len(individuals.xpos))):
                x_check = individuals.xpos[i]
                y_check = individuals.ypos[i]
                z_check = individuals.zpos[i]
                p1 = (x_check,y_check,y_check)#(float(valsZ[i])))
                p2 = (0.0,0.0,0.0)
                euclid_check = distance.euclidean(p2,p1)         
                while (euclid_check > max_reach):
                    print euclid_check,"Euclidean Checked and was found to be bad resizing to bring into range"
                    individuals.xpos[i] = (individuals.xpos[i]* 0.9)
                    individuals.ypos[i] = (individuals.ypos[i]* 0.9)
                    individuals.zpos[i] = (individuals.ypos[i]* 0.9)
                    x_check = individuals.xpos[i]
                    y_check = individuals.ypos[i]
                    z_check = individuals.zpos[i]
                    p1 = (x_check,y_check,y_check)#(float(valsZ[i])))
                    euclid_check = distance.euclidean(p2,p1)
                print euclid_check,"New Euclidean Accepted For", individuals.indnum

def cal_acc_euclid(remain_ind):
    #for individuals in remain_ind:
    for individuals in remain_ind.current_ind_instances:    
        #if individuals.sim_run == True:
        print "ind num in acc auclid", individuals.indnum
        for i in range (0 , (len(individuals.xpos))):
            x_check = individuals.xpos[i]
            y_check = individuals.ypos[i]
            z_check = individuals.zpos[i]
            p1 = (x_check,y_check,y_check)#(float(valsZ[i])))
            p2 = (0.0,0.0,0.0)
            point_euclid_add = distance.euclidean(p2,p1)  
            individuals.acc_euclid = individuals.acc_euclid + point_euclid_add

# def cal_vel_score(remain_ind):
#     #for individuals in remain_ind:
#     for individuals in remain_ind.current_ind_instances:    
#         if individuals.sim_run == False:
#             print "ind num in acc auclid", individuals.indnum
#             for i in range (0 , (len(individuals.xpos))):
#                 ()
                # x_check = individuals.xpos[i]
                # y_check = individuals.ypos[i]
                # z_check = individuals.zpos[i]
                # p1 = (x_check,y_check,y_check)#(float(valsZ[i])))
                # p2 = (0.0,0.0,0.0)
                # point_euclid_add = distance.euclidean(p2,p1)  
                # individuals.acc_euclid = individuals.acc_euclid + point_euclid_add


def cal_ifElite(remain_ind):
    # passes the whole population
    for individuals in remain_ind.current_ind_instances:
        # check all have i and j referrances
        which_box(individuals)
        indiv_to_check_against = []

        for ind_to_check in remain_ind.indinstanceshistory:
            if individuals.i_box_Elite == ind_to_check.i_box_Elite and individuals.j_box_Elite == ind_to_check.j_box_Elite:
                # these are in the same bob
                indiv_to_check_against.append(ind_to_check)
        false_count = 0
        for ind_to_check_against in indiv_to_check_against:
            #check against the list we just made
            if individuals.euclid > ind_to_check_against.euclid:
                individuals.isElite = True
                print "Individual was better than someone ", individuals.indnum
            if individuals.euclid < ind_to_check_against.euclid:
                false_count = false_count + 1
        if false_count < 5:
            # in the top 5 for all generations
            print "Individual ", individuals.indnum, "is Elite"
            individuals.isElite = True
   
  
    

def which_box(ind):

    if ind.acc_euclid > 0.0 and  ind.acc_euclid <= 1.2:
        ind.i_box_Elite = 0
    if ind.acc_euclid > 1.2 and  ind.acc_euclid <= 2.4:
        ind.i_box_Elite = 1
    if ind.acc_euclid > 2.4 and  ind.acc_euclid <= 3.6:
        ind.i_box_Elite = 2
    if ind.acc_euclid > 3.6 and  ind.acc_euclid <= 4.8:
        ind.i_box_Elite = 3
    if ind.acc_euclid > 4.8:
        ind.i_box_Elite = 4

    if (ind.vmax > 0.0 and ind.vmax <= 0.1):
        ind.j_box_Elite = 0
    if (ind.vmax > 0.1 and ind.vmax <= 0.2):
        ind.j_box_Elite = 1
    if (ind.vmax > 0.2 and ind.vmax <= 0.3):
        ind.j_box_Elite = 2
    if (ind.vmax > 0.3 and ind.vmax <= 0.4):
        ind.j_box_Elite = 3
    if (ind.vmax > 0.4):
        ind.j_box_Elite = 4





def generate_new_children(remain_ind,parent_1, parent_2):
    #Passed the entire population and specificially the two parents that will generate two children. 
    crossover_point = 0 # this will be set later
    equal = False # are the two individuals equal length 
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
    child_1x = []#Ready for the new child xpos/ypos/zpos
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
        print "Even Cross over from Half Chromo"

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
    remain_ind.indcount = remain_ind.indcount + 1
    add = Individual(remain_ind.indcount,child_1num,child_1x,child_1y,child_1z,child_1v,remain_ind.gencount)
    remain_ind.current_ind_instances.append(add)
    remain_ind.indinstanceshistory.append(add)

    remain_ind.indcount = remain_ind.indcount + 1
    add = Individual(remain_ind.indcount,child_2num,child_2x,child_2y,child_2z,child_2v,remain_ind.gencount)
    remain_ind.current_ind_instances.append(add)
    remain_ind.indinstanceshistory.append(add)
    
