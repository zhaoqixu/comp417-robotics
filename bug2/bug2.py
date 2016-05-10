#!/usr/bin/env python

import rospy
import math
import roslib
import random
#import sys
from  tf.transformations import euler_from_quaternion

# The laser scan message
from sensor_msgs.msg import LaserScan
# The velocity command message
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Quaternion

min_wall_distance = 0.9
closeToObst = 0
duration = 0.2
turn_speed = 0.4
movement_speed = 0.15
pos = 0
#set up your start and goal points here
goal_x = 0
goal_y = 0
start_x = 19.96
start_y = 10.92
distance_to_goal = 0
#thresgold to goal and to the line
thresholddist_togoal = 0.5
thresholddist_toline = 0.1
atGoal = False
follow_type = 0 # 0 follows line and 1 follows wall
posx = 0
posy = 0
quat = 0
radians_gtos = 0
angle_toturn = 0 

def laser_callback(scan):
	length = len(scan.ranges)
	midbeam = scan.ranges[length/2]		#middle beam data
	leftmostbeam = scan.ranges[length-1]
	rightmostbeam = scan.ranges[0]
	if (leftmostbeam < min_wall_distance or rightmostbeam < min_wall_distance or midbeam < min_wall_distance):
		global closeToObst
		closeToObst = 1
	elif math.isnan(rightmostbeam):
	 	closeToObst = 2
	elif rightmostbeam > 1.5:
		closeToObst = 3
	else:
		closeToObst = 0

def position_callback(data):
	global follow_type
	global atGoal
	global posx
	global posy
	global quat
	global angle_toturn
	
	tangent = float(start_y-goal_y)/(start_x-goal_x)
	radians_gtos = math.atan(tangent)
	quat = data.pose[2].orientation
	q = [quat.x, quat.y, quat.z, quat.w]
	roll, pitch, yaw = euler_from_quaternion(q)
	#print yaw
	posx = data.pose[2].position.x
	posy = data.pose[2].position.y
	temp_x = start_x - goal_x
	temp_y = start_y - goal_y
	pi = 3.1415926
	# calculate how much angle to turn
	if yaw > 0:
		angle_toturn = pi - yaw + radians_gtos
	else:
		angle_toturn = -pi - yaw + radians_gtos 
	
	#calculate the angle that need to turn, but still have some issues
	coef = float(-goal_y+start_y)/(-goal_x+start_x)
	const = -(float(-goal_y+start_y)/(-goal_x+start_x))*goal_x + goal_y
	est_y = posx*coef+const
	#distance to the goal
	distance_to_goal = math.sqrt((goal_y-posy)**2 + (goal_x-posx)**2)
	if distance_to_goal < thresholddist_togoal:
		atGoal = True
	#follow type:  along the wall or along the line
	if abs(est_y-posy) < thresholddist_toline:
		follow_type = 0
	else:
		follow_type = 1

#turn function
def turn(pub,duration,turn_speed):
	vel = Twist()
	stopTime = rospy.Time.now() + rospy.Duration(duration)
	while rospy.Time.now() < stopTime:
		vel.linear.x = 0.0 
		vel.linear.y = 0.0 
		vel.linear.z = 0.0
		vel.angular.x = 0.0 
		vel.angular.y = 0.0 
		vel.angular.z = turn_speed;
		pub.publish(vel)
#go forward for a while
def goforward(pub,duration,move_speed):
	vel = Twist()
	stopTime = rospy.Time.now() + rospy.Duration(1)
	while rospy.Time.now() < stopTime:
		vel.linear.x = move_speed
		vel.linear.y = 0.0 
		vel.linear.z = 0.0
		vel.angular.x = 0.0 
		vel.angular.y = 0.0 
		vel.angular.z = 0.0
		pub.publish(vel)

def gostraight(pub,move_speed):
	vel = Twist()
	vel.linear.x = move_speed; 
	vel.linear.y = 0.0
	vel.linear.z = 0.0
	vel.angular.x = 0.0
	vel.angular.y = 0.0
	vel.angular.z = 0.0
	pub.publish(vel)


if __name__ == "__main__":

	rospy.init_node('wallfollower', anonymous=True)
	pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 10)
	sub = rospy.Subscriber('/scan', LaserScan, laser_callback)
	sub_pos = rospy.Subscriber('/gazebo/model_states', ModelStates, position_callback)
	temp_angle = 0
	while closeToObst != 1:
		gostraight(pub,movement_speed)
	while not rospy.is_shutdown():
		if atGoal:
			break

		if (follow_type == 0 and closeToObst == 0):
			temp_angle = angle_toturn
			vel_line = Twist()
			#turn to the goal direction
			turn(pub, 1, angle_toturn)
			if closeToObst == 1:
				turn(pub,1,-temp_angle*0.7)
			#go along the line until you find another wall
			stopTime = rospy.Time.now() + rospy.Duration(800)
			while rospy.Time.now() < stopTime:
				vel_line.linear.x = movement_speed*0.4
				vel_line.linear.y = 0.0
				vel_line.linear.z = 0.0
				vel_line.angular.x = 0.0
				vel_line.angular.y = 0.0
				vel_line.angular.z = 0.0
				pub.publish(vel_line)
				if (closeToObst == 1 or atGoal == True) :
					break
			# make sure that the robot go along the wall
			turn(pub,1,turn_speed) 
			
		elif (closeToObst == 1 or closeToObst == 2 or closeToObst == 3):
			if closeToObst == 1:
				turn(pub,duration,turn_speed)
				if follow_type == 0:
					goforward(pub,0.4,movement_speed)
			elif closeToObst == 2:
				goforward(pub,0.8,0.5)
				turn(pub,1.5,-0.5)
			elif closeToObst == 3:
				goforward(pub,0.8,0.5)
				turn(pub,1.5,-0.5)
		else:
			gostraight(pub,movement_speed)			
	
	print "FOUND GOAL!"
