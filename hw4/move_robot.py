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
    print("MOVE FORWARD")
    enc_tgt(1,1,3)
    fwd()
    time.sleep(0.5)


def move_center(): 
    pass