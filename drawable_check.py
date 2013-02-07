#! /usr/bin/python

import os
import sys
import getopt
import random
import time

# list of param values
params = ["project-folder=","debug-output","test-removings","help"]

# method to display list of params
def usage():
	print "Android Resourcecheck-Parameters:"
	for param in params:
		explanation = "(add this param to enable the feature)"
		if param.endswith("="):
			explanation = "(a string)"	
		print "["+param[0:1]+"]"+param[1:]+" "+explanation

# get the execution params here
try:
	# "dth" are boolean-/ flag-params
	opts, args = getopt.getopt(sys.argv[1:], "dth", params)
except getopt.GetoptError, err:
	# will print something like "option -* not recognized"
	print str(err)
	sys.exit(2)

path = None
debug = False
testing = False

# make use of the params
for o, a in opts:
	if o in ("--project-folder"):
		path = a
	elif o in ("-d" "--debug"):
		debug = True
	elif o in ("-t" "--test-removings"):
		testing = True
	elif o in ("-h" "--help"):
		usage()
		sys.exit(1);

# change to projects /res-folder
if path is not None:
	baseFolder =  os.path.join(os.getcwd(),path,"res")
	os.chdir(baseFolder)
else:
	print "Project folder missing."
	sys.exit(1);

print '\033[1;92mStarted.\033[1;m'

# get all drawable-*dpi folders and there contents
drawableFoldersContent = []
for dirname, dirnames, filenames in os.walk('.'):
	if "drawable-" and "dpi" in dirname:
		drawableFoldersContent.append((os.path.basename(dirname), filenames))

# in case the testing parameter is set, remove some values to be sure we get a report
if testing:
	print
	print '\033[1;34mRemoving:\033[1;m'
	for x in range(0,len(drawableFoldersContent)):
		# remove two values
		for y in 0,1:
			valueToRemove = random.randrange(0,len(drawableFoldersContent[x][1]))
			print "from "+drawableFoldersContent[x][0]+": "+drawableFoldersContent[x][1][valueToRemove]
			del drawableFoldersContent[x][1][valueToRemove]

# create the report file with naming conventions
os.chdir("..")
report = open(os.path.join(os.getcwd(),time.strftime("%y%m%d")+"_"+os.path.basename(os.getcwd())+" Resourcereport.txt"), "w")
report.write("Resourcereport for "+os.path.basename(os.getcwd())+"-Project:\n\n")

# this is the check for all drawables
resourceMissing = False
for x in range(0,len(drawableFoldersContent)):
	missings = []
	otherSets = range(0,len(drawableFoldersContent))
	otherSets.remove(x)
	# compare the current drawable folder-content with all other drawable folders to check for differences
	for y in otherSets:
		currentMissings = set(drawableFoldersContent[y][1]).difference(drawableFoldersContent[x][1])
		for missing in currentMissings:
			if missing not in missings:
				missings.append(missing)

	# write missing files to console and report file
	if len(missings) > 0:
		if not resourceMissing:
			print
			print '\033[1;34mFiles:\033[1;m'
			resourceMissing = True
		report.write("Files missing in "+drawableFoldersContent[x][0]+":\n")
		print "Files missing in "+drawableFoldersContent[x][0]+":"
		for missing in missings:
			report.write(" / "+missing+"\n")
			print " - "+missing

# in case no differences has been found
if not resourceMissing:
	report.write("No resources missing. Everything looks fine. :)\n")

# do debug output if intended to
if debug:
	print
	print '\033[1;34mDebug:\033[1;m'
	for dirname, filenames in drawableFoldersContent:
		print str(dirname)+": \n"+str(filenames)

# document the report creation time
report.write("\n\nThis report was generated at: "+time.strftime("%X - %B %d. %Y"))

report.close()

print
print '\033[1;92mFinished.\033[1;m'
sys.exit(0)