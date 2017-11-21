import time
import io 
from gopigo import *

def right_uturn():
    print("UTURN - RIGHT")
    set_left_speed(100)
    set_right_speed(100)
    DPR = 360.0/64
    enc_tgt(1,0,int(95//DPR))
    right_rot()
    time.sleep(0.5)


def left_uturn():
    print("UTURN - LEFT")
    set_left_speed(100)
    set_right_speed(100)
    DPR = 360.0/64
    enc_tgt(0,1,int(95//DPR))
    left_rot()
    time.sleep(0.5)


def move_forward():
    set_left_speed(105)
    set_right_speed(100)
    print("MOVE FORWARD")
    enc_tgt(1,1,3)
    fwd()
    time.sleep(0.5)


def turn_left_degrees(deg): 
    set_left_speed(100)
    set_right_speed(100)
    DPR = 360.0/64
    enc_tgt(0,1,int(deg//DPR))
    left_rot()
    time.sleep(1.5)


def turn_right_degrees(deg): 
    set_left_speed(100)
    set_right_speed(100)
    DPR = 360.0/64
    enc_tgt(1,0,int(deg//DPR))
    right_rot()
    time.sleep(1.5)


def move_forward_pixels(pix):
    #100 pixels = 2 inches
    #8 inches = 18 in tgt
    inches = float(pix)/float(50)
    print("MOVE FORWARD")
    enc_tgt(1,1,int((18/float(8))*inches))
    fwd()
    time.sleep(0.5)


def move_left_to_line(dist):
    print("turning left to line...")
    turn_left_degrees(90)
    print("moving to line...")
    move_forward_pixels(dist)
    print("turning right back to parallel...")
    turn_right_degrees(90)


def move_right_to_line(dist):
    print("turning right to line...")
    turn_right_degrees(90)
    print("moving to line...")
    move_forward_pixels(dist)
    print("turning left back to parallel...")
    turn_left_degrees(90)

