#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, SRI International
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of SRI International nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Acorn Pooley, Mike Lautman

## BEGIN_SUB_TUTORIAL imports
##
## To use the Python MoveIt interfaces, we will import the `moveit_commander`_ namespace.
## This namespace provides us with a `MoveGroupCommander`_ class, a `PlanningSceneInterface`_ class,
## and a `RobotCommander`_ class. More on these below. We also import `rospy`_ and some messages that we will use:
##

import sys
import copy
import rospy
import numpy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import itertools as it
import csv
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from sensor_msgs.msg import JointState
from moveit_msgs.msg import RobotTrajectory, Grasp, PlaceLocation, Constraints, RobotState
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
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

    ## BEGIN_SUB_TUTORIAL setup
    ##
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

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to a planning group (group of joints).  In this tutorial the group is the primary
    ## arm joints in the Panda robot, so we set the group's name to "panda_arm".
    ## If you are using a different robot, change this value to the name of your robot
    ## arm planning group.
    ## This interface can be used to plan and execute motions:
    group_name = "chain1"
    group_name2= "chain2"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    move_group2= moveit_commander.MoveGroupCommander(group_name2)

    ## Create a `DisplayTrajectory`_ ROS publisher which is used to display
    ## trajectories in Rviz:
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    ## END_SUB_TUTORIAL

    ## BEGIN_SUB_TUTORIAL basic_info
    ##
    ## Getting Basic Information
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^
    # We can get the name of the reference frame for this robot:
    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame

    # We can also print the name of the end-effector link for this group:
    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link

    # We can get a list of all the groups in the robot:
    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()

    # Sometimes for debugging it is useful to print the entire state of the
    # robot:
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""

    ##chain 2
    planning_frame2 = move_group2.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame2

    # We can also print the name of the end-effector link for this group:
    eef_link2 = move_group2.get_end_effector_link()
    print "============ End effector link: %s" % eef_link2
    ## END_SUB_TUTORIAL

    # Misc variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    self.move_group2 = move_group2
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.planning_frame2 = planning_frame2
    self.eef_link = eef_link
    self.eef_link2 = eef_link2
    self.group_names = group_names

  def go_to_joint_state(self,joints):
    # Copy class variables to local variables to make the web tutorials more clear.
    # In practice, you should use the class variables directly unless you have a good
    # reason not to.
    move_group = self.move_group

    ## BEGIN_SUB_TUTORIAL plan_to_joint_state
    ##
    ## Planning to a Joint Goal
    ## ^^^^^^^^^^^^^^^^^^^^^^^^
    # We can get the joint values from the group and adjust some of the values:
    joint_goal = move_group.get_current_joint_values()

    joint_goal[0] = joints[0]
    joint_goal[1] = joints[1]
    joint_goal[2] = joints[2]
    joint_goal[3] = joints[3]
    joint_goal[4] = joints[4]

    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    #print type(joint_goal)

    check = move_group.go(joint_goal, wait=True)
    print check

    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()

    # For testing:
    current_joints = move_group.get_current_joint_values()
    current_pose = self.move_group.get_current_pose().pose
    print current_pose

    return all_close(joint_goal, current_joints, 0.01)

  def go_to_pose_goal(self,x,y,z,ox,oy,oz,w):
      # Copy class variables to local variables to make the web tutorials more clear.
      # In practice, you should use the class variables directly unless you have a good
      # reason not to.
      move_group = self.move_group
      move_group2 = self.move_group2

      pose_goal = geometry_msgs.msg.Pose()
      pose_goal.position.x = x
      pose_goal.position.y = y
      pose_goal.position.z = z
      pose_goal.orientation.x = ox
      pose_goal.orientation.y = oy
      pose_goal.orientation.z = oz
      pose_goal.orientation.w = w

      move_group.set_pose_target(pose_goal)
      move_group2.set_pose_target(pose_goal)

      ## Now, we call the planner to compute the plan and execute it.

      plan = move_group.go(wait=True)
      if plan==False:
          finaltry=0
          while finaltry<3:
              finaltry=finaltry+1
              plan = move_group.go(wait=True)
      plan2 = move_group2.go(wait=True)
      if plan2==False:
          finaltry=0
          while finaltry<3:
              finaltry=finaltry+1
              plan2 = move_group2.go(wait=True)

      print(plan2)
      # Calling `stop()` ensures that there is no residual movement
      move_group.stop()

      move_group2.stop()
      # It is always good to clear your targets after planning with poses.
      # Note: there is no equivalent function for clear_joint_value_targets()
      #move_group.clear_pose_targets()
      move_group2.clear_pose_targets()

      ## END_SUB_TUTORIAL

      # For testing:
      # Note that since this section of code will not be included in the tutorials
      # we use the class variable rather than the copied state variable
      current_pose = self.move_group.get_current_pose().pose
      current_pose2 = self.move_group2.get_current_pose().pose


      #print "============ Printing robot state"
      #print current_pose
      #print current_pose2
      #print ""
      return all_close(pose_goal, current_pose2, 0.01)

  # move only the bottom part after having moved the top part from the visual
  def go_to_work_goal(self):
      move_group = self.move_group
      move_group2 = self.move_group2

      current_pose = self.move_group.get_current_pose().pose

      pose_goal = geometry_msgs.msg.Pose()
      pose_goal.position.x = current_pose.position.x
      pose_goal.position.y = current_pose.position.y
      pose_goal.position.z = current_pose.position.z
      pose_goal.orientation.x = current_pose.orientation.x
      pose_goal.orientation.y = current_pose.orientation.y
      pose_goal.orientation.z = current_pose.orientation.z
      pose_goal.orientation.w = current_pose.orientation.w

      move_group2.set_pose_target(pose_goal)

      ## Now, we call the planner to compute the plan and execute it.
      plan2 = move_group2.go(wait=True)

      print(plan2)
      # Calling `stop()` ensures that there is no residual movement
      move_group2.stop()
      # It is always good to clear your targets after planning with poses.
      # Note: there is no equivalent function for clear_joint_value_targets()
      #move_group.clear_pose_targets()

      move_group2.clear_pose_targets()

      #print "============ Printing robot state"
      #print current_pose
      #print current_pose2
      #print ""
      return all_close(pose_goal, current_pose, 0.01)

  def go_to_position_goal(self,x,y,z):
     # Copy class variables to local variables to make the web tutorials more clear.
     # In practice, you should use the class variables directly unless you have a good
     # reason not to.
     pose_goal = geometry_msgs.msg.Pose()
     move_group = self.move_group
     #move_group2 = self.move_group2
     eef_link = move_group.get_end_effector_link()

     target_position=[x,y,z]
     #move_group.set_position_target()
     #positions tried :
     #[-0.000167733,0.000365719,0.10125]
     #[-0.002,0.03,0.088]
     #[0.01,0,0.1]
     move_group.set_position_target([x,y,z],eef_link)

     ## Now, we call the planner to compute the plan and execute it.
     plan = move_group.go(wait=True)
     if plan==False:
         finaltry=0
         while finaltry<3:
             finaltry=finaltry+1
             plan = move_group.go(wait=True)
     # Calling `stop()` ensures that there is no residual movement
     move_group.stop()
     move_group.clear_pose_targets()
     ## END_SUB_TUTORIAL

     # For testing:
     # Note that since this section of code will not be included in the tutorials
     # we use the class variable rather than the copied state variable
     current_pose = self.move_group.get_current_pose().pose
     return all_close(pose_goal, current_pose, 0.01)

  def workspace_orientation():
      #Workspace test by hand
      ###############################3
      #90/0 degrees middle
      #tutorial.go_to_pose_goal(0,0,0.1,0.708,0.705,0.0017,0.0017)
      #tutorial.go_to_pose_goal(0.01,0.02,0.1,0.708,0.705,0.0017,0.0017)
      #tutorial.go_to_pose_goal(0.044,0,0.1,0.708,0.705,0.0017,0.0017)
      #60
      #tutorial.go_to_pose_goal(0,0,0.1,0.61,0.61,-0.35,-0.035)
      #50
      #tutorial.go_to_pose_goal(0,0,0.1,0.64,0.64,-0.29,-0.29)
      #40
      #tutorial.go_to_pose_goal(0,0,0.1,0.66,0.66,-0.24,-0.24)
      #30
      #tutorial.go_to_pose_goal(0,0,0.097,0.685,0.681,-0.1801,-0.1811)
      #tutorial.go_to_pose_goal(0,0,0.1,0.685,0.681,-0.1801,-0.1811)
      #20
      #tutorial.go_to_pose_goal(-0.0002,0.00001,0.098,0.6982,0.6947,-0.121,-0.122)
      #tutorial.go_to_pose_goal(0,0,0.1,0.6982,0.6947,-0.121,-0.122)
      ##the code I added
      #print "============ Press `Enter` for current_ee ..."
      #raw_input()
      #tutorial.current_ee()

      ##the actual targets
       #target 2 nope
      tutorial.go_to_pose_goal(-0.020188, -0.0003265817, 0.997409, 0.0374078, 0.998231, -0.0461802, -0.00172873)


      #target 1 Works
      tutorial.go_to_pose_goal(0, -0.000342553, 0.0995654, 0.0374116, 0.998231, -0.0461742, -0.00172868)
      #target 2 done
      tutorial.go_to_pose_goal(-0.0197256,-0.000393056,0.100385,0.704998,0.702201,-0.0701882,-0.0704678)
      #target 3 done
      tutorial.go_to_pose_goal(-0.0201047,0.0401313,0.0997435, 0.793591,0.562272, -0.134422, -0.189724)
      #target 4 done
      tutorial.go_to_pose_goal(-0.0396635, 0.024835, 0.100057, 0.697148, 0.70021, -0.109075 , -0.108598) ###this one
      #target 4 nope
      tutorial.go_to_pose_goal(-0.0396635, 0.024835, 0.100057, 0.697148, 0.70021, -0.109075 , -0.108598) ###this one
      #target 5 done
      tutorial.go_to_pose_goal( 0.0249996, -0.0147974, 0.0996652, 0.664474, 0.747232, -0.00814132, -0.00723935)
      #target 5 nope
      tutorial.go_to_pose_goal( 0.0249996, -0.0147974, 0.0996652, 0.664474, 0.747232, -0.00814132, -0.00723935)
      #target 6 done
      tutorial.go_to_pose_goal( 0.024568, 0.024365, 0.100188, 0.0403925, 0.989238, -0.140511, -0.00573549)
      #target 7 done
      tutorial.go_to_pose_goal( 0.024777, -0.0552243, 0.100139, 0.0391906, 0.961136, -0.273054, -0.011132)
      #target 8 done
      tutorial.go_to_pose_goal(-0.0349722, -0.053412, 0.100465, 0.0349256, 0.932642, -0.358858, -0.0134366)
      #target 9 done
      tutorial.go_to_pose_goal(-0.0404218, -0.0303118, 0.0998911, 0.283953, 0.930061, -0.222988, -0.0680778)
      #target 10 done
      tutorial.go_to_pose_goal(-0.0455302, -0.0101575, 0.0995743, 0.332935, 0.904698, -0.249491, -0.091813)
      #target 11 done
      tutorial.go_to_pose_goal(-0.000203871, -0.0444923, 0.0996843, 0.332922, 0.90472, -0.249439, -0.0917881)
      #target 12 done
      tutorial.go_to_pose_goal(0.0450683, -0, 0.0997801, 0.40938, 0.912233, 0.0141125, 0.00633455)
      #target 13 done
      tutorial.go_to_pose_goal(0.0448726, -0.0301161, 0.100269, 0.708773, 0.704005, 0.031659, 0.03187345)
      #target 16 done here
      tutorial.go_to_pose_goal(0.0302282, 0.0449977, 0.0999986, 0.0365429, 0.97552, 0.216701, 0.00811948)


      return True


def main():
  try:
    print ""
    print "----------------------------------------------------------"
    print "Welcome to the MoveIt MoveGroup Python Interface Tutorial"
    print "----------------------------------------------------------"
    print "Press Ctrl-D to exit at any time"
    print ""
    print "============ Press `Enter` to begin the tutorial by setting up the moveit_commander ..."
    raw_input()
    tutorial = MoveGroupPythonIntefaceTutorial()


    #print "============ Press `Enter` to execute a movement using a joint goal for simulaton ..."
    #raw_input()

    #tutorial.go_to_pose_goal(0.01,0.02,0.1,0.708,0.705,0.0017,0.0017)
    #tutorial.go_to_work_goal()

    #print "============ Press `Enter` to execute a movement using a joint goal for simulaton ..."
    #raw_input()
    #tutorial.go_to_pose_goal(0,0,0.1,0.708,0.705,0.0017,0.0017)



    #print "============ Press `Enter` to execute a movement using a joint goal for simulaton ..."
    #raw_input()
    #tutorial.go_to_pose_goal(0.044,0,0.1,0.708,0.705,0.0017,0.0017)
    #tutorial.go_to_pose_goal(0.019,0.02169,0.1,0.353446,0.935451,0.00259,0.000982)
    #tutorial.go_to_position_goal(0.0302282, 0.0449977, 0.0999986)
    #tutorial.go_to_position_goal(-0.0542632, 0.000125413, 0.100796)

    #print "============ trying it with orientation ..."
    #tutorial.go_to_pose_goal(-0.0542632, 0.000125413, 0.100796,0.63885, 0.727072, -0.188917, -0.165993)

    #print "============ Press `Enter` for bottom to follow ..."
    #raw_input()
    #tutorial.go_to_work_goal()

    #print "============ Press `Enter` for bottom to follow ..."
    #raw_input()
    #tutorial.go_to_work_goal()

    #print "============ Press `Enter` for bottom to follow ..."
    #raw_input()
    #tutorial.go_to_work_goal()

    print "============ Press `Enter` to execute a movement using a joint goal for simulaton ..."
    raw_input()
    ##the actual targets
    tutorial.go_to_pose_goal(0.0302282, 0.0449977, 0.0999986, 0.0365429, 0.97552, 0.216701, 0.00811948)



    #print "============ Press `Enter` to execute a movement from the saved achievable joints ..."
    #raw_input()

    #for i in range(0,60,10):
        #print(posData[i][0],posData[i][1],posData[i][2])
        #print(orData[i][0],orData[i][1],orData[i][2],orData[i][3])
        #tutorial.go_to_pose_goal(round(posData[i][0],2),round(posData[i][0],2),round(posData[i][0],2),orData[i][0],orData[i][1],orData[i][2],orData[i][3])
        ##tutorial.go_to_pose_goal(posData[i][0],posData[i][1],posData[i][2],orData[i][0],orData[i][1],orData[i][2],orData[i][3])
        ##print i



    print "============ Python tutorial demo complete!"
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()

## BEGIN_TUTORIAL
## .. _moveit_commander:
##    http://docs.ros.org/melodic/api/moveit_commander/html/namespacemoveit__commander.html
##
## .. _MoveGroupCommander:
##    http://docs.ros.org/melodic/api/moveit_commander/html/classmoveit__commander_1_1move__group_1_1MoveGroupCommander.html
##
## .. _RobotCommander:
##    http://docs.ros.org/melodic/api/moveit_commander/html/classmoveit__commander_1_1robot_1_1RobotCommander.html
##
## .. _PlanningSceneInterface:
##    http://docs.ros.org/melodic/api/moveit_commander/html/classmoveit__commander_1_1planning__scene__interface_1_1PlanningSceneInterface.html
##
## .. _DisplayTrajectory:
##    http://docs.ros.org/melodic/api/moveit_msgs/html/msg/DisplayTrajectory.html
##
## .. _RobotTrajectory:
##    http://docs.ros.org/melodic/api/moveit_msgs/html/msg/RobotTrajectory.html
##
## .. _rospy:
##    http://docs.ros.org/melodic/api/rospy/html/
## CALL_SUB_TUTORIAL imports
## CALL_SUB_TUTORIAL setup
## CALL_SUB_TUTORIAL basic_info
## CALL_SUB_TUTORIAL plan_to_joint_state
## CALL_SUB_TUTORIAL plan_to_pose
## CALL_SUB_TUTORIAL plan_cartesian_path
## CALL_SUB_TUTORIAL display_trajectory
## CALL_SUB_TUTORIAL execute_plan
## CALL_SUB_TUTORIAL add_box
## CALL_SUB_TUTORIAL wait_for_scene_update
## CALL_SUB_TUTORIAL attach_object
## CALL_SUB_TUTORIAL detach_object
## CALL_SUB_TUTORIAL remove_object
## END_TUTORIAL
