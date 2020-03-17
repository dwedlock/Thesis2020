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
#from odom import Odom # this was attached to the old recording process
#import multiprocessing # this was attached to the old recording process
#from multiprocessing import Process , Queue # this was attached to the old recording process
from GA import *
#Physics 
from gravity import GravityControl

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
    # writer below is to pass sings to out Link Listener and recording program
    writer = rospy.Publisher('writer', String, queue_size=1)
    filestring = rospy.Publisher('filestring', String, queue_size=1)
    hello_str = "Test listener is working %s" % rospy.get_time()
    file_str = "/NewFile"
    writer.publish(hello_str)
    filestring.publish(file_str)
    print "Generating a population"
    pop = Population(20)
    grav = GravityControl()
    grav.init_values()
    grav.change_gravity(0.0,0.0,-9.8)

    generation = pop.gencount
    pop.generate_inds(pop.numberinds,numpoints,xmin,xmax,ymin,ymax,zmin,zmax,vmin,vmax,generation)
    pop.gen_wp()
    check_valid_waypoints(pop.current_ind_instances)
    print "Success adding table "
    time.sleep(1)
    print "============ Please ensure the Recorder is started and then Press `Enter` to execute joint state goal ..."
    raw_input()
    tutorial.go_to_joint_state(0.0,-0.5,0.0,0.0,0.0,0.0) # note Rads each joint 
    while (1):
        pop.gencount = pop.gencount + 1
        grav.change_gravity(0.0,0.0,-9.8)
        run_simulation(tutorial,pop,pop.gencount,filestring,writer)
        grav.change_gravity(0.0,0.0,-11.8)
        run_real(tutorial,pop,pop.gencount,filestring,writer)
        evaluate_pop(pop) # This is a GA function call to evauate this population before the next generatio   

    print "============ Exiting the Loop!"

def run_simulation(tutorial,pop,loops,filestring,writer):
  for individuals in pop.current_ind_instances:
    file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))
    file_str_real = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))
    print "New Path entered and Model Posmoving to home"
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    time.sleep(10)
    print "Should be at home position, all joints Zero, ready for Individual", individuals.indnum
    if individuals.sim_run == False: # this line ensures we only do the new ones
      file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))
      file_str_real = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (loops))
      filestring.publish(file_str)
      pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
    ## The line was removed because of a fault in the cartesian_plan software
    #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,writer)
    test = True
    for i in range(0,(len(individuals.xpos))):
      individuals.sim_success = True
      if test == True:
        return_tf = tutorial.go_to_pose_goal(1.0,individuals.xpos[i],individuals.ypos[i],individuals.zpos[i],individuals.vmax[i],writer)
      if test == True:
        test = return_tf
      if test == False:
        individuals.sim_success = False
        individuals.euclid = 0
        print "This individual ",individuals.indnum," has a bad waypoint given a Eucidean of Zero"
        individuals.sim_run = True
      else:
        print " "

def run_real(tutorial,pop,loops,filestring,writer):
  print "Running Real"
  for individuals in pop.current_ind_instances:

    file_str = "Results/Real/ind%sgen%s.csv" % ((individuals.indnum), (loops))
    
    print "REAL",individuals.indnum, " New Path entered and Model Posmoving to home"
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    time.sleep(10)
    print "REAL Should be at home position, all joints Zero, ready for Individual", individuals.indnum
    if individuals.real_run == False: # this line ensures we only do the new ones
      file_str = "Results/Real/ind%sgen%s.csv" % ((individuals.indnum), (loops))

      filestring.publish(file_str)
      pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
    ## The line was removed because of a fault in the cartesian_plan software
    #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,writer)
    test = True
    for i in range(0,(len(individuals.xpos))):
      individuals.real_success = True
      if test == True:
        return_tf = tutorial.go_to_pose_goal(1.0,individuals.xpos[i],individuals.ypos[i],individuals.zpos[i],individuals.vmax[i],writer)
      if test == True:
        test = return_tf
      if test == False:
        individuals.real_success = False
        individuals.euclid = 0
        print "This Real individual ",individuals.indnum," has a bad waypoint given a Eucidean of Zero"
        individuals.real_run = True
      else:
        print "This Real individual", individuals.indnum," with euclid",individuals.euclid," was already assessed... skipping to next"

if __name__ == '__main__':
  main()