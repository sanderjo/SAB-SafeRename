#!/usr/bin/env python
import os
import sys

language = 'ger' # 3 letters, lower case!


def handlemkv(name):
	print name
	# find Audio streams 	
	# ffmpeg -i *.mkv 2>&1 | grep -i -e Audio:
	# Example output:
	#    Stream #0:1(ger): Audio: ac3, 48000 Hz, stereo, fltp, 224 kb/s (default)
	#    Stream #0:2(jpn): Audio: ac3, 48000 Hz, stereo, fltp, 224 kb/s
	cmd = 'ffmpeg -i "' + name + '" 2>&1 | grep -i -e Audio:'
	print "cmd is", cmd
	streamnumber = -1
	for thisline in os.popen(cmd).readlines():
		print thisline.rstrip()
		if thisline.find(language)>=0:
			streamnumber = thisline.split(':')[1].split('(')[0]
			break
	if streamnumber >= 0:
		print "Language found in stream", streamnumber
	else:
		print("Language %s not found" % (language))
		return()
	print "Go on"

	# leave only one audio stream, remove all subs
	# mkvmerge -o new2.mkv -a 1 --nosubs movie-Ger-Jap-Dub.mkv
	directory, filename = os.path.split(name)
	cleanmoviename = os.path.join(directory, "cleanedmovie.mkv")
	print "cleanmoviename", cleanmoviename
	cmd = 'mkvmerge -o "' + cleanmoviename + '" -a 1 --nosubs "' + name + '"'
	print "command is", cmd
	for thisline in os.popen(cmd).readlines():
		print thisline.rstrip()

	# move / rename
	# to do ...


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
		handlemkv(fullname)

