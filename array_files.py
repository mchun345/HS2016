motor5 = open("motor5.txt","wb")
motor6 = open("motor6.txt","wb")

def write_break_1_7():
	for i in range(0,40):
		motor5.write("0,")
		motor6.write("0,")
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
	motor5.write("130,130,0,0,0,0,")
	motor6.write("0,0,0,0,195,195,")
	motor5.write("\n")
	motor6.write("\n")

motor5.write("motor5 = [\n")
motor6.write("motor6 = [\n")

for i in range(0,11):
	write_break_1_7()
	write_beat()

write_break_1_4()
write_beat()
write_break_1_4()
write_beat()
write_break_1()
write_beat()
write_break_500()
write_beat()

for i in range(0,44):
	write_break_300()
	write_beat()

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

motor5.close()
motor6.close()
