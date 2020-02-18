#!/usr/bin/env python
## To use the Python MoveIt interfaces, we will import the `moveit_commander`_ namespace.
## This namespace provides us with a `MoveGroupCommander`_ class, a `PlanningSceneInterface`_ class,
## and a `RobotCommander`_ class. More on these below. We also import `rospy`_ and some messages that we will use:
##

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
# from compas.datastructures import Mesh
# import compas_fab
# from compas_fab.backends import RosClient
# from compas_fab.robots import CollisionMesh
# from compas_fab.robots import PlanningScene
# from compas_fab.robots.ur5 import Robot
# from compas.geometry import Box


## END_SUB_TUTORIAL


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
    print "Davids Trials of Code for UR10 Arm Control"

     ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    
    ## Instantiate a `RobotCommander`_ object. Provides information such as the robot's
    ## kinematic model and the robot's current joint states
    robot = moveit_commander.RobotCommander()
    ## Instantiate a `PlanningSceneInterface`_ object.  This provides a remote interface
    ## for getting, setting, and updating the robot's internal understanding of the
    ## surrounding world:
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "manipulator"#"ur10" #was panda_arm
    move_group = moveit_commander.MoveGroupCommander(group_name)

    ## Create a `DisplayTrajectory`_ ROS publisher which is used to display
    ## trajectories in Rviz:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    planning_frame = move_group.get_planning_frame()
    print "DW============ Planning frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = move_group.get_end_effector_link()
    print "DW============ End effector link: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "DW============ Available Planning Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "DW============ Printing robot state"
    print robot.get_current_state()
    print ""
    ## END_SUB_TUTORIAL

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names


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
    return all_close(joint_goal, current_joints, 0.01)


  def go_to_pose_goal(self,W,X,Y,Z):
    # Copy class variables to local variables to make the web tutorials more clear.
    move_group = self.move_group

    print "Planning to a Pose Goal X ", X," Y ",Y," Z ",Z
    pose_goal = geometry_msgs.msg.Pose()
    # Note these are in Quarternians 
    pose_goal.orientation.w = W#1.0
    pose_goal.position.x = X#0.4
    pose_goal.position.y = Y#0.1
    pose_goal.position.z = Z#0.4 Confirmed as UP
    move_group.set_pose_target(pose_goal)
    ## Now, we call the planner to compute the plan and execute it.
    plan = move_group.go(wait=True)
    # Calling `stop()` ensures that there is no residual movement
    move_group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    move_group.clear_pose_targets()
    current_pose = self.move_group.get_current_pose().pose
    return all_close(pose_goal, current_pose, 0.01)


  def plan_cartesian_path(self,coords,ind,odom,scale=1):
    #Can access the individual that we are acting upon below
    #ind.printIndnum()
    print "Im in Planning"
    print "Note I need x y z and velocity "
    listcoords = [] #ensure empty
    listcoords = copy.deepcopy(coords)# can be any length in x y z x y z format
    #print "where are we going"
    #print listcoords
    move_group = self.move_group
    #move_group.stop()
    move_group.clear_pose_targets() # ensure no pose targets

    waypoints = [] # ensure empty 
    wpose = move_group.get_current_pose().pose
    move_group.allow_looking(True)
    move_group.allow_replanning(True)
    move_group.set_planning_time(300)
    move_group.set_num_planning_attempts(300)
    move_group.set_goal_position_tolerance(0.01)
    move_group.set_goal_orientation_tolerance(0.5)
    move_group.set_goal_tolerance(0.5)
    move_group.set_goal_joint_tolerance(0.5)
    vel = []


    while listcoords > 0:
      #print listcoords[0]
      
      if len(listcoords) != 0:

        
        #print "I had a list"
        #print listcoords
        wpose.position.x = listcoords[0]  # First move up (z)
        listcoords.pop(0)
        #print listcoords
        wpose.position.y = listcoords[0]  # First move up (z)
        listcoords.pop(0)
        #print listcoords
        wpose.position.z = listcoords[0]  # and sideways (y)
        listcoords.pop(0)
        vel.append(copy.deepcopy(listcoords[0]))
        listcoords.pop(0)
        #print listcoords
        waypoints.append(copy.deepcopy(wpose))
      else:
        print "Either at end of list... or out of scope"
        break
    #print "Way points"
    #print waypoints
    print "planning for individual", ind.indnum
    (plan, fraction) = move_group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step # Dear David, leave this alone
                                       0.0,   # jump_threshold
                                       avoid_collisions = True,
                                       path_constraints = None )         

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    #rospy.sleep(1)
    #print "Done planning if -1 is error PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
    #print plan
    time.sleep(30)
    #print "Display"
    #robot = self.robot
    #display_trajectory_publisher = self.display_trajectory_publisher
    #display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    #display_trajectory.trajectory_start = robot.get_current_state()
    #display_trajectory.trajectory.append(plan)
    #move_group.display_trajectory(plan)
    #print "Fin display"
    #time.sleep(20) # This allows time to display 
    #print "Start Execute"
    #move_group = self.move_group
    #print odom.is_alive()
    if(odom.is_alive() == False):
      #print "here"
      odom.start()
      #time.sleep(1)
    #time.sleep(1)
    #print odom.is_alive()
    if(odom.is_alive() == True):
      #print "I started"
      odom.start_record()
      #time.sleep(1)
    time.sleep(2) # give other process time to start
    move_group.execute(plan, wait=True)
    #linked = move_group.get_current_pose
    #print "linked"
    #print linked
    #raw_input()
    
    odom.stop_record()
    time.sleep(10) # this allows time to execute 
   
    print "Finish Execute Stopped Recording "
    #print "Ive executed the plan"
    #move_group.clear_pose_target()
    #move_group.clear_pose_targets()
    current_pose = self.move_group.get_current_pose().pose
    
    #tutorial.display_trajectory(cartesian_plan)  
    #tutorial.execute_plan(cartesian_plan, wait=True)
    #print plan
    #print fraction
    ind.euclid = odom.evaluate()
    print "Individual number",ind.indnum," has a euclidean of ",ind.euclid
    time.sleep(1)
    #odom.large_x = 100
    return plan, fraction



  def display_trajectory(self, plan):
    print "Im displaying a trajectory " 
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.

    robot = self.robot
    display_trajectory_publisher = self.display_trajectory_publisher
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan)
    # Publish
    display_trajectory_publisher.publish(display_trajectory)
    print "finishing a trajectory "
    rospy.sleep(5)


  def execute_plan(self, plan):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    print "Im executing a plan EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
    #print plan
    move_group = self.move_group
    move_group.execute(plan, wait=True)
    print "Ive executed the plan"
    #move_group.clear_pose_targets()
    #current_pose = self.move_group.get_current_pose().pose
    print "I have cleared old targets and updated poses"
    rospy.sleep(5)


  def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    box_name = self.box_name
    scene = self.scene

    start = rospy.get_time()
    seconds = rospy.get_time()
    while (seconds - start < timeout) and not rospy.is_shutdown():
      # Test if the box is in attached objects
      attached_objects = scene.get_attached_objects([box_name])
      is_attached = len(attached_objects.keys()) > 0

      # Test if the box is in the scene.
      # Note that attaching the box will remove it from known_objects
      is_known = box_name in scene.get_known_object_names()

      # Test if we are in the expected state
      if (box_is_attached == is_attached) and (box_is_known == is_known):
        return True

      # Sleep so that we give other threads time on the processor
      rospy.sleep(0.1)
      seconds = rospy.get_time()

    # If we exited the while loop without returning then we timed out
    return False
 
  def add_box(self, timeout=10):
      box_pose = geometry_msgs.msg.PoseStamped()
      box_pose.header.frame_id = "base"
      box_pose.pose.orientation.w = 1.0
      box_pose.pose.position.x = 0.0 # slightly above the end effector
      box_pose.pose.position.y = 0.0 # slightly above the end effector
      box_pose.pose.position.z = 0.0 # slightly above the end effector
      box_name = "box"
      time.sleep(2) # this is required to give the sim time to
      self.scene.add_box(box_name, box_pose, size=(10, 10, 0.01))
      #self.box_name=box_name
      time.sleep(2) # this is required to give the sim time to upload 
        #table = False
        #table = self.wait_for_state_update(box_is_known=True, timeout=timeout)
        #while table == False: # this loop was to ensure the table is present Might take out later
        #  table = (self.wait_for_state_update(box_is_known=True, timeout=timeout))
        #  print "no table yet"


# def main():
  
#   print "Python has started"
#   tutorial = MoveGroupPythonIntefaceTutorial()
#   print "adding a table for collisions"
#   tutorial.add_box()
#   print "Success adding table "
#   time.sleep(1)

#   print "============ Press `Enter` to execute joint state goal ..."
#   raw_input()
#   tutorial.go_to_joint_state(0.0,-0.5,0.0,0.0,0.0,0.0) # note Rads each joint 
#   #print "============ Press `Enter` to execute a movement using a pose goal ..."
  
#   #raw_input()
#   #tutorial.go_to_pose_goal(1.0,0.2,0.1,0.4) #W X Y Z
#     #xx = 0.1
#     #yy = 0.1
#     #zz = 0.1
#   loops = 0
#   while (1):
#       #random.seed(5)
#       #xx = xx+0.1
#       #y = yy+0.1
#       #zz = zz+0.1
#     print loops
#     loops = loops + 1
#     print "New Path entered"     
#     print "Can I Home? waiting on Raw Input"
#     raw_input()
#     print "Should be at home position"
#     tutorial.go_to_joint_state(0.0,-1.57,0.0,0.0,0.0,0.0) 
#     rospy.sleep(5)

#     pathlist = [0.1,0.5,0.3,0.1,0.5,0.8,0.1,0.5,1.0,0.1,0.5,1.1]
#     cartesian_plan, fraction = tutorial.plan_cartesian_path(pathlist)
#     print "waiting on Raw Input"
#     raw_input()

#   print "============ Exiting the Loop!"

# if __name__ == '__main__':
#   main()




#  def attach_box(self, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
#    box_name = self.box_name
#    robot = self.robot
#    scene = self.scene
#    eef_link = self.eef_link
#    group_names = self.group_names

    ## BEGIN_SUB_TUTORIAL attach_object
    ##
    ## Attaching Objects to the Robot
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ## Next, we will attach the box to the Panda wrist. Manipulating objects requires the
    ## robot be able to touch them without the planning scene reporting the contact as a
    ## collision. By adding link names to the ``touch_links`` array, we are telling the
    ## planning scene to ignore collisions between those links and the box. For the Panda
    ## robot, we set ``grasping_group = 'hand'``. If you are using a different robot,
    ## you should change this value to the name of your end effector group name.
#    grasping_group = 'hand'
#    touch_links = robot.get_link_names(group=grasping_group)
#    scene.attach_box(eef_link, box_name, touch_links=touch_links)
    ## END_SUB_TUTORIAL

    # We wait for the planning scene to update.
#    return self.wait_for_state_update(box_is_attached=True, box_is_known=False, #timeout=timeout)

### NOTE BELOW NOT WORKING DUE TO PLANNING CONFIG FILE 
#  def detach_box(self, timeout=4):
#    # Copy class variables to local variables to make the web tutorials more clear.
#    # In practice, you should use the class variables directly unless you have a good
#    # reason not to.
#    box_name = self.box_name
#    scene = self.scene
#    eef_link = self.eef_link

    ## BEGIN_SUB_TUTORIAL detach_object
    ##
    ## Detaching Objects from the Robot
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ## We can also detach and remove the object from the planning scene:
#    scene.remove_attached_object(eef_link, name=box_name)
    ## END_SUB_TUTORIAL

    # We wait for the planning scene to update.
#    return self.wait_for_state_update(box_is_known=True, box_is_attached=False, #timeout=timeout)


#  def remove_box(self, timeout=4):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
#    box_name = self.box_name
#    scene = self.scene

    ## BEGIN_SUB_TUTORIAL remove_object
    ##
    ## Removing Objects from the Planning Scene
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ## We can remove the box from the world.
#    scene.remove_world_object(box_name)

    ## **Note:** The object must be detached before we can remove it from the world
    ## END_SUB_TUTORIAL

    # We wait for the planning scene to update.
#    return self.wait_for_state_update(box_is_attached=False, box_is_known=False, #timeout=timeout)
