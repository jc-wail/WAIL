#!/usr/bin/python
import sys
import commands
import re
from tags import *
ip_exp = re.compile('\d+[.]\d+[.]\d+[.]\d+')

#Process command line arguments
value = sys.argv[1]
options = ""

#Run commands
print "running traceroute"
cmd_val = commands.getstatusoutput("traceroute "+value+" "+options)


#Process command vals 
# Option line max hops = 30
# <Hop number> <dns or ip> (<ip>) <latency1> ms <latency2> ms <latency3> ms 
# or
# * * *

print "analyzing return"
hops = []
line_number = 1
new_val = cmd_val[1].split("\n")
#print new_val
resolved = 0
not_resolved = 0
for lines in new_val:
#    print lines
    #eat first
    if line_number == 1:
        line_number = line_number+1
        continue
    #process numbered lines
    tmp = lines.split(" ")
    #remove all '' elements
    tmp1 = []
    for entries in tmp:
        if entries:
            tmp1.append(entries)
    tmp = tmp1
#    print tmp
    if not ip_exp.findall(tmp[1]):
        #print "*dns name "+tmp[1]
        if tmp[1]!="*":
            hops.append(tmp[1])
            resolved = resolved+1
    else:
        not_resolved = not_resolved+1
        #print "*no dns name found "+tmp[1]
        if tmp[1]!="*":
            hops.append("*no dns name found "+tmp[1])
    line_number = line_number+1

#call pathaudit analysis
print "Total hops: %s" %(resolved+not_resolved)
print "Resolved hops: %s" %(resolved) 
tags5_analysis(hops)
