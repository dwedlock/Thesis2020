#!/usr/bin/env python


import roslib; roslib.load_manifest('ur_driver')
import actionlib
from control_msgs.msg import *
from trajectory_msgs.msg import *
import rospy
import time
import copy
#rom gazebo_ros

class VelocityControl(object):
    def __init__(self):

        self.JOINT_NAMES = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                    'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        
        
        self.Q1 = [0.0,0.0,-1.1,0,0,0] #assumed X Y -Z R P Y
        self.Q2 = [0.0,0.0,-1.2,0,0,0]
        self.Q3 = [0.0,0.0,-1.3,0,0,0]

        self.client = None
        #global client
        try:
            #rospy.init_node("test_move", anonymous=True, disable_signals=True)
            self.client = actionlib.SimpleActionClient('arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
            print "Waiting for server..."
            self.client.wait_for_server()
            print "Connected to server"
            print("Move")
               
        except KeyboardInterrupt:
            print "failure or interupt"
            rospy.signal_shutdown("KeyboardInterrupt")
            raise

    def move1(self,individual):

        g = FollowJointTrajectoryGoal()
        g.trajectory = JointTrajectory()
        g.trajectory.joint_names = self.JOINT_NAMES
        if individual.num_points > 0:
            #self.Q1 = [individual.xpos[0],individual.ypos[0],-(individual.zpos[0]),0,0,0]
            vel = 1.0#individual.vmax[0]
            trial = JointTrajectoryPoint(positions=self.Q1, velocities=[vel*2]*6, time_from_start=rospy.Duration(5.0))
        if individual.num_points > 1:
            #self.Q2 = [individual.xpos[1],individual.ypos[1],-(individual.zpos[1]),0,0,0]
            vel2 = 1.0#individual.vmax[1]
            trial2 = JointTrajectoryPoint(positions=self.Q2, velocities=[vel*2]*6, time_from_start=rospy.Duration(10.0))
        if individual.num_points > 2:
            #self.Q3 = [individual.xpos[2],individual.ypos[2],-(individual.zpos[2]),0,0,0]
            vel3 = 1.0#individual.vmax[2]
            trial3= JointTrajectoryPoint(positions=self.Q3, velocities=[vel*2]*6, time_from_start=rospy.Duration(15.0))

        #trial2 = JointTrajectoryPoint(positions=self.Q2, velocities=[1]*6, time_from_start=rospy.Duration(2.0))
        #trial3 = JointTrajectoryPoint(positions=self.Q3, velocities=[1]*6, time_from_start=rospy.Duration(3.0))
        g.trajectory.points = [
            trial,
            trial2,
            trial3]
        self.client.send_goal(g)
        print "Ive sent the velocity goal"
        time.sleep(10)
        try:
            self.client.wait_for_result()
        except KeyboardInterrupt:
            self.client.cancel_goal()
            raise

    def move_disordered(self):
        order = [4, 2, 3, 1, 5, 0]
        g = FollowJointTrajectoryGoal()
        g.trajectory = JointTrajectory()
        g.trajectory.joint_names = [self.JOINT_NAMES[i] for i in order]
        q1 = [self.Q1[i] for i in order]
        q2 = [self.Q2[i] for i in order]
        q3 = [self.Q3[i] for i in order]
        g.trajectory.points = [
            JointTrajectoryPoint(positions=q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
        self.client.send_goal(g)
        self.client.wait_for_result()
        
    def move_repeated(self):
        g = FollowJointTrajectoryGoal()
        g.trajectory = JointTrajectory()
        g.trajectory.joint_names = self.JOINT_NAMES
        
        d = 2.0
        g.trajectory.points = []
        for i in range(10):
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=self.Q1, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=self.Q2, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 1
            g.trajectory.points.append(
                JointTrajectoryPoint(positions=self.Q3, velocities=[0]*6, time_from_start=rospy.Duration(d)))
            d += 2
        self.client.send_goal(g)
        try:
            self.client.wait_for_result()
        except KeyboardInterrupt:
            self.client.cancel_goal()
            raise

    def move_interrupt(self):
        g = FollowJointTrajectoryGoal()
        g.trajectory = JointTrajectory()
        g.trajectory.joint_names = self.JOINT_NAMES
        g.trajectory.points = [
            JointTrajectoryPoint(positions=Q1, velocities=[0]*6, time_from_start=rospy.Duration(2.0)),
            JointTrajectoryPoint(positions=Q2, velocities=[0]*6, time_from_start=rospy.Duration(3.0)),
            JointTrajectoryPoint(positions=Q3, velocities=[0]*6, time_from_start=rospy.Duration(4.0))]
        
        self.client.send_goal(g)
        time.sleep(2.0)
        print "Interrupting"
        self.client.send_goal(g)
        try:
            self.client.wait_for_result()
        except KeyboardInterrupt:
            self.client.cancel_goal()
            raise

