#!/usr/bin/env python

import roslib; roslib.load_manifest("chairbot_neato_node")
import rospy, time

from math import sin, cos, fabs
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
from sensor_msgs.msg import Joy
from std_msgs.msg import Int8
from chairbot_neato_driver.chairbot_neato_driver import Botvac
from sensor_msgs.msg import Joy

import socket
import re
global chairbot_number
hostname = socket.gethostname()
chair_id = re.search(r"\d+(\.\d+)?", hostname)
chairbot_number = chair_id.group(0)

class NeatoTeleop:

    def __init__(self):
        """ Start up connection to the Neato Robot. """
        rospy.init_node('Teleop'+chairbot_number, anonymous=True)
        self.rate = 10      
        self.cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        rospy.Subscriber('/joy', Joy, self.joy_handler, queue_size=10)
        self._joy_flag = False

    def joy_handler(self, joy_msg):
        self._joystick_buttons =  joy_msg.buttons
        self._joystick_axes = joy_msg.axes
        self._joy_flag = True

    def publish_commands(self):
        command = Twist()
        Lft_t = self._joystick_axes[0]
        Lft_d = self._joystick_axes[1]
        Rgh_t = self._joystick_axes[3]
        Rgh_d = self._joystick_axes[4]
        command.linear.x = -1*Lft_d
        command.angular.z = Rgh_t
        self.cmd_pub.publish(command)

    def spin(self):
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            if self._joy_flag:
                self.publish_commands()
            r.sleep()
                
if __name__ == "__main__":    
    neato_teleop = NeatoTeleop()
    neato_teleop.spin()
