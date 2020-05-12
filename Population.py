

from Individual import Individual
import random
from datetime import datetime
import time
import sys
from GA import *

class Population:
    indcount = 1
    gencount = 0
    current_ind_instances = []
    indinstanceshistory = []
    def __init__(self,numberinds):
        self.numberinds = numberinds
        #self.numbpoints = random.randint(1,10)
        #self.pop_size
        print "Init Population worked"
        self.numpoints = [2,4]
        self.xmin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]
        self.xmax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]
        self.ymin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]#[-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
        self.ymax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]#[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
        self.zmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
        self.zmax = [1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8]
        self.vmin = [0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
        self.vmax = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

    def generate_inds(self,num,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,gen):
        #self.pop_size = num
        print "Generating individuals"
        for x in range (0,num): # ie for each individual 
            
            x_pos = []
            y_pos = []
            z_pos = []
            v_max = []
            number_points = random.randint(numpoints[0],numpoints[1])
            key = random.SystemRandom()
            seed_key = key.randint(0,sys.maxint)
            for i in range (0,number_points):
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
            add = Individual(Population.indcount,number_points,x_pos,y_pos,z_pos,v_max,gen)
            Population.current_ind_instances.append(add)
            Population.indinstanceshistory.append(add)
            Population.indcount = Population.indcount + 1

    def printpop(self):
        ()
        #print self.number
    
    def gen_wp(self):
        for individuals in Population.current_ind_instances:
            individuals.generate_wp()


