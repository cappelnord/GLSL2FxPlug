# Part of GLSL2FxPlug
# https://github.com/cappelnord/GLSL2FxPlug

import random
import os
import shutil
import sys

from processor import process_file
from utils import *

CWD = os.getcwd()

OUTPUT_DIR = "output/"
TEMPLATE_DIR = "src/templates/"

def random_dir_string():
	return "glsl2fxplug" + str(random.randint(50000, 100000))

def copy_test_project(src, dst, shader_src):
	print "Creating GLSLTest project ..."
	shutil.copytree(src, dst)
	shutil.copyfile(src + "/../gl_helpers.m", dst + "/GLSLTest/gl_helpers.m")
	shutil.copyfile(src + "/../gl_helpers.h", dst + "/GLSLTest/gl_helpers.h")
	template_copy_file(src + "/GLSLTest/AppDelegate.m", dst + "/GLSLTest/AppDelegate.m", {"SHADER_SRC": shader_src})
	return True

def build_glsltest(path):
	os.chdir(path)
	print "Building GLSLTest project ..."
	res = call_process("xcodebuild")
	if res["returncode"] != 0:
		print "--> Error building GLSLTest project:"
		print res["stderr"]
		return False

	return True

def run_shader_test(path):
	os.chdir(path + "/build/Release/GLSLTest.app/Contents/MacOS/")
	print "Running GLSLTest ..."
	res = call_process("./GLSLTest")
	sys.stdout.write(res["stdout"])
	if res["returncode"] != 0:
		print "--> Shaders didn't compile right!"
		return False
	else:
		print "--> Vertex & fragment shaders seem to be fine!"
		return True

def clean_up_test(path):
	shutil.rmtree(path)

def test_shader(data):
	shader_src = data["code"]["SHADER_SOURCE"]

	success = True
	path = "/tmp/" + random_dir_string()
	success = success and copy_test_project(TEMPLATE_DIR + "GLSLTest", path, shader_src)
	if success:
		success = success and build_glsltest(path)
	if success:
		success = success and run_shader_test(path)
	clean_up_test(path)

	if not success:
		print "--> Generated GLSL source:"
		print data["vertex_string"]
		print data["fragment_string"]
	
	os.chdir(CWD)
	return success
	
COMMAND_LINE_TOOLS_INSTALLED = """Did you install Xcode and it's Command Line Tools?
To get Command Line Tools open Xcode -> Preferences -> Downloads and install them there"""

def test_build_system(data):
	success = True
	print "Checking build system ..."
	xcodebuild_res = call_process("xcodebuild -version")
	cc_res = call_process("cc --version")
	
	if xcodebuild_res["returncode"] == 0:
		print "-->", xcodebuild_res["stdout"].split("\n")[0]
	else:
		print "--> Could not run xcodebuild!"
		print COMMAND_LINE_TOOLS_INSTALLED
		return False
	
	if cc_res["returncode"] == 0:
		print "-->", cc_res["stdout"].split("\n")[0]
	else:
		print "--> Could not run cc!"
		print COMMAND_LINE_TOOLS_INSTALLED
		return False
	
	# It's a little strange, that the FxPlug Framework seems to sit
	# in the example folder, but well ... as long as it works!
	fxplug_res = call_process("ls /Developer/Examples/FxPlug/FxPlug.framework/")
	
	if fxplug_res["returncode"] == 0:
		print "--> FxPlug SDK installed"
	else:
		print "--> Could not find FxPlug Framework."
		print "You can download the FxPlug SDK from https://developer.apple.com"
		return False
	
	return success

CMDPHASES = {
"template":		  {}, # this is special
"parse":          {"test": False, "generate": True,  "build": False, "install": False},
"test": 		  {"test": True,  "generate": False, "build": False, "install": False},
"generate":		  {"test": False, "generate": True,  "build": False, "install": False},
"build":		  {"test": True,  "generate": True,  "build": True,  "install": False},
"install":  	  {"test": True,  "generate": True,  "build": True,  "install": True},
"build-notest":   {"test": False, "generate": True,  "build": True,  "install": False},
"install-notest": {"test": False, "generate": True,  "build": True,  "install": True} 
}

def valid_cmd(cmd):
	return cmd in CMDPHASES.keys()
	
RETURNCODES = {
	"invalid_argcount": 	10,
	"invalid_command": 		11,
	"invalid_build_system": 12,
	"glsltest_failed": 		13,
	"could_not_read_file": 	14,
	"missing_command": 		15,
	"missing_shader": 		16,
	"generation_failed": 	17,
	"build_failed": 		18,
	"install_failed":		19
}

HELP = """

"""

TEMPLATE = """$GLSL2FXPLUG  1
$TYPE         filter
$CLASSNAME    %(name)s
$DISPLAYNAME  %(name)s
$DESCRIPTION  Descriptive Text
$GROUP        GLSL2FxPlug
$GROUPUUID    7E03B162-9472-4CE9-ADA5-139E0C6BDD32
$BUNDLEID     your.company.%(lower_name)s
$UUID         %(uuid)s

$VERTEX
/* Add your vertex shader parameters here */

void main() {
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}

$FRAGMENT
/* Add your fragment shader parameters here */
$INPUT InputTexture

void main() {
    gl_FragColor = texture2DRect(InputTexture, gl_TexCoord[0].st);
}

"""

def generate_template(filename):
	classname = filename[:filename.find(".")]
	#TODO: Check for valid classname

	print "Generating file template ..."
	values = {
		"name": classname,
		"lower_name": classname.lower(),
		"uuid": generate_uuid()
	}
	file_string = TEMPLATE%values;
	
	print "Wrote file template to", filename
	out_file = open(filename, "w")
	out_file.write(file_string)
	out_file.close()

def generate_project(data):
	src_classname = "GLSLFxPlug"
	classname = data["info"]["CLASSNAME"]
	os.chdir(CWD)
	try_create_dir(OUTPUT_DIR)
	try_create_dir(OUTPUT_DIR + classname)
	dst_path = OUTPUT_DIR + classname + "/src/"
	print "Generating project to", dst_path
	try_create_dir(dst_path)
	try_create_dir(dst_path + classname + ".xcodeproj")

	shutil.copyfile(TEMPLATE_DIR + "gl_helpers.m", dst_path + "gl_helpers.m")
	shutil.copyfile(TEMPLATE_DIR + "gl_helpers.h", dst_path + "gl_helpers.h")

	info = data["info"]
	code = data["code"]

	template_copy_file(TEMPLATE_DIR + src_classname+"/"+src_classname+".h", dst_path + classname + ".h", 
		copy_dict_into({"CLASSNAME": classname}, code)
	)

	template_copy_file(TEMPLATE_DIR + src_classname+"/"+src_classname+".m", dst_path + classname + ".m", 
		copy_dict_into({"CLASSNAME": classname}, code)
	)


	template_copy_file(TEMPLATE_DIR + src_classname+"/Info.plist", dst_path + "Info.plist", 
		copy_dict_into({"CLASSNAME": classname}, info)
	)


	template_copy_file(TEMPLATE_DIR + src_classname+"/"+src_classname+".xcodeproj/project.pbxproj",
					   dst_path + classname + ".xcodeproj/project.pbxproj", {
		"CLASSNAME": classname
	})

	return True

def build_project(data):
	print "Building project ..."
	
	os.chdir(CWD)
	classname = data["info"]["CLASSNAME"]
	dst_path = OUTPUT_DIR + classname + "/"
	os.chdir(dst_path + "src")
	res = call_process("xcodebuild -configuration Release")
	if res["returncode"] != 0:
		print "--> Error building project:"
		print res["stdout"]
		print res["stderr"]
		return False

	print "--> Build complete!"

	os.chdir(CWD)

	final_dst_path = dst_path + classname + ".fxplug"

	try: shutil.rmtree(final_dst_path)
	except: pass

	shutil.move(dst_path + "src/build/Release/" + classname + ".fxplug", final_dst_path)
	shutil.rmtree(dst_path + "src/build")

	print "--> Product moved to " + dst_path

	return True

def install_project(data):
	print "Installing plug-in  ..."
	os.chdir(CWD)
	classname = data["info"]["CLASSNAME"]
	path = os.getenv("HOME") + "/Library/Plug-Ins"
	try_create_dir(path)
	path = path + "/FxPlug"
	try_create_dir(path)

	final_dst_path = path + "/" + classname + ".fxplug"

	try: shutil.rmtree(final_dst_path)
	except: pass

	shutil.copytree(OUTPUT_DIR + classname + "/" + classname + ".fxplug", final_dst_path)
	print "--> Plug-In copied to " + path

	return True

def main(cmd, file):
	if not valid_cmd(cmd):
		print "Invalid command:", cmd
		print HELP
		sys.exit(RETURNCODES["invalid_command"])
	
	if not file.find(".") > 0:
		file  = file + ".glsl2fxplug"

	if cmd == "template":
		generate_template(file)
		sys.exit(0)
	
	phases = CMDPHASES[cmd]
	
	print "GLSL2FxPlug " + VERSION + "\n-->", cmd, file
	
	print "Processing input file ..."

	data = process_file(file)
	if not data:
		print "Processing ", file, "failed.\nI'm giving up!"
		sys.exit(RETURNCODES["could_not_read_file"])

	for k in data["info"].keys():
		if data["info"][k] == None:
			print "-->", k, "is missing. I'm giving up!"
			sys.exit(RETURNCODES["missing_command"])

	if data["fragment_string"] == None:
		print "--> found no fragment shader. I'm giving up!"
		sys.exit(RETURNCODES["missing_shader"])

	if data["vertex_string"] == None:
		print "--> found no vertex shader. I'm giving up!"
		sys.exit(RETURNCODES["missing_shader"])

	def perform_and_test(phase, func, sorry, returncode):
		if phases[phase]:
			if not func(data):
				print sorry + ". I'm giving up!"
				sys.exit(RETURNCODES[returncode])

	perform_and_test("test", test_build_system, "Build system not complete", "invalid_build_system")
	perform_and_test("test", test_shader, "GLSLTest failed", "glsltest_failed")
	perform_and_test("generate", generate_project, "Could not generate project", "generation_failed")
	perform_and_test("build", build_project, "Could not build project", "build_failed")	
	perform_and_test("install", install_project, "Could not install project", "instal_failed")

arg_cmd = "build"
arg_file = ""
if len(sys.argv) < 2 or len(sys.argv) > 3:
	print "Invalid argument count."
	print HELP
	sys.exit(RETURNCODES["invalid_argcount"])
if len(sys.argv) == 2:
	arg_file = sys.argv[1]
if len(sys.argv) == 3:
	arg_file = sys.argv[2]
	arg_cmd = sys.argv[1]

main(arg_cmd, arg_file)