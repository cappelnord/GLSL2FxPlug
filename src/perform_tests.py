from utils import call_process
import os
import sys
import shutil

cmd = "build"
if len(sys.argv) > 1:
	cmd = sys.argv[1]

files = os.listdir("tests/.")
files = [x for x in files if (x.endswith(".glsl2fxplug"))]

print "Testing all .glsl2fxplug files in tests/ with command: " + cmd

for filename in files:
	path = "tests/" + filename
	print "Running " + filename + " ..."
	ret = call_process("./glsl2fxplug.sh " + cmd + " " + path)
	if ret["returncode"] != 0:
		print ret["stdout"]
		sys.exit(-1)
	shutil.rmtree("output/" + filename[:filename.find(".")])

print "All tests ran without errors!"