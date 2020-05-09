#!/usr/bin/env python

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
from multiprocessing import Process
import os


def all_close(goal, actual, tolerance):
  """
  Convenience method for testing if a list of values are within a tolerance of their counterparts in another list
  @param: goal       A list of floats, a Pose or a PoseStamped
  @param: actual     A list of floats, a Pose or a PoseStamped
  @param: tolerance  A float
  @returns: bool
  """
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True


class MoveGroupPythonIntefaceTutorial(object):
  """MoveGroupPythonIntefaceTutorial"""
  def __init__(self):
    super(MoveGroupPythonIntefaceTutorial, self).__init__()
    print "UR10 Arm Control based upon UR10 Joint limited Moveit Controller"
     ## initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"#"ur10" #was panda_arm This comes from universal_robot/ur10_moveit_config/config
    move_group = moveit_commander.MoveGroupCommander(group_name)
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)
    #/move_group/trajectory_execution/allowed_start_tolerance

    planning_frame = move_group.get_planning_frame()
    eef_link = move_group.get_end_effector_link()
    group_names = robot.get_group_names()
    #Add the table to generate collisions
    box_pose = geometry_msgs.msg.PoseStamped()
    box_pose.header.frame_id = robot.get_planning_frame()
    box_pose.pose.orientation.w = 1.0
    box_pose.pose.position.x = 0.0 # slightly above the end effector
    box_pose.pose.position.y = 0.0 # slightly above the end effector
    box_pose.pose.position.z = 0.01 # slightly above the end effector
    box_name = "box"
    time.sleep(2) # this is required to give the sim time to
    scene.add_box(box_name, box_pose, size=(10, 10, 0.01))
    time.sleep(2) # this is required to give the sim time to upload 
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names
    self.prev_x = 0
    self.prev_y = 0
    self.prev_z = 0
    

  def go_to_joint_state(self,zero,one,two,three,four,five):
    # NOTE Danger This joint state controller does no planning and will operate to collision
    move_group = self.move_group
    joint_goal = move_group.get_current_joint_values()
    joint_goal[0] = zero #radians so 1 rad = 57.3 or 90deg = 1.57rads
    joint_goal[1] = one#1.57#-pi/4 
    joint_goal[2] = two#1.57
    joint_goal[3] = three#1.57#-pi/2
    joint_goal[4] = four#1.57
    joint_goal[5] = five#1.57#pi/3
    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.go(joint_goal, wait=True)
    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()
    # For testing:
    current_joints = move_group.get_current_joint_values()
    #print "Robot Currently at"
    #print self.robot.get_current_state()
    move_group.allow_looking(True)
    move_group.allow_replanning(True)
    move_group.set_planning_time(90)
    move_group.set_num_planning_attempts(2050) #Gets ignored by RVIZ
    move_group.set_goal_position_tolerance(0.2)
    move_group.set_goal_orientation_tolerance(0.2)
    move_group.set_goal_tolerance(0.5)
    move_group.set_goal_joint_tolerance(0.5)
    return all_close(joint_goal, current_joints, 0.03)

  def go_to_pose_goal(self,W,X,Y,Z,V,writer,ind,iteration):
    # Copy class variables to local variables to make the web tutorials more clear.
    move_group = self.move_group
    move_group.set_max_velocity_scaling_factor(V)
    move_group.set_max_acceleration_scaling_factor(0.1)
    #print "Planning to a Pose Goal X ", X," Y ",Y," Z ",Z
    pose_goal = geometry_msgs.msg.Pose()
    # Note these are in Quarternians 
    #if (interation == 0):
    move_group.stop()
    current_pose = self.move_group.get_current_pose().pose
    move_group.set_start_state_to_current_state()
    #else:
    move_group.clear_pose_targets()

    move_group.set_planner_id = iteration

    pose_goal.orientation.w = W#1.0
    pose_goal.position.x = X#0.4
    pose_goal.position.y = Y#0.1
    pose_goal.position.z = Z#0.4 Confirmed as UP
    move_group.set_pose_target(pose_goal)
    ## Now, we call the planner to compute the plan and execute it.
    #inst_str = "start"
    #writer.publish(inst_str) # Starts the Listener
    #writer.publish(inst_str)
    #time.sleep(0.5)
    #print "We started to move", X, Y, Z
    #0.1 0.1 0.5 0.5 0.01

    # below errros fixed by adding allowed start tolerance to trajectory execution launch 
    #[ERROR] [1587709928.889767583, 944.830000000]: 
    #Invalid Trajectory: start point deviates from current robot state more than 0.01
    #joint 'elbow_joint': expected: 0.196037, current: -0.411416

    #[ERROR] [1587710219.463240473, 1229.669000000]: 
    #Invalid Trajectory: start point deviates from current robot state more than 0.01
    #joint 'elbow_joint': expected: 0.130583, current: 0.151856

    #[ERROR] [1587710391.002413623, 1399.749000000]: 
    #Invalid Trajectory: start point deviates from current robot state more than 0.01
    #joint 'elbow_joint': expected: 0.0518671, current: -0.169169


    #[ERROR] [1587710762.060893651, 1768.368000000]: 
    #Invalid Trajectory: start point deviates from current robot state more than 0.01
    #joint 'elbow_joint': expected: -0.0116591, current: 0.083973


    
    planner = move_group.plan()
    #print "Planner"
    #print planner
    #print planner
    ind.plan_1.append(planner)
    #move_group.plan = ind.plan_1 # THis line will be used later
    print "Move to next point for the plan"
    plan = move_group.go(wait=True)
    #print plan_1
    #inst_str = "stop"
    #writer.publish(inst_str) #stops the listener 
    #time.sleep(0.1)
    #writer.publish(inst_str)
    #print "We finished a move", plan
    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    move_group.clear_pose_targets()
    current_pose = self.move_group.get_current_pose().pose
    #plan = True
    #all_close(pose_goal, current_pose, 0.01)
    return plan



  def plan_cartesian_path(self,coords,ind,writer,scale=1):
    #Note, while the below code operates there is a random intermitent error that causes the controller to fail
    listcoords = [] #ensure empty
    listcoords = copy.deepcopy(coords)# can be any length in x y z x y z format
    move_group = self.move_group
    #move_group.stop()
    move_group.clear_pose_targets() # ensure no pose targets
    waypoints = [] # ensure empty 
    wpose = move_group.get_current_pose().pose
    move_group.set_max_velocity_scaling_factor(0.1)
    move_group.set_max_acceleration_scaling_factor(0.1)
    move_group.set_start_state_to_current_state()
    vel = []

    while listcoords > 0:
      if len(listcoords) != 0:
        wpose.position.x = listcoords[0]  # First move up (z)
        listcoords.pop(0)
        wpose.position.y = listcoords[0]  # First move up (z)
        listcoords.pop(0)
        wpose.position.z = listcoords[0]  # and sideways (y)
        listcoords.pop(0)
        vel.append(copy.deepcopy(listcoords[0]))
        listcoords.pop(0)
        waypoints.append(copy.deepcopy(wpose))
      else:
        #print "Either at end of list... or out of scope"
        break
    move_group.clear_pose_targets()
    move_group.stop()
    time.sleep(1)
    (plan, fraction) = move_group.compute_cartesian_path(
                                        waypoints,   # waypoints to follow
                                        0.01,        # eef_step # Dear David, leave this alone
                                        0.0,   # jump_threshold
                                        avoid_collisions = True)  
    print "exited planner started timer purple movement should have stopped"       
    time.sleep(30)
    print "timer finished, planner should finihsed, fraction is ", fraction
    time.sleep(2) # give other process time to start
    inst_str = "start"
    move_group.stop()
    writer.publish(inst_str) # Starts the Listener
    time.sleep(0.2)# this sleep ensures we pick it up
    writer.publish(inst_str)
    time.sleep(0.2)
    if plan != -1 and fraction > 0.1:
      print "We have a good plan "
      move_group.execute(plan, wait=True)
      ind.success = True 
    if plan == -1 or fraction < 0.1:
      print "Plan failure -1 returned, this was a bad plan"
      ind.sim_run = True
      ind.success = False
    time.sleep(0.2)
    inst_str = "stop"
    writer.publish(inst_str) #stops the listener 
    time.sleep(1)
    writer.publish(inst_str) #stops the listener 
    print "Finish Execute Stopped Recording "
    current_pose = self.move_group.get_current_pose().pose
    time.sleep(1)
    return plan, fraction

  def display_trajectory(self, plan):
    print "Im displaying a trajectory " 
    robot = self.robot
    display_trajectory_publisher = self.display_trajectory_publisher
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    display_trajectory_publisher.publish(display_trajectory)
    print "finishing a trajectory "
    rospy.sleep(5)


  def execute_plan(self, plan):
    #print "Planner"
    #print plan
    #print "Im starting a plan" 
    #self.move_group.clear_pose_targets()
    print "In execute"
    #move_group = self.move_group
    #time.sleep(1)
    #
    #self.move_group.set_start_state_to_current_state() # this generates errors/ 
    state = self.move_group.execute(plan, wait=True)
    #time.sleep(10) # this does not help...

    print "Released from execute"
    #print state
    #print "Ive executed the plan"
    #rospy.sleep(5)


  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    box_name = self.box_name
    scene = self.scene
    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      # Test if the box is in attached objects
      attached_objects = scene.get_attached_objects([box_name])
      is_attached = len(attached_objects.keys()) > 0
      is_known = box_name in scene.get_known_object_names()
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True
      rospy.sleep(0.1)
      seconds = rospy.get_time()
    return False
 
  def add_box(self, timeout=10):
      box_pose = geometry_msgs.msg.PoseStamped()
      box_pose.header.frame_id = robot.get_planning_frame()
      box_pose.pose.orientation.w = 1.0
      box_pose.pose.position.x = 0.0 # slightly above the end effector
      box_pose.pose.position.y = 0.0 # slightly above the end effector
      box_pose.pose.position.z = -0.02 # slightly above the end effector
      box_name = "box"
      time.sleep(2) # this is required to give the sim time to
      self.scene.add_box(box_name, box_pose, size=(10, 10, 0.01))
      time.sleep(2) # this is required to give the sim time to upload 
