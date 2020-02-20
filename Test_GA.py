from Population import Population
#from Thesis_python_interface import MoveGroupPythonIntefaceTutorial
import time
import sys
import time
import copy
import rospy
import random
#import moveit_commander
#import moveit_msgs.msg
#import geometry_msgs.msg
from math import pi
#from std_msgs.msg import String
#from moveit_commander.conversions import pose_to_list
#from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetLinkState
#from gazebo_msgs.msg import LinkState
#from odom import Odom
#from multiprocessing import Process , Queue
from GA import *
from scipy.spatial import distance


def evaluate_test(ind):
    # evaluate an individual 
    p1 = ()
    p2 = ()
    print "Last X ", ind.xpos[-1],"Y ",ind.ypos[-1],"Z",ind.zpos[-1]
    p1 = (0.0,0.0,0.0)
    p2 = (ind.xpos[-1],ind.ypos[-1],ind.zpos[-1])#last point
    print "P1 ",p1
    print "P2 ",p2
    ind.euclid = distance.euclidean(p1,p2)
    print " New Euclid ==== ",ind.euclid
    print "Evaluation Done on ", ind.indnum
    #time.sleep(1)



def main():


    print "The test has started"
    # Initial population has these ranges for 10 positions
    numpoints = [1,9]
    xmin = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
    xmax = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    ymin = [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
    ymax = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    zmin = [0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3]
    zmax = [1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2]
    vmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    vmax = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    

    print "Generating a population"
    pop = Population(20)
    #Generate an initial population of 20
    pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax)
    pop.gen_wp()
    loops = 0
    
    while (1):

        # SIMULATOR LOOP IND are updated with a Euclid distance 
        for individuals in pop.indinstances:
          #print "New Path entered and Model Pos" 
          #print model_info_prox    
            #print "Can I Home? waiting on Raw Input"
            #raw_input()
          #print "Should be at home position"
          #tutorial.go_to_joint_state(0.1,-1.57,0.1,0.1,0.1,0.1) 
          rospy.sleep(2)
          if individuals.evaluated == False: # this line ensures we only do the new ones 
            pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
            #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,odom)

            evaluate_test(individuals)


            individuals.evaluated = True
          else:
            print "This individual", individuals.indnum," with euclid",individuals.euclid," was already assessed... skipping to next"


        print "Evaluation Cycle"
        print "Sorting the individuals in this population"
        pop.indinstances.sort(key=lambda x: x.euclid,reverse=False)
        ###Below CALLS GA FUNCTIONS FOR GA AND NEW POP INSTANCES
        #print_all(pop) #GA function call to print all individuals
        evaluate_ind(pop) # GA function call Note also generates the new individuals 

    print "============ Exiting the Loop!"


if __name__ == '__main__':
  main()