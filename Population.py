

from Individual import Individual
import random
from datetime import datetime
import time
import sys
from GA import *
import csv


class Population:
    indcount = 1
    gencount = 0
    current_ind_instances = []
    indinstanceshistory = []
    def __init__(self,numberinds,restart_sim,last_ind):
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
        self.res_sim = restart_sim
        self.last_working_ind = last_ind

    def load_inds():
        print "We are starting a load of historical individuals, we assume the csv file is correct"
        
        file_ind = "Results/Population/totalgens.csv"
        #with open(file_ind, 'a') as csvfile:
        reader = csv.reader(file_ind)
        for row in reader:#range (1,self.last_working_ind):
            add = Individual(row[2],number_points,x_pos,y_pos,z_pos,v_max,gen)
            Population.indcount = row[2] #individual number
            add.saved_to_gens = True
            #0individuals.gen
            add.gen= row[0]
            #1'Generation
            #2individuals.indnum
            add.indnum= row[2]
            #3"Euclid"
            #4individuals.euclid,
            add.euclid= row[4]
            #5individuals.num_points
            add.num_points= row[]5
            #6individuals.xpos
            add.xpos= row[6]
            #7individuals.ypos
            add.ypos= row[7]
            #8individuals.zpos
            add.zpos= row[8]
            #9individuals.vmax
            add.vmax= row[9]
            #10 individuals.gen
            add.gen= row[10]
            #11 individuals.alive
            add.alive= row[11]
            #12 individuals.sim_run
            add.sim_run= row[12]
            #13 individuals.real_run
            add.real_run= row[13]
            #14 individuals.waypoints
            add.waypoints= row[14]
            #15 individuals.acc_euclid
            add.acc_euclid= row[15]
            #16 individuals.sim_success
            add.sim_success= row[16]
            #17 individuals.execute_success
            add.execute_success= row[17]
            #18 individuals.saved_to_gens
            add.saved_to_gens= row[18]
            #19 individuals.saved_to_gens
            add.saved_to_gens= row[19]
            #20 individuals.mutated
            add.mutated= row[20]
            #21 individuals.calc_euclid
            add.calc_euclid= row[21]
            #22 individuals.isElite
            add.isElite= row[22]
            #23 individuals.EliteMapPos
            add.EliteMapPos = row[23]
            # add the updated individual to the current inds in the population
            Population.current_ind_instances.append(add)
            Population.indinstanceshistory.append(add)

        




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


