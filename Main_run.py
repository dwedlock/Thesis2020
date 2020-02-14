from Population import Population
from Thesis_python_interface import MoveGroupPythonIntefaceTutorial
import time
import sys
import time
import copy
import rospy
import random
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from gazebo_msgs.srv import GetModelState, GetModelStateRequest, GetLinkState
from gazebo_msgs.msg import LinkState
from odom import Odom
from multiprocessing import Process , Queue
from GA import *

def main():


    print "Python has started"
    tutorial = MoveGroupPythonIntefaceTutorial()
    model_info_prox = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    rospy.wait_for_service('/gazebo/get_link_state')
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
    #pop.printpop()
    #Generate an initial population of 20
    pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax)
    # print the whole population 
    pop.gen_wp()

    print "adding a table for collisions"
    tutorial.add_box()
    print "Success adding table "
    time.sleep(1)

    print "============ Press `Enter` to execute joint state goal ..."
    raw_input()
    tutorial.go_to_joint_state(0.0,-0.5,0.0,0.0,0.0,0.0) # note Rads each joint 
  #print "============ Press `Enter` to execute a movement using a pose goal ..."
  
  #raw_input()
  #tutorial.go_to_pose_goal(1.0,0.2,0.1,0.4) #W X Y Z
    #xx = 0.1
    #yy = 0.1
    #zz = 0.1
    loops = 0
    q = Queue()
    q2 = Queue()
    odom = Odom(q,q2)
    
    while (1):
      #random.seed(5)
      #xx = xx+0.1
      #y = yy+0.1
      #zz = zz+0.1

        print loops
        loops = loops + 1
        #print_all(pop)

        # SIMULATOR LOOP IND are updated with a Euclid distance 
        for individuals in pop.indinstances:
          print "New Path entered and Model Pos" 
          #print model_info_prox    
            #print "Can I Home? waiting on Raw Input"
            #raw_input()
          print "Should be at home position"
          tutorial.go_to_joint_state(0.1,-1.57,0.1,0.1,0.1,0.1) 
          rospy.sleep(2)
          if individuals.evaluated == False: # this line ensures we only do the new ones 
            pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
            cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,odom)
            individuals.evaluated = True
          else:
            print "This individual was already assessed skipping to next"

            #odom.run()
            #print "waiting on Raw Input"
            #raw_input()

        print "Evaluation Cycle"
        print "Sorting the individuals in this population"
        pop.indinstances.sort(key=lambda x: x.euclid,reverse=False)
        ###CALL GA FUNCTIONS FOR GA AND NEW POP INSTANCES

        print_all(pop)
        evaluate_ind(pop)


        #for individuals in pop.indinstances:
        #  print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid
          #evaluate_ind(individuals)


          

    print "============ Exiting the Loop!"





if __name__ == '__main__':
  main()