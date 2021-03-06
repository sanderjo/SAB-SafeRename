#!/usr/bin/env python
import os
import sys
import re

language = 'ger' # 3 letters, lower case!


def handlemkv(mkvfilename):
	print mkvfilename
	# find Audio streams 	
	# ffmpeg -i *.mkv 2>&1 | grep -i -e Audio:
	# Example output:
	#    Stream #0:1(ger): Audio: ac3, 48000 Hz, stereo, fltp, 224 kb/s (default)
	#    Stream #0:2(jpn): Audio: ac3, 48000 Hz, stereo, fltp, 224 kb/s
	cmd = 'ffmpeg -i "' + mkvfilename + '" 2>&1 | grep -i -e Audio:'
	print "cmd is", cmd
	streamnumber = -1
	for thisline in os.popen(cmd).readlines():
		print thisline.rstrip()
		if thisline.find(language)>=0:
			try:
				# streamnumber = thisline.split(':')[1].split('(')[0]
				streamnumber = re.findall(r"[\w']+", thisline)[2]
				print "Stream number", streamnumber
				streamnumber = int(streamnumber)	# force it to be an integer so we know we found correct info
			except:
				print "Something went wrong with find the stream number. Please report with logfile"
				sys.exit(0)
			break
	if streamnumber >= 0:
		print "Language found in stream", streamnumber
	else:
		print("Language %s not found" % (language))
		return()
	print "Go on"

	# leave only one audio stream, remove all subs
	# mkvmerge -o new2.mkv -a 1 --nosubs movie-Ger-Jap-Dub.mkv
	directory, filename = os.path.split(mkvfilename)
	cleanmoviename = os.path.join(directory, "cleanedmovie.mkv")
	print "cleanmoviename", cleanmoviename
	cmd = 'mkvmerge -o "' + cleanmoviename + '" -a ' + str(streamnumber) + '  --nosubs "' + mkvfilename + '"'
	print "command is", cmd
	for thisline in os.popen(cmd).readlines():
		print thisline.rstrip()

	# Delete original mkv, rename new one to original name and chmod it
	print "Cleaning up"
	os.remove(mkvfilename)
	os.rename(cleanmoviename, mkvfilename)
	os.chmod(mkvfilename, 0775)



try:
	root = sys.argv[1]
except:
	print "Define directory on the commandline"
	sys.exit(1)

print("Language %s to be kept" % (language))

print "Searching:", root
for path, subdirs, files in os.walk(root):
    for name in files:
        fullname = os.path.join(path, name)
	if os.path.splitext(fullname)[1].lower() == '.mkv':
		print "Found mkv", fullname
		handlemkv(fullname)

