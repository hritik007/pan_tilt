#!/usr/bin/env python
from __future__ import print_function

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

#from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
import sys, select, termios, tty

pan_counter=0
tilt_counter=0
pan=0
tilt=0

moveBindings = {
        's':(1,0,0,0),
        'w':(-1,0,0,0),
        'd':(0,-1,0,0),
        'a':(0,1,0,0),
    }

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('pan_tilt_topic', Quaternion, queue_size = 1)
    rospy.init_node('pan_tilt_node')

    speed = rospy.get_param("~speed", 1.0)
    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                

                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            else:
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break
            
            global pan_counter,tilt_counter, pan,tilt

            commands=Quaternion()

            if(pan_counter>90):
                pan=90
            elif(pan_counter<-90):
                pan=-90
            else:
                pan=pan+y
            
            if(tilt_counter>90):
                tilt=90
            elif(tilt_counter<-90):
                tilt=-90
            else:
                tilt=tilt+x            

            commands.x=tilt
            commands.y=pan


            pan_counter=pan_counter+y
            tilt_counter=tilt_counter+x
            print("w: up  s: down  a: left  d: right")
            print("pan  : "+str(-pan)+" Degrees")
            print("tilt : "+str(-tilt)+" Degrees")
            print("......................")

            pub.publish(commands)

    except Exception as e:
        print(e)