import time
#import Individual
from copy import deepcopy
from itertools import izip
import csv
from scipy.spatial import distance

def print_all(all_ind): # passed population

    for individuals in all_ind.indinstances:
        print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid

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






def evaluate_ind(all_ind): # recall the whole pop
    # ENTRY POINT OF GA
    worst = 5
    loop = 0
    ## Decision Point
    # Keep Best 5? 
    #Generate the actual Eucideans from two excell spreadsheets
    for individuals in all_ind.indinstances:
        calc_euclid(individuals)
    # sorts best to worst Euclidean 
    all_ind.indinstances.sort(key=lambda x: x.euclid,reverse=False)


    for i in range(0,10):# kill bottom 5 NOTE must be less than pop number of crash
        print "popping an ind"
        topop = all_ind.indinstances[i]
        topop.alive = False # this way the historical population can still be sorted for alive True/False 
        all_ind.indinstances.pop(0)
    print "New pop of 5 with 5 Dead"    
    print_all(all_ind)
    grabGenertics(all_ind)
    # now grab their genetics
    #es smallest to largest

    #for individuals in all_ind.indinstances:

    #Clear the current individuals
    #    all_ind.indinstances = []
def grabGenertics(remain_ind):
    newnum = 20 # this is how many new individuals to generate
    numpoints = []
    sortnumpoints = [] # list if two min max

    for individuals in remain_ind.indinstances:
        #get all of the possible min max num points and put them in a list 
        #individuals.printIndnum()
        #print "h"
        val = deepcopy(individuals.returnnumpoints())
        #print val
        #print "e"
        sortnumpoints.append(val)
        #print "re"
    sortnumpoints.sort()
    numpoints.append(sortnumpoints[0])    # new minimum
    numpoints.append(sortnumpoints[-1])   # new maximum
    print "new min max number points", numpoints
            

    new_xmin = [] # list if 10ish min max
    new_xmax= [] # list if 10ish min max
    new_ymin= [] # list if 10ish min max
    new_ymax= [] # list if 10ish min max
    new_zmin= [] # list if 10ish min max
    new_zmax= [] # list if 10ish min max
    new_vmin= [] # list if 10ish min max
    new_vmax= [] # list if 10ish min max

    for i in range(0,9):# CHANGE FOR POSSIBLE POINTS CHAANGE
        #create a list to sort for min max
        xold = []
        yold =[]
        zold = []
        vold = []
        #for each lasting individual
        for individuals in remain_ind.indinstances:
            try:
                #Get the historical target x y z for each point

                xold.append((individuals.returnx())[i])
                yold.append((individuals.returny())[i])
                zold.append((individuals.returnz())[i])
                vold.append((individuals.returnv())[i])
            except:
                print "may be no points to copy ie shorter array"
        #for each point Take each and sort to find new min max
        xold.sort()
        yold.sort()
        zold.sort()
        vold.sort()   
        # for each point add a new min and max
        try:
            new_xmin.append(xold[0]) # list if 10ish min max
            new_xmax.append(xold[-1]) # list if 10ish min max
            new_ymin.append(yold[0]) # list if 10ish min max
            new_ymax.append(yold[-1]) # list if 10ish min max
            new_zmin.append(zold[0]) # list if 10ish min max
            new_zmax.append(zold[-1]) # list if 10ish min max
            new_vmin.append(vold[0]) # list if 10ish min max
            new_vmax.append(vold[-1]) # list if 10ish min max
        except:
            print "Out of points"
        
        print "New Version Ind"
        print "Number Points",numpoints[0],num_points[1]
        print new_xmin#.append(xold[0]) # list if 10ish min max
        print new_xmax#.append(xold[-1]) # list if 10ish min max
        print new_ymin#.append(yold[0]) # list if 10ish min max
        print new_ymax#.append(yold[-1]) # list if 10ish min max
        print new_zmin#.append(zold[0]) # list if 10ish min max
        print new_zmax#.append(zold[-1]) # list if 10ish min max
        print new_vmin#.append(vold[0]) # list if 10ish min max
        print new_vmax#.append(vold[-1]) # list if 10ish min max        
        #from individual attributes below 
        #self.xpos = deepcopy(xpos)
        #self.ypos = deepcopy(ypos)
        #self.zpos = deepcopy(zpos)
        #self.vmax = deepcopy(vmax)
        #self.num_points = number_points
        #variable length assessment of the below
        

        #to arrays of new min and maxes
        #xmin = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
        #xmax = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        #ymin = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
        #ymax = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        #zmin = [0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3]
        #zmax = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2]
        #vmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        #vmax = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]


    #send the new min max for each coordinate point to the new population generator. 
    print "generating new pop of ", newnum
    remain_ind.generate_inds(newnum,numpoints,new_xmin,new_xmax,new_ymin,new_ymax,new_zmin,new_zmax,new_vmin,new_vmax)
    for individuals in remain_ind.indinstances:
        if individuals.evaluated == False:
            remain_ind.gen_wp()
    #######pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax)
    # reverse false fiv