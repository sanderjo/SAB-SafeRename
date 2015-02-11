#!/usr/bin/env python
# SABnzbd post-processing script to rename files based on info found in rename.sh-like scripts
# based on https://github.com/clinton-hall/GetScripts/blob/master/SafeRename.py

import os
import sys
import re

import shlex # because we need ignoring spaces within quotes

def rename_script(dirname):
    rename_file = ""
    for dir, dirs, files in os.walk(dirname):
        for file in files:
            if re.search('(rename\S*\.(sh|bat))',file):
                rename_file = os.path.join(dir, file)
                dirname = dir
                break
    if rename_file: 
        rename_lines = [line.strip() for line in open(rename_file)]
        for line in rename_lines:
            #cmd = filter(None, re.split('(?:mv|Move)\s+(\S+)\s+(\S+)',line))
            if re.search('^(mv|Move)', line, re.IGNORECASE):
                cmd = shlex.split(line)[1:]
            else:
                continue 
            if len(cmd) == 2 and os.path.isfile(os.path.join(dirname, cmd[0])):
                orig = os.path.join(dirname, cmd[0])
                dest = os.path.join(dirname, cmd[1].split('\\')[-1].split('/')[-1])
                if os.path.isfile(dest):
                    continue
                print "[INFO] Renaming file %s to %s" % (orig, dest)
                try:
                    os.rename(orig, dest)
                except Exception,e:
                    print "[ERROR] Unable to rename file due to: %s" % (str(e))
                    sys.exit(NZBGET_POSTPROCESS_ERROR)


# Main

try:
    (scriptname,directory,orgnzbname,jobname,reportnumber,category,group,postprocstatus,url) = sys.argv
except:
    try:
        # are we testing only?
        directory = sys.argv[1]
    except:
        print "No commandline parameters found"
        sys.exit(1)    

print "Directory is", directory
rename_script(directory)

