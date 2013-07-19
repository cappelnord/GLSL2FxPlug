# Part of GLSL2FxPlug
# https://github.com/cappelnord/GLSL2FxPlug

import subprocess
import os

VERSION = "0.1"

def replace_key(key):
	return "${" + key.upper() + "}"

"""
def template_replace(string, dict):
	for key in dict.keys():
		string = string.replace(replace_key(key), dict[key])
	return string
"""

# White-Space Indendation aware template_replace
def template_replace(string, dict):
	input_lines = string.splitlines()
	output_lines = []

	for line in input_lines:
		single_line_key = None

		for key in dict.keys():
			if line.strip() == replace_key(key):
				single_line_key = key
				break

		if not single_line_key:
			for key in dict.keys():
				line = line.replace(replace_key(key), dict[key])
			output_lines.append(line)
		else:
			whitespace = line[:line.find(replace_key(key))]
			new_lines = dict[key].splitlines()
			for new_line in new_lines:
				output_lines.append(whitespace + new_line)

	return "\n".join(output_lines)

	
def template_copy_file(src, dst, dict):
	s = ""
	with open(src, "r") as input_file:
		s = input_file.read()
	s = template_replace(s, dict)
	with open(dst, "w") as output_file:
		output_file.write(s)

def call_process(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	res = process.communicate()
	return {"returncode":process.returncode, "stdout":res[0], "stderr":res[1]}

def generate_uuid():
	return call_process("uuidgen")["stdout"]

def try_create_dir(path):
	if not os.path.isdir(path): os.mkdir(path)

def copy_dict_into(dst, src):
	for key in src.keys():
		dst[key] = src[key]
	return dst