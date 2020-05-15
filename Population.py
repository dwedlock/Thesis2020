

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
        #self.Elites = [][]

    def load_inds(self):
        print "We are starting a load of historical individuals, we assume the csv file is correct"
        
        file_ind = open("Results/Population/totalgens.csv","rb")
        #with open(file_ind, 'a') as csvfile:
        reader = csv.reader(file_ind)

        for row in reader:#range (1,self.last_working_ind):
            print "waypoints",row[5]#,"one",row[1],"one",row[2]
            ind = int(row[2])
            gen = int(row[0])
            x_pos = []
            y_pos = []
            z_pos = []
            v_max = []

            print "ind gen",ind,gen   
            file_ind_waypoints = open("Results/Individuals/ind%sgen%s.csv" % ((ind),(gen)),"rb")
            #with open(file_ind, 'a') as csvfile:
            reader_wp = csv.reader(file_ind_waypoints)
            i = 0
            for rows in reader_wp:#range (1,self.last_working_ind):
                #print "Row Zero",rows[0]#,"one",rows[1],"one",rows[2]
                if (i > 2) and (i < (3+int(row[5]))):
                    print "i",i,"zero",rows[0],"one",rows[1],"two",rows[2]###
                    x_pos.append(float(rows[0]))
                    y_pos.append(float(rows[1]))
                    z_pos.append(float(rows[2]))
                    v_max.append(float(rows[3]))

                i = i+1
            
            number_points = int(row[5])
            
            add = Individual(int(row[2]),number_points,x_pos,y_pos,z_pos,v_max,gen)
            Population.indcount = int(row[2]) #individual number
            add.saved_to_gens = True
            #0individuals.gen
            add.gen= int(row[0])
            #1'Generation
            #2individuals.indnum
            add.indnum= int(row[2])
            #3"Euclid"
            #4individuals.euclid,
            add.euclid= float(row[4])
            #5individuals.num_points
            add.num_points= int(row[5])
            # #6individuals.xpos
            # add.xpos= row[6]
            # #7individuals.ypos
            # add.ypos= row[7]
            # #8individuals.zpos
            # add.zpos= row[8]
            # #9individuals.vmax
            # add.vmax= row[9]
            #6 individuals.gen
            add.gen= int(row[6])
            #7 individuals.alive
            add.alive= bool(row[7])
            #8 individuals.sim_run
            add.sim_run= bool(row[8])
            #9 individuals.real_run
            add.real_run= bool(row[9])
            ##14 individuals.waypoints
            ##add.waypoints= row[14]
            #10 individuals.acc_euclid
            add.acc_euclid= float(row[10])
            #11 individuals.sim_success
            add.sim_success= bool(row[11])
            #12 individuals.execute_success
            add.execute_success= bool(row[12])
            #13 individuals.saved_to_gens
            add.saved_to_gens= bool(row[13])
            #14 individuals.saved_to_gens
            add.saved_to_gens= bool(row[14])
            #15 individuals.mutated
            add.mutated= bool(row[15])
            #16 individuals.calc_euclid
            add.calc_euclid= bool(row[16])
            #17 individuals.isElite
            add.isElite= bool(row[17])
            #18 individuals.EliteMapPos
            add.EliteMapPos = int(row[18])
            # add the updated individual to the current inds in the population
            add.i_box_Elite= int(row[19])
            #18 individuals.EliteMapPos
            add.j_box_Elite = int(row[20])
            # add the updated individual to the current inds in the population
            #self.i_box_Elite = 0
            #self.j_box_Elite = 0

            print "printing an individual"
            add.printIndnum()
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

            allvelocity = random.uniform(vmin[1],vmax[1])

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
                v_max.append(allvelocity) 
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


