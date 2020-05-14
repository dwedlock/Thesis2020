#!/usr/bin/env python
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
#import os


#from odom import Odom # this was attached to the old recording process
#import multiprocessing # this was attached to the old recording process
#from multiprocessing import Process , Queue # this was attached to the old recording process
from GA import *
#Physics 
from gravity import GravityControl
from velocity import VelocityControl

def main():
    """
    This is the main program for running the simulation and real....
    Before launching please launch in order:

      roslaunch ur_gazebo ur10_joint_limited.launch
      roslaunch ur10_moveit_config ur10_moveit_planning_execution.launch sim:=true
      roslaunch ur10_moveit_config moveit_rviz.launch config:=true
      python Listen_link.py 
      python Main_run.py
    """
    print "Python has started"
    #os.system("xterm -e \"pyhton Listen_link.py\"")   
    #print "Started Listener"
    tutorial = MoveGroupPythonIntefaceTutorial()
    model_info_prox = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    rospy.wait_for_service('/gazebo/get_link_state')
    rospy.wait_for_service('/gazebo/get_model_state')
    # writer below is to pass sings to out Link Listener and recording program
    writer = rospy.Publisher('writer', String, queue_size=1)
    filestring = rospy.Publisher('filestring', String, queue_size=1)
    rospy.set_param('/move_group/trajectory_execution/allowed_start_tolerance',0)
    hello_str = "Test listener is working %s" % rospy.get_time()
    file_str = "/NewFile"
    writer.publish(hello_str)
    filestring.publish(file_str)
    print "Generating a population"
    pop = Population(8,False,0) #should be an even number 10-20 
    if pop.gencount == 0:
      pop.gencount = pop.gencount + 1
    grav = GravityControl()
    velocity = VelocityControl()
    grav.init_values()
    grav.change_gravity(0.0,0.0,-9.8)

    generation = pop.gencount
    if pop.res_sim == False:
      pop.generate_inds(pop.numberinds,pop.numpoints,pop.xmin,pop.xmax,pop.ymin,pop.ymax,pop.zmin,pop.zmax,pop.vmin,pop.vmax,generation)
      pop.gen_wp()
    if pop.res_sim == True:
      pop.load_inds()

    check_valid_waypoints(pop.current_ind_instances)
    print "Success adding table "
    time.sleep(1)
    print "============ Please ensure the Recorder is started and then Press `Enter` to execute joint state goal ..."
    raw_input()
    tutorial.go_to_joint_state(0.0,-0.5,0.0,0.0,0.0,0.0) # note Rads each joint 
    # The main loop for the program is below
    while (pop.gencount<100):
        
        grav.change_gravity(0.0,0.0,-9.8)
        print "Starting for population count number", pop.gencount
        run_simulation(tutorial,pop,pop.gencount,filestring,writer,velocity)
        #make gravity Heavier to change simulation of 'real' slightly
        grav.change_gravity(0.0,0.0,-11.8)
        run_real(tutorial,pop,pop.gencount,filestring,writer,velocity)
        # Evaluate, also calculates Euclidean based on collected data points between sim and real
        evaluate_pop(pop) # This is a GA function call to evauate this population before the next generatio   
        

    print "============ Exiting the Loop!"

def run_simulation(tutorial,pop,loops,filestring,writer,velocity):
  for individuals in pop.current_ind_instances:
    file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))
    file_str_real = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))
    print "New Path entered and Model Posmoving to home"
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    time.sleep(10)
    print "Should be at home position, all joints Zero, ready for Individual", individuals.indnum,"Gen",individuals.gen
    if individuals.sim_run == False: # this line ensures we only do the new ones
      file_str = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))
      file_str_real = "Results/Sim/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))
      filestring.publish(file_str)
      pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
      #individuals.sim_success = True
    ## The line was removed because of a fault in the cartesian_plan software
    #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,writer)
    test = True
    ##Generate Plans for Each Waypoints
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    
    # Below starts the planner for each individual in the population
    # This is a slow process and requires greater computational time. 
    # There is a pause between waypoints however the successful plans are saved for execution later. 

    if individuals.sim_run == False:
      print "Starting Planner"
      time.sleep(10)
      for i in range(0,(len(individuals.xpos))):
        #individuals.sim_success = True
        if test == True:
          return_tf = tutorial.go_to_pose_goal(1.0,individuals.xpos[i],individuals.ypos[i],individuals.zpos[i],individuals.vmax[i],writer,individuals,i)
          individuals.sim_run = True
        if test == True:
          test = return_tf
          individuals.sim_success = True
          
        if test == False:
          print "Test Result",test
          individuals.sim_success = False
          individuals.euclid = 0
          print "RUN Sim This individual ",individuals.indnum," has a bad waypoint given a Eucidean of Zero"
          individuals.sim_run = True
        else:
          print " "
    ##Execute Plans for each way point
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    
    # Below executes the sucessful plans for each waypoint, this is a fast process and needs to be recorded. 

    print "About to execute for ind number ",individuals.indnum,"Success is ",individuals.sim_success
    time.sleep(10)
    inst_str = "start" 
    writer.publish(inst_str) # Starts the Listener
    time.sleep(1)
    if individuals.sim_success == True and individuals.execute_success == False:
      inst_str = "start" 
      writer.publish(inst_str) # Starts the Listener
      for i in range(0,(len(individuals.xpos))):
        #for each waypoint
        print "Moving to a point"
        tutorial.execute_plan(individuals.plan_1[i])
    inst_str = "stop"
    writer.publish(inst_str) # Starts the Listener
    inst_str = "stop"
    writer.publish(inst_str) # Starts the Listener
    #if individuals.sim_success == True:
      #print "We had a good plan and excecution, now do velocity component"
      #tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) #home before move
      #time.sleep(10) #needs time to move home
      #velocity.move1(individuals)
    

def run_real(tutorial,pop,loops,filestring,writer,velocity):
  print "Running Real"
  for individuals in pop.current_ind_instances:

    file_str = "Results/Real/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))
    
    print "Run REAL Should be at home position, all joints Zero, ready for Individual", individuals.indnum,"Gen",individuals.gen
    tutorial.go_to_joint_state(0.0,0.0,0.0,0.0,0.0,0.0) # note Rads each joint 
    time.sleep(10)
    print "REAL Should be at home position, all joints Zero, ready for Individual", individuals.indnum
    if individuals.real_run == False: # this line ensures we only do the new ones
      file_str = "Results/Real/ind%sgen%s.csv" % ((individuals.indnum), (pop.gencount))

      filestring.publish(file_str)
      pathlist = individuals.waypoints#[0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
    ## The line was removed because of a fault in the cartesian_plan software
    #cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist,individuals,writer)
    test = True
    inst_str = "start"
    writer.publish(inst_str) # Starts the Listener
    time.sleep(1) # ensure we got a start
    if individuals.sim_success == True and individuals.execute_success == False:
      inst_str = "start"
      writer.publish(inst_str)
      for i in range(0,(len(individuals.xpos))):
        individuals.real_success = True
      #if test == True:
        tutorial.execute_plan(individuals.plan_1[i])
        individuals.execute_success = True
        #return_tf = tutorial.go_to_pose_goal(1.0,individuals.xpos[i],individuals.ypos[i],individuals.zpos[i],individuals.vmax[i],writer,individuals,i)
      #if test == True:
      #  test = return_tf
      #if test == False:
      #  individuals.real_success = False
      #  individuals.euclid = 0
      #  print "This Real individual ",individuals.indnum," has a bad waypoint given a Eucidean of Zero"
      #  individuals.real_run = True
      #else:
      #  print "This Real individual", individuals.indnum," with euclid",individuals.euclid," was already assessed... skipping to next"
    inst_str = "stop"
    writer.publish(inst_str) # Starts the Listener
    time.sleep(1)
    inst_str = "stop"
    writer.publish(inst_str) # Starts the Listener

if __name__ == '__main__':
  main()