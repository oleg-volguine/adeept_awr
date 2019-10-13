#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Motor
# Product     : RaspRover
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2019/02/23
#
# --- User Changes ---
# Modified-by : ov.mymail@gmail.com
# Modified-on : 2019/10/13
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685

#change this form 1 to 0 to reverse servos
look_direction = 1


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# the min and max lengths of the pulse to drive the servo in ms. Servo sweeps angle from approx 0 to 180
# the actual range of the servo is bigger, however we reserve a small buffer at eith end, as  robot structure restricts movement
# moving outside of the range may damage the servo/roobt
servo_min =  100
servo_max =  500

# default servo position
default_pos = (servo_max - servo_min)/2

# current servo position
current_pos = default_pos;

# defines how much the servo moves each time. We increment/decrement the current value of the pulse by this amount
# smaller values allow move refined movement, but they may not be practical
servo_move_increment = 20

# time in seconds, to allow servo to move into position
servo_move_time = 0.5

# defines which servo to control, 0..15 on the Adafruit PCA9685
servo_id = 0;


# ensures that the new pulse value does not exceed the allowed range 
def ctrl_range(raw, max_genout, min_genout):
	if raw > max_genout:
		raw_output = max_genout
	elif raw < min_genout:
		raw_output = min_genout
	else:
		raw_output = raw
	return int(raw_output)


def camera_ang(direction, ang):
	global current_pos
	
	if ang == 'no':
                ang = servo_move_increment;
	if look_direction:
		if direction == 'lookdown':
			current_pos+=ang
			current_pos = ctrl_range(current_pos, servo_max, servo_min)
		elif direction == 'lookup':
			current_pos-=ang
			current_pos = ctrl_range(current_pos, servo_max, servo_min)
		elif direction == 'home':
			current_pos = default_pos
	else:
		if direction == 'lookdown':
			current_pos-=ang
			current_pos = ctrl_range(current_pos, servo_max, servo_min)
		elif direction == 'lookup':
			current_pos+=ang
			current_pos = ctrl_range(current_pos, servo_max, servo_min)
		elif direction == 'home':
			current_pos = default_pos	

        # send a pulse to servo of the specified length, pulse will start at '0' and end at 'current_pos'.
	pwm.set_pwm(servo_id, 0, int(current_pos));
	time.sleep(servo_move_time);


def clean_all():
	pwm.set_all_pwm(0, 0)


if __name__ == '__main__':
        
        current_pos = default_pos;
        '''
        while current_pos < servo_max:
                current_pos += servo_move_increment;        
                pwm.set_pwm(servo_id, 0, int(current_pos));
                time.sleep(servo_move_time);

        while current_pos > servo_min:
                current_pos -= servo_move_increment;        
                pwm.set_pwm(servo_id, 0, int(current_pos));
                time.sleep(servo_move_time);
        '''
        camera_ang('home', 'no');
        
        while current_pos < servo_max:
                current_pos += servo_move_increment;        
                camera_ang('lookup', 'no');
                #pwm.set_pwm(servo_id, 0, int(current_pos));
                #time.sleep(servo_move_time);
        while current_pos > servo_min:
                current_pos -= servo_move_increment;
                camera_ang('lookdown', 'no');

        
        
