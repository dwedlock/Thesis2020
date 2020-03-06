

from copy import deepcopy
import csv

class Individual:

    def __init__(self,indnum,number_points,xpos,ypos,zpos,vmax,gen):
        self.alive = True
        self.sim_run = False
        self.indnum = indnum
        self.xpos = deepcopy(xpos)
        self.ypos = deepcopy(ypos)
        self.zpos = deepcopy(zpos)
        self.vmax = deepcopy(vmax)
        self.num_points = number_points
        self.waypoints = []
        self.euclid = 0 #
        self.gen = gen
        self.success = False
        self.mutated = False
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
            #print "Loop",loop
            loop = loop + 1
            self.waypoints.append(self.xpos[i])
            self.waypoints.append(self.ypos[i])
            self.waypoints.append(self.zpos[i])
            self.waypoints.append(self.vmax[i])
        
        file_ind = "Results/Individuals/ind%sgen%s.csv" % ((self.indnum),(self.gen))
        with open(file_ind, 'a') as csvfile:
            writer = csv.writer(csvfile,delimiter= ' ',quotechar ='|',quoting = csv.QUOTE_MINIMAL)
            writer.writerow([self.gen],'Generation')
            writer.writerow([self.indnum],'Individual Number')
            writer.writerow([self.num_points],'Number of points')
            #for val in self.xpos:
            
            writer.writerows(self.xpos)
            writer.writerows(self.ypos)
            writer.writerows(self.zpos)
            writer.writerows(self.vmax)            

        #print "My Waypoints"
        #print self.waypoints

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