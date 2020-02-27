

from Individual import Individual
import random
from datetime import datetime
import time
import sys
from GA import *

class Population:
    indcount = 1
    gencount = 1
    current_ind_instances = []
    indinstanceshistory = []
    def __init__(self,numberinds):
        
        
        self.numberinds = numberinds
        self.numbpoints = random.randint(1,10)
        #self.num_reproduce = numberinds
        #self.
        
        print "Init worked"
        



    def generate_inds(self,num,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,gen):
        print "Generating individuals"
        for x in range (0,num): # ie for each individual 
            
            x_pos = []
            y_pos = []
            z_pos = []
            v_max = []
            number_points = random.randint(numpoints[0],numpoints[1])
            #vals = [5,15,20,25,30,40,45,100,200,300,50]
            #random.seed(random.choice(vals))
            #random.shuffle(vals)
            key = random.SystemRandom()
            seed_key = key.randint(0,sys.maxint)
            #loop = 0
            #print "numbpoints", self.numbpoints
            for i in range (0,number_points):
                #print "Loop",loop
                #loop = loop + 1
                random.seed(seed_key)
                seed_key = key.randint(0,sys.maxint)
                #random.shuffle(vals)
                x_pos.append(random.uniform(xmin[i],xmax[i])) 
                random.seed(seed_key)
                seed_key = key.randint(0,sys.maxint)
                #random.shuffle(vals)
                y_pos.append(random.uniform(ymin[i],ymax[i])) 
                random.seed(seed_key)
                seed_key = key.randint(0,sys.maxint)
                #random.shuffle(vals)
                z_pos.append(random.uniform(zmin[i],zmax[i])) 
                random.seed(seed_key)
                seed_key = key.randint(0,sys.maxint)
                #random.shuffle(vals)
                v_max.append(random.uniform(vmin[i],vmax[i])) 

                #self.numpoints = random.randint(1,5)
            #print "numbpoints", self.numbpoints
            #print "Xpos", x_pos
            #print "ypos", y_pos

            add = Individual(Population.indcount,number_points,x_pos,y_pos,z_pos,v_max,gen)
            Population.current_ind_instances.append(add)
            Population.indinstanceshistory.append(add)
            Population.indcount = Population.indcount + 1
            #for each individual write a record




    def printpop(self):
        ()
        #print self.number
    
    def gen_wp(self):
        for individuals in Population.current_ind_instances:
            #individuals.printIndnum()
            #print "Generating the waypoints for the initial population"
            individuals.generate_wp()





        #self.me.printIndnum()


