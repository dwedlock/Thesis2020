
from copy import deepcopy
import csv

class Individual:

    def __init__(self,indnum,number_points,xpos,ypos,zpos,vmax,gen):
        self.gen = gen
        self.indnum = indnum
        self.euclid = 0 #
        self.num_points = number_points
        self.xpos = deepcopy(xpos)
        self.ypos = deepcopy(ypos)
        self.zpos = deepcopy(zpos)
        self.vmax = vmax

        self.alive = True
        self.sim_run = False
        self.real_run = False      
        self.waypoints = []
        self.acc_euclid = 0
        self.sim_success = False
        self.real_success = False
        self.execute_success = False
        self.parent_of_gen = 0 
        self.plan_1 = []
        self.saved_to_gens = False
        self.mutated = False
        self.calc_euclid = False
        self.isElite = False
        self.EliteMapPos = 0
        self.i_box_Elite = 0
        self.j_box_Elite = 0
        print "Init Ind", indnum, "completed"

    def printIndnum(self):
        print " Printing"
        #print "Turn this on for all stats print"
        print self.indnum
        print "X", str(self.xpos)[1:-1]
        print "Y", str(self.ypos)[1:-1]
        print "Z", str(self.zpos)[1:-1]
        print "V", str(self.vmax)[1:-1]

    def generate_wp(self):
        loop = 0
        #print "num points ",self.num_points
       
        for i in range(0,self.num_points):
            try:
                #print "Loop",loop
                loop = loop + 1
                self.waypoints.append(self.xpos[i])
                self.waypoints.append(self.ypos[i])
                self.waypoints.append(self.zpos[i])
                self.waypoints.append(self.vmax[i])
            except:
                print "might have a bad wp"
        file_ind = "Results/Individuals/ind%sgen%s.csv" % ((self.indnum),(self.gen))
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([self.gen,",",'Generation'])
            writer.writerow([self.indnum,",",'Individual Number'])
            writer.writerow([self.num_points,",",'Number of points'])  

            for i in range (0 , (len(self.xpos))):
                #error her
                #try:
                writer.writerow([self.xpos[i],",",self.ypos[i],",",self.zpos[i],",",self.vmax])
                #writer.writerow(self.ypos)
                #writer.writerow(self.zpos)
                #writer.writerow(self.vmax)   
                 #except:
                #    print "Might have a bad WP"         

    def returnnumpoints(self):
        return self.num_points

    def returnx(self):
        return self.xpos

    def returny(self):
        return self.ypos

    def returnz(self):
        return self.zpos

    def returnv(self):
        return self.vmax