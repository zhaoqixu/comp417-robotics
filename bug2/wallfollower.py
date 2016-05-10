#!/usr/bin/env python

import rospy
import math

# The laser scan message
from sensor_msgs.msg import LaserScan

# The velocity command message
from geometry_msgs.msg import Twist



min_wall_distance = 0.8
closeToObst = 0
duration = 0.2
turn_speed = 0.4
movement_speed = 0.15


def laser_callback(scan):
	#use three beams to check the distance to the wall
	length = len(scan.ranges)
	midbeam = scan.ranges[length/2]
	leftmostbeam = scan.ranges[length-1]
	rightmostbeam = scan.ranges[0]

	if (leftmostbeam < min_wall_distance or rightmostbeam < min_wall_distance or midbeam < min_wall_distance):
		global closeToObst
		closeToObst = 1
	elif math.isnan(rightmostbeam): #need turn
	 	closeToObst = 2
	elif rightmostbeam > 1.2: #another condition that need turn
		closeToObst = 3
	else:
		closeToObst = 0

	

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
	vel = Twist()
	check = Twist()
	#first of all, find a wall
	while closeToObst != 1:
		gostraight(pub,movement_speed)
	#handle different situations 
	while not rospy.is_shutdown():
		#close to the wall
		if closeToObst == 1:
			turn(pub,duration,turn_speed)
		#if meet a door, go straight for a while then turn right
		elif closeToObst == 2:
			vel1 = Twist()
			stopTime = rospy.Time.now() + rospy.Duration(1)
			while rospy.Time.now() < stopTime:
				vel1.linear.x = 0.5
				vel1.linear.y = 0.0 
				vel1.linear.z = 0.0
				vel1.angular.x = 0.0 
				vel1.angular.y = 0.0 
				vel1.angular.z = 0.0;
				pub.publish(vel1)
			vel2 = Twist()
			stopTimeturn = rospy.Time.now() + rospy.Duration(1.5)
			while rospy.Time.now() < stopTimeturn:
				vel2.linear.x = 0.0
				vel2.linear.y = 0.0 
				vel2.linear.z = 0.0
				vel2.angular.x = 0.0 
				vel2.angular.y = 0.0 
				vel2.angular.z = -0.5;
				pub.publish(vel2)
		#turn right
		elif closeToObst == 3:
			vel1 = Twist()
			stopTime = rospy.Time.now() + rospy.Duration(1)
			while rospy.Time.now() < stopTime:
				vel1.linear.x = 0.5 
				vel1.linear.y = 0.0 
				vel1.linear.z = 0.0
				vel1.angular.x = 0.0 
				vel1.angular.y = 0.0 
				vel1.angular.z = 0.0;
				pub.publish(vel1)
			vel2 = Twist()
			stopTimeturn = rospy.Time.now() + rospy.Duration(1.5)
			while rospy.Time.now() < stopTimeturn:
				vel2.linear.x = 0.0
				vel2.linear.y = 0.0 
				vel2.linear.z = 0.0
				vel2.angular.x = 0.0 
				vel2.angular.y = 0.0 
				vel2.angular.z = -0.5;
				pub.publish(vel2)
		else:
			vel.linear.x = movement_speed; #go straight
			vel.linear.y = 0.0
			vel.linear.z = 0.0
			vel.angular.x = 0.0
			vel.angular.y = 0.0
			vel.angular.z = 0.0
			pub.publish(vel)






		

