#!/usr/bin/env python2.7

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sin, cos, sqrt

x = y = theta = 0.0

def callback(data):
    global x, y, theta
    x = data.x
    y = data.y
    q = data.orientation
    (_, _, theta) = euler_from_quaternion([q.x, q.y, q.z, q.w])

def move_bot():
    global x, y, theta
    #k_linear = 0.25
    k_angular = 1.0
    rospy.init_node('go_to_goal', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    vel = Twist()
    goal = Point()
    rate = rospy.Rate(10)
    goal.x = float(input('Enter x - coordinate of goal: '))
    goal.y = float(input('Enter y - coordinate of goal: '))
    while sqrt((goal.x - x)**2 + (goal.y - y)**2) > 0.1:
        e_y = goal.y - y
        e_x = goal.x - x
        #e_linear = sqrt(e_x**2 + e_y**2)
        theta_desired = atan2(e_y,e_x)
        e_theta = theta_desired - theta
        e_theta = atan2(sin(e_theta),cos(e_theta))
        vel.angular.z = k_angular*e_theta
        vel.linear.x = 0
        vel.linear.y = sin(theta)
        #vel.linear.x = k_linear*e_linear
        pub.publish(vel)
        rate.sleep()
    vel.linear.x = 0.0
    vel.angular.y = 0.0
    vel.angular.z  = 0.0
    pub.publish(vel)

if __name__=='__main__':
    try:
        move_bot()
    except rospy.ROSInterruptException:
        pass