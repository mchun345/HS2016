import numpy as np


motor1 = open("motor1.txt","wb")
motor2 = open("motor2.txt","wb")
motor3 = open("motor3.txt","wb")
motor4 = open("motor4.txt","wb")
motor5 = open("motor5.txt","wb")
motor6 = open("motor6.txt","wb")

def write_break_1_7():
	for i in range(0,40):
		motor1.write("0,")
		motor2.write("0,")
		motor3.write("0,")
		motor4.write("0,")
		motor5.write("0,")
		motor6.write("0,")
	motor1.write("\n")
	motor2.write("\n")
	motor3.write("\n")
	motor4.write("\n")
	motor5.write("\n")
	motor6.write("\n")



def write_break_1_4():
	for i in range(0,33):
		motor5.write("0,")
		motor6.write("0,")
	motor5.write("\n")
	motor6.write("\n")



def write_break_1():
	for i in range(0,25):
		motor5.write("0,")
		motor6.write("0,")
	motor5.write("\n")
	motor6.write("\n")


def write_break_500():
	for i in range(0,12):
		motor5.write("0,")
		motor6.write("0,")
	motor5.write("\n")
	motor6.write("\n")



def write_break_300():
	for i in range(0,7):
		motor5.write("0,")
		motor6.write("0,")
	motor5.write("\n")
	motor6.write("\n")



def write_beat():
	# motor1.write("0,0,0,0,0,0,")
	# motor2.write("0,0,0,0,0,0,")
	# motor3.write("0,0,0,0,0,0,")
	# motor4.write("0,0,0,0,0,0,")
	motor5.write("130,130,0,0,0,0,")
	motor6.write("0,0,0,0,195,195,")
	# motor1.write("\n")
	# motor2.write("\n")
	# motor3.write("\n")
	# motor4.write("\n")
	motor5.write("\n")
	motor6.write("\n")


def write_lerp(val):
	val = float(val)
	intensity1 = int((val)*128)
	intensity2 = int((1-val)*128*.3)
	motor1.write("%d," % intensity2)
	motor2.write("%d," % intensity2)
	motor3.write("%d," % intensity1)
	motor4.write("%d," % intensity1)

# SetMotor(1, intensity5)
# SetMotor(3, intensity6)
# SetMotor(2, intensity5)
# SetMotor(4, intensity6)

motor1.write("motor1 = [\n")
motor2.write("motor2 = [\n")
motor3.write("motor3 = [\n")
motor4.write("motor4 = [\n")
motor5.write("motor5 = [\n")
motor6.write("motor6 = [\n")

for i in range(0,11):
	write_break_1_7()
	write_beat()
	motor1.write("0,0,0,0,0,0,")
	motor2.write("0,0,0,0,0,0,")
	motor3.write("0,0,0,0,0,0,")
	motor4.write("0,0,0,0,0,0,")


write_break_1_4()
write_beat()
write_break_1_4()
write_beat()
write_break_1()
write_beat()
write_break_500()
write_beat()

for i in np.linspace(0,1,140):
	write_lerp(i)

for i in range(0,44):
	write_break_300()
	write_beat()

for i in range(0,344):
	write_lerp(1)

for i in np.linspace(1,0,94):
	write_lerp(i)

write_break_500()
write_beat()
write_break_500()
write_beat()
write_break_500()
write_beat()
write_break_1()
write_beat()
write_break_1_4()
write_beat()
write_break_1_7()
write_beat()
write_break_1_7()
write_beat()
write_break_1_4()
write_beat()
write_break_1_4()
write_beat()
write_break_500()
write_beat()
write_break_500()
write_beat()

for i in range(0,15):
	write_break_300()
	write_beat()

write_break_500()
write_beat()
write_break_500()
write_beat()
write_break_1()
write_beat()
write_break_1_4()
write_beat()

# fo.write("]")

motor1.write("0]\n")
motor2.write("0]\n")
motor3.write("0]\n")
motor4.write("0]\n")
motor5.write("0]\n")
motor6.write("0]\n")

motor1.close()
motor2.close()
motor3.close()
motor4.close()
motor5.close()
motor6.close()
