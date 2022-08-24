import time
from subprocess import *
import os

PGFUZZ_HOME = os.getenv("PGFUZZ_HOME")

if PGFUZZ_HOME is None:
    raise Exception("PGFUZZ_HOME environment variable is not set!")

ARDUPILOT_HOME = os.getenv("ARDUPILOT_HOME")

if ARDUPILOT_HOME is None:
    raise Exception("ARDUPILOT_HOME environment variable is not set!")

open("restart.txt", "w").close()

c = 'gnome-terminal -- python ' + PGFUZZ_HOME + 'ArduPilot/open_simulator.py'
handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)

time.sleep(90)
c = 'gnome-terminal -- python ' + PGFUZZ_HOME + 'ArduPilot/fuzzing.py'
handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
output, error = handle.communicate()
if handle.returncode != 0:
    print("%d, %s, %s" % (handle.returncode, output, error))

while True:
	time.sleep(1)

	f = open("restart.txt", "r")

	if f.read() == "restart":
		f.close()
		open("restart.txt", "w").close()

		c = 'gnome-terminal -- python ' + PGFUZZ_HOME + 'ArduPilot/open_simulator.py'
		handle = Popen(c, stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
	
