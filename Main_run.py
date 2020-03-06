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
import multiprocessing 
from multiprocessing import Process , Queue
from GA import *



def main():


    print "Python has started"
    tutorial = MoveGroupPythonIntefaceTutorial()
    model_info_prox = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    rospy.wait_for_service('/gazebo/get_link_state')
    # Initial population has these ranges for 10 positions
    numpoints = [2,9]
    xmin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]
    xmax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]
    ymin = [-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9,-0.9]#[-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5]
    ymax = [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]#[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    zmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    zmax = [1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8]
    vmin = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    vmax = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
    

    rospy.wait_for_service('/gazebo/get_model_state')
    writer = rospy.Publisher('writer', String, queue_size=1)
    filestring = rospy.Publisher('filestring', String, queue_size=1)
    hello_str = "hello world %s" % rospy.get_time()
    file_str = "/NewFile"
    #rospy.loginfo(hello_str)
    writer.publish(hello_str)
    filestring.publish(file_str)
    print "Generating a population"
    pop = Population(20)
    #pop.printpop()
    #Generate an initial population of 20
    generation = pop.gencount
    pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,generation)
    # print the whole population 
    pop.gen_wp()

    print "adding a table for collisions"
    #tutorial.add_box()
    print "Success adding table "
    time.sleep(1)

    print "============ Please start Recorder and then Press `Enter` to execute joint state goal ..."
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
    #odom = Odom(q,q2)
    #odom.run() # THis starts the logger of data 

    while (1):
      #random.seed(5)
      #xx = xx+0.1
      #y = yy+0.1
      #zz = zz+0.1

        print loops
        loops = loops + 1
        #print_all(pop)

        # SIMULATOR LOOP IND are updated with a Euclid distance 
        for individuals in pop.current_ind_instances:

          file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))

          print "New Path entered and Model Pos" 
          #print model_info_prox    
            #print "Can I Home? waiting on Raw Input"
            #raw_input()
          print "moving to home"
          tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
          time.sleep(10)
          #tutorial.go_to_joint_state(0.1,-1.57,0.1,0.1,0.1,0.1) 
          #tutorial.go_to_pose_goal(1,0.2,0.2,0.6)
          #rospy.sleep(2)
          print "Should be at home position, all joints Zero"
          if individuals.sim_run == False: # this line ensures we only do the new ones
            #inst_str = "Start" #%s" % rospy.get_time()
            #individuals.gen = pop.gencount
            file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))
            #writer.publish(inst_str)
            filestring.publish(file_str)

            pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
            ## This line was removed 
            #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,writer)
            test = True
            for i in range(0,(len(individuals.xpos))):
              individuals.success = True
              if test == True:
                return_tf = tutorial.go_to_pose_goal(1.0,individuals.xpos[i],individuals.ypos[i],individuals.zpos[i],individuals.vmax[i],writer)
              if test == True:
                test = return_tf
              if test == False:
                individuals.success = False
                individuals.euclid = 0

                print "This individual ",individuals.indnum," has a bad waypoint given a Eucidean of Zero"


              #time.sleep(.1)
            



            individuals.sim_run = True
            #inst_str = "Stop"
            #writer.publish(inst_str)
          else:
            print "This individual", individuals.indnum," with euclid",individuals.euclid," was already assessed... skipping to next"


            #
            #print "waiting on Raw Input"
            #raw_input()

        print "Evaluation Cycle"
        print "Sorting the individuals in this population"
        #pop.indinstances.sort(key=lambda x: x.euclid,reverse=False)
        ###CALL GA FUNCTIONS FOR GA AND NEW POP INSTANCES
        #print_all(pop)
        evaluate_pop(pop) # This is a GA function call to evauate this population before the next generation


        #for individuals in pop.indinstances:
        #  print "Sorted Individual by Euclid", individuals.indnum,": Euclidean Score " ,individuals.euclid
          #evaluate_pop(individuals)


          

    print "============ Exiting the Loop!"





if __name__ == '__main__':
  main()