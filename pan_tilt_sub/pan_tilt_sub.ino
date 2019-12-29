#if defined(ARDUINO) && ARDUINO >= 100
     #include "Arduino.h"
   #else
     #include <WProgram.h>
   #endif
   
   #include <Servo.h> 
   #include <ros.h>
   #include <geometry_msgs/Quaternion.h>
   
   ros::NodeHandle  nh;
   float pan,tilt;
   Servo servo1;
   Servo servo2;
   
   void servo_cb( const geometry_msgs::Quaternion& cmd_msg){
    pan = map(cmd_msg.x, -90, 90, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
    servo1.write(pan); 

    tilt = map(cmd_msg.y, -90, 90, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
    servo2.write(tilt);
   }
   
   
   ros::Subscriber<geometry_msgs::Quaternion> sub("pan_tilt_topic", servo_cb);
   
   void setup(){
   
    nh.initNode();
    nh.subscribe(sub);
    
    servo1.attach(9);
    servo2.attach(10);//attach it to pin 9
  }
  
   void loop(){
     nh.spinOnce();
     delay(1);
   }
