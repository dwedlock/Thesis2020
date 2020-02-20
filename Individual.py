

from copy import deepcopy

class Individual:

    def __init__(self,indnum,number_points,xpos,ypos,zpos,vmax):
        self.alive = True
        self.evaluated = False
        self.indnum = indnum
        self.xpos = deepcopy(xpos)
        self.ypos = deepcopy(ypos)
        self.zpos = deepcopy(zpos)
        self.vmax = deepcopy(vmax)
        self.num_points = number_points
        self.waypoints = []
        self.euclid = 50000 # super large number to begin with
        print "Init Ind", indnum, "completed"

    def printIndnum(self):
        print "Turn this on for all stats print"
        #print self.indnum
        #print self.xpos
        #print self.ypos
        #print self.zpos
        #print self.vmax

    def generate_wp(self):
        loop = 0
        print "num points ",self.num_points
        for i in range(0,self.num_points):
            #print "Loop",loop
            loop = loop + 1
            self.waypoints.append(self.xpos[i])
            self.waypoints.append(self.ypos[i])
            self.waypoints.append(self.zpos[i])
            self.waypoints.append(self.vmax[i])
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