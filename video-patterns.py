import json
import serial #Requires PySerial
import serial.tools.list_ports
import time
import applescript
import signal
import sys


#####################################
#
# Detect and Connect to Vybe Device
#
#####################################


#Load Vybe device details
vybe_desc = {}
with open('vybe.json', 'r') as f:
	vybe_desc = json.load(f)


#Search for all connected Vybe devices
connectedDevices = []
for portcandidate in serial.tools.list_ports.comports():
	port_type = portcandidate[2] #each port description is a list of length 3; item 3 has vendor id and product id
	# if port_type.find('USB VID:PID=%s:%d'%(str(vybe_desc["comm"]["usbserial"]["vid"]), vybe_desc["comm"]["usbserial"]["pid"])) >= 0:
	if port_type.find('USB VID:PID=0483:5740')>= 0: #or just change json to "0483", always plug in power first, rather than usb first
		print "Found %s"%(portcandidate[0],)
		connectedDevices.append(portcandidate[0]) #name of this port

#Connect to first found Vybe device
vybe = None
if connectedDevices:
	portname = connectedDevices[0]
	vybe = serial.Serial(port=portname, baudrate=vybe_desc["comm"]["usbserial"]["baud"], writeTimeout = 0.05)
else:
	raise IOError("%s not detected."%(vybe_desc["name"],))

#####################################
#
# Functions for activating actuators
#
#####################################

def SetVoicecoil(index, value):
	value = min(max(0, value), 255)

	# format: "VCL <number as character> <buzz value 0-255 as character\n"
	msg = 	"VCL %s %s\n"%(str(index), chr(value))
	vybe.write(msg)
	vybe.flush()


def SetMotor(index, value):
	value = min(max(0, value), 255)

	# format: "MTR <number as character> <buzz value 0-255 as character\n"
	msg = 	"MTR %s %s\n"%(str(index), chr(value))
	vybe.write(msg)
	vybe.flush()

######################################################
#
# Heartbeat function parameterized 
# Want to insert "gaps" programmatically before each
# Fixed heartbeat (always same time buzz?)
######################################################
def HeartBeat():
	buzz_intensity_motor_1 = 130 
	buzz_intensity_motor_2 = 195 
	buzz_duration = 0.084 #seconds for vibrator to actually vibrate
	# buzz_duration = 0.07 #seconds for vibrator to actually vibrate
	# break_duration = 0.125 #seconds to sleep as our "break", might need to re-adjust depending on "perceived urgency" of heartbeat, 0.01 for intense, 0.1 as norm
	break_duration = 0.084 #seconds to sleep as our "break", might need to re-adjust depending on "perceived urgency" of heartbeat, 0.01 for intense, 0.1 as norm

	#first beat of heartbeat
	SetMotor(5, buzz_intensity_motor_1)
	time.sleep(buzz_duration)
	SetMotor(5, 0)

	#break btw beats of heartbeat
	time.sleep(break_duration)

	#second beat of heartbeat
	SetMotor(6, buzz_intensity_motor_2)
	time.sleep(buzz_duration)
	SetMotor(6, 0)

######################################################
#
# Checker
# 
######################################################
def Checker(value):
    if value == 'beat':
        HeartBeat()
        print 'Beat'
    else:
        SetMotor(5,0)
        SetMotor(6,0)
        time.sleep(float(value))
        print 'Pause'

######################################################
#
# Run Video AppleScript
# 
######################################################

def video():
    script = applescript.AppleScript('''
    tell application "QuickTime Player"
    activate
	set theMovie to open file "Matthew's MacBook Air:Users:Matthew:Desktop:edited driving clips:drive-full-transistion.mov"
	tell theMovie
	    play
		set the presenting to true
		set the looping to false
	end tell
	
	--use this to see what properties can be modified
	--get the properties of theMovie
    end tell
    ''').run()

def kill_running_video():
    script = applescript.AppleScript('''
    tell application "System Events"
	set ProcessList to name of every process
	if "QuickTime Player" is in ProcessList then
		set ThePID to unix id of process "QuickTime Player"
		do shell script "kill -KILL " & ThePID
	end if
    end tell
    ''').run()

### Only works at the end
def end_video():
    script = applescript.AppleScript('''
    tell application "QuickTime Player" to quit
    ''').run()


######################################################
#
# Catch control + c - kill script safely 
# 
######################################################

def signal_handler(signal, frame):
    #end_video() #doesnt seem to run here?
    #kill_running_video() #also doesn't seem to work here
    exit(0)

def zero():
	for i in range(1,7):
		SetVoicecoil(i, 0)
		SetMotor(i, 0)



########################################################
# Play Zone
########################################################

driving_part_1 = [1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat', 1.7, 'beat']
driving_part_2 = [1.4, 'beat', 1.4, 'beat', 1.0, 'beat', 0.5, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat']
driving_part_3 = [0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat',
0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat',
0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat'
]
driving_part_4 = [ 0.3, 'beat', 0.3, 'beat', 0.5, 'beat', 0.5, 'beat', 0.5, 'beat',
1.0, 'beat', 1.4, 'beat'
]
driving_part_5 = [1.7, 'beat', 1.7, 'beat', 1.4, 'beat', 1.4, 'beat', 0.5, 'beat']
driving_part_6 = [0.5, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 
0.3, 'beat', 0.3, 'beat', 0.3, 'beat', 0.3, 'beat',  0.3, 'beat', 0.3, 'beat', 0.3, 'beat',  0.3, 'beat',  0.3, 'beat',  0.3, 'beat', 0.3, 'beat', 0.3, 'beat',
0.5, 'beat', 0.5, 'beat', 1.0, 'beat', 1.4, 'beat'
]

motor1 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,38,38,37,37,37,37,36,36,36,35,35,35,35,34,34,34,33,33,33,33,32,32,32,32,31,31,31,30,30,30,30,29,29,29,29,28,28,28,27,27,27,27,26,26,26,25,25,25,25,24,24,24,24,23,23,23,22,22,22,22,21,21,21,20,20,20,20,19,19,19,19,18,18,18,17,17,17,17,16,16,16,16,15,15,15,14,14,14,14,13,13,13,12,12,12,12,11,11,11,11,10,10,10,9,9,9,9,8,8,8,8,7,7,7,6,6,6,6,5,5,5,4,4,4,4,3,3,3,3,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,3,3,4,4,4,5,5,6,6,7,7,7,8,8,9,9,9,10,10,11,11,11,12,12,13,13,14,14,14,15,15,16,16,16,17,17,18,18,18,19,19,20,20,21,21,21,22,22,23,23,23,24,24,25,25,26,26,26,27,27,28,28,28,29,29,30,30,30,31,31,32,32,33,33,33,34,34,35,35,35,36,36,37,37,37,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,38,38,37,37,37,37,37,36,36,36,36,36,35,35,35,35,35,34,34,34,34,33,33,33,33,33,32,32,32,32,32,31,31,31,31,31,30,30,30,30,29,29,29,29,29,28,28,28,28,28,27,27,27,27,27,26,26,26,26,25,25,25,25,25,24,24,24,24,24,23,23,23,23,22,22,22,22,22,21,21,21,21,21,20,20,20,20,20,19,19,19,19,18,18,18,18,18,17,17,17,17,17,16,16,16,16,16,15,15,15,15,14,14,14,14,14,13,13,13,13,13,12,12,12,12,12,11,11,11,11,10,10,10,10,10,9,9,9,9,9,8,8,8,8,8,7,7,7,7,6,6,6,6,6,5,5,5,5,5,4,4,4,4,4,3,3,3,3,2,2,2,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,3,3,4,4,4,5,5,6,6,7,7,8,8,9,9,9,10,10,11,11,12,12,13,13,14,14,14,15,15,16,16,17,17,18,18,18,19,19,20,20,21,21,22,22,23,23,23,24,24,25,25,26,26,27,27,28,28,28,29,29,30,30,31,31,32,32,32,33,33,34,34,35,35,36,36,37,37,37,38,0]


motor2 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,38,38,37,37,37,37,36,36,36,35,35,35,35,34,34,34,33,33,33,33,32,32,32,32,31,31,31,30,30,30,30,29,29,29,29,28,28,28,27,27,27,27,26,26,26,25,25,25,25,24,24,24,24,23,23,23,22,22,22,22,21,21,21,20,20,20,20,19,19,19,19,18,18,18,17,17,17,17,16,16,16,16,15,15,15,14,14,14,14,13,13,13,12,12,12,12,11,11,11,11,10,10,10,9,9,9,9,8,8,8,8,7,7,7,6,6,6,6,5,5,5,4,4,4,4,3,3,3,3,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,3,3,4,4,4,5,5,6,6,7,7,7,8,8,9,9,9,10,10,11,11,11,12,12,13,13,14,14,14,15,15,16,16,16,17,17,18,18,18,19,19,20,20,21,21,21,22,22,23,23,23,24,24,25,25,26,26,26,27,27,28,28,28,29,29,30,30,30,31,31,32,32,33,33,33,34,34,35,35,35,36,36,37,37,37,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,38,38,37,37,37,37,37,36,36,36,36,36,35,35,35,35,35,34,34,34,34,33,33,33,33,33,32,32,32,32,32,31,31,31,31,31,30,30,30,30,29,29,29,29,29,28,28,28,28,28,27,27,27,27,27,26,26,26,26,25,25,25,25,25,24,24,24,24,24,23,23,23,23,22,22,22,22,22,21,21,21,21,21,20,20,20,20,20,19,19,19,19,18,18,18,18,18,17,17,17,17,17,16,16,16,16,16,15,15,15,15,14,14,14,14,14,13,13,13,13,13,12,12,12,12,12,11,11,11,11,10,10,10,10,10,9,9,9,9,9,8,8,8,8,8,7,7,7,7,6,6,6,6,6,5,5,5,5,5,4,4,4,4,4,3,3,3,3,2,2,2,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,3,3,4,4,4,5,5,6,6,7,7,8,8,9,9,9,10,10,11,11,12,12,13,13,14,14,14,15,15,16,16,17,17,18,18,18,19,19,20,20,21,21,22,22,23,23,23,24,24,25,25,26,26,27,27,28,28,28,29,29,30,30,31,31,32,32,32,33,33,34,34,35,35,36,36,37,37,37,38,0]
motor3 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,11,12,13,14,15,16,17,18,19,20,21,22,23,23,24,25,26,27,28,29,30,31,32,33,34,34,35,36,37,38,39,40,41,42,43,44,45,46,46,47,48,49,50,51,52,53,54,55,56,57,58,58,59,60,61,62,63,64,65,66,67,68,69,69,70,71,72,73,74,75,76,77,78,79,80,81,81,82,83,84,85,86,87,88,89,90,91,92,93,93,94,95,96,97,98,99,100,101,102,103,104,104,105,106,107,108,109,110,111,112,113,114,115,116,116,117,118,119,120,121,122,123,124,125,126,127,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,126,125,123,122,121,119,118,116,115,114,112,111,110,108,107,105,104,103,101,100,99,97,96,94,93,92,90,89,88,86,85,83,82,81,79,78,77,75,74,72,71,70,68,67,66,64,63,61,60,59,57,56,55,53,52,50,49,48,46,45,44,42,41,39,38,37,35,34,33,31,30,28,27,26,24,23,22,20,19,17,16,15,13,12,11,9,8,6,5,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,3,4,4,5,6,7,7,8,9,9,10,11,11,12,13,14,14,15,16,16,17,18,18,19,20,21,21,22,23,23,24,25,26,26,27,28,28,29,30,30,31,32,33,33,34,35,35,36,37,37,38,39,40,40,41,42,42,43,44,45,45,46,47,47,48,49,49,50,51,52,52,53,54,54,55,56,56,57,58,59,59,60,61,61,62,63,64,64,65,66,66,67,68,68,69,70,71,71,72,73,73,74,75,75,76,77,78,78,79,80,80,81,82,82,83,84,85,85,86,87,87,88,89,90,90,91,92,92,93,94,94,95,96,97,97,98,99,99,100,101,101,102,103,104,104,105,106,106,107,108,109,109,110,111,111,112,113,113,114,115,116,116,117,118,118,119,120,120,121,122,123,123,124,125,125,126,127,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,126,124,123,121,120,118,117,115,114,112,111,109,108,106,105,103,102,100,99,97,96,94,93,91,90,88,87,85,84,82,81,79,78,76,75,73,72,70,69,67,66,64,63,61,60,58,57,55,54,52,51,49,48,46,45,43,42,40,39,37,36,34,33,31,30,28,27,25,24,22,21,19,18,16,15,13,12,10,9,7,6,4,3,1,0,0]


motor4 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,11,11,12,13,14,15,16,17,18,19,20,21,22,23,23,24,25,26,27,28,29,30,31,32,33,34,34,35,36,37,38,39,40,41,42,43,44,45,46,46,47,48,49,50,51,52,53,54,55,56,57,58,58,59,60,61,62,63,64,65,66,67,68,69,69,70,71,72,73,74,75,76,77,78,79,80,81,81,82,83,84,85,86,87,88,89,90,91,92,93,93,94,95,96,97,98,99,100,101,102,103,104,104,105,106,107,108,109,110,111,112,113,114,115,116,116,117,118,119,120,121,122,123,124,125,126,127,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,126,125,123,122,121,119,118,116,115,114,112,111,110,108,107,105,104,103,101,100,99,97,96,94,93,92,90,89,88,86,85,83,82,81,79,78,77,75,74,72,71,70,68,67,66,64,63,61,60,59,57,56,55,53,52,50,49,48,46,45,44,42,41,39,38,37,35,34,33,31,30,28,27,26,24,23,22,20,19,17,16,15,13,12,11,9,8,6,5,4,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,3,4,4,5,6,7,7,8,9,9,10,11,11,12,13,14,14,15,16,16,17,18,18,19,20,21,21,22,23,23,24,25,26,26,27,28,28,29,30,30,31,32,33,33,34,35,35,36,37,37,38,39,40,40,41,42,42,43,44,45,45,46,47,47,48,49,49,50,51,52,52,53,54,54,55,56,56,57,58,59,59,60,61,61,62,63,64,64,65,66,66,67,68,68,69,70,71,71,72,73,73,74,75,75,76,77,78,78,79,80,80,81,82,82,83,84,85,85,86,87,87,88,89,90,90,91,92,92,93,94,94,95,96,97,97,98,99,99,100,101,101,102,103,104,104,105,106,106,107,108,109,109,110,111,111,112,113,113,114,115,116,116,117,118,118,119,120,120,121,122,123,123,124,125,125,126,127,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,126,124,123,121,120,118,117,115,114,112,111,109,108,106,105,103,102,100,99,97,96,94,93,91,90,88,87,85,84,82,81,79,78,76,75,73,72,70,69,67,66,64,63,61,60,58,57,55,54,52,51,49,48,46,45,43,42,40,39,37,36,34,33,31,30,28,27,25,24,22,21,19,18,16,15,13,12,10,9,7,6,4,3,1,0,0]


motor5 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
130,130,0,0,0,0]
motor6 = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,195,195]


video()

# for idx,val in enumerate(driving_part_1): 
#    print idx 
#    Checker(val)
# 
# #this does work here at least
# #kill_running_video()

# for idx,val in enumerate(driving_part_2): 
#    print idx 
#    Checker(val)

# for idx,val in enumerate(driving_part_3): 
#    print idx 
#    Checker(val)

# for idx,val in enumerate(driving_part_4): 
#    print idx 
#    Checker(val)

# for idx,val in enumerate(driving_part_5): 
#    print idx 
#    Checker(val)

# for idx,val in enumerate(driving_part_6): 
#    print idx 
#    Checker(val)

for i in range(0,len(motor1)):
	SetMotor(1,motor1[i])
	SetMotor(2,motor2[i])
	SetMotor(3,motor3[i])
	SetMotor(4,motor4[i])
	SetMotor(5,motor5[i])
	SetMotor(6,motor6[i])
	time.sleep(0.042)


end_video()
zero()
exit(0)

#for killing script and ending safely on control+c
signal.signal(signal.SIGINT, signal_handler)
# sleep until a signal is received
signal.pause()