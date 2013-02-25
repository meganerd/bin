#!/usr/bin/env python2.7

import os
import os.path
import getopt, sys
import random
import glob

VERSION=1.00
    
def print_usage():
	print "Usage:"
	print "generate_wallpater.py -f <src file> -d <directory path>  -T <target file>"

def print_help():
	print "generate_wallpaper.py"
	print "Combine multiple wallpapers into a single wallpaper.\n"
	print_usage()
	print "\nOptions:"
	print "   -f (--file)       Source image file";
	print "   -d (--directory)  Source image directory";
	print "   -T (--target)     Target image file to generate"
	print "                     (Overwrites existing file)";
	print "   -V (--version)    script version";
	print "   -h (--help)       usage help \n";

def ValidateFile(filename):

	# Confirm that the file exists
	#if not os.path.exists(filename):
	#	print "Error: File \"" + filename + "\" does not exist!"
	#	sys.exit()

	# Confirm that the file is really a file
	if not os.path.isfile(filename):
		#print "Error: \"" + filename + "\" is not a file!"
		print "Error: File \"" + filename + "\" does not exist or is not a file!"
		sys.exit()

	# Get file extension
	file_extension = os.path.splitext(filename)[1][1:].strip()
	
	# Confirm that file extension is of type .jpg
	if file_extension is "jpg":  
		print "Error: Unsupported file format for file \"" + filename + "\" - Expected .jpg"
		sys.exit()

def ValidateDirectory(directory):
	# Confirm that directory exists
	#if not os.path.exists(directory):
	#	print "Error: Directory \"" + directory + "\" does not exist!"
	#	sys.exit()

	# Confirm that directory is really a directory
	if not os.path.isdir(directory):
		print "Error: Directory \"" + directory + "\" does not exist or is not a directory!"
		sys.exit()


def GetRandomFileFromDirectory(directory):
	
	# Get all .jpg files from directory
	files = glob.glob(directory + '*.jpg')
	
	# Confirm that at least one file was found
	nfiles = len(files)
	if nfiles < 1:
		print "Error: No files of extension \".jpg\" was found in directory \"" + directory + "\""
		sys.exit()
		
	
	# Need to validate the file type and existance here...
	
	
	# return random file
	index = random.randrange(0, len(files))
	return files[index]
	

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hVf:d:T:", ["help", "version", "file=", "directory", "target="])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		print_usage()
		sys.exit(2)
		
	filename = []
	target = None
	for o, a in opts:
		if o in ("-h", "--help"):
			print_help()
			sys.exit()
		elif o in ("-V", "--version"):
			print "Version", VERSION
			sys.exit()
		elif o in ("-f", "--file"):
			ValidateFile(a)
			filename.append(a)
		elif o in ("-d", "--directory"):
			directory = a
			
			if not directory[-1] is "/":
				directory += "/"
			
			ValidateDirectory(directory)
			filename.append(GetRandomFileFromDirectory(directory))
		elif o in ("-T", "--target"):
			target = a
		else:
			assert False, "unhandled option"
			
				
	# Do some validating of input data here and find out weather to use precreated wallpapers or generate dual-monitor wallpapers
	
	if (len(filename) == 1):
		cmd="hsetroot -fill " + filename[0]
		os.system(cmd)
	elif (len(filename) > 1):
		
		if (target == None):
			print "Target file missing. (--target flag)"
			sys.exit()
		
		cmd="convert " + " ".join(filename) + " +append " + target
		os.system(cmd)
		
		cmd="hsetroot -fill " + target
		os.system(cmd)
		
	else:
		print "Add at least one file and/or directory combined. (--file/--directory flag)"
		sys.exit()




if __name__ == "__main__":
	main()
	
