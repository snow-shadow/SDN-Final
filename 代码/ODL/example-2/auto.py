import os
import time
def runteam1():
	os.system("./addt1.sh")
	time.sleep(1)
	os.system("./delt2.sh")
	return 1;
def runteam2():
	os.system("./addt2.sh")
	time.sleep(1)
	os.system("./delt1.sh")
	return 1;
os.system("./delflows.sh")
os.system("./inite.sh")
while(True):
	runteam1()
	runteam2()
