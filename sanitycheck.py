#!/usr/bin/env python
'''
gives a count of how many individual ips are in a given input (from stdin) and informs you if there were repleats of any of the provided ips
can also alternatively output the IPs individually (with -o flag). 

usage:
cat <filewithips> | python sanitycheck.py
cat <filewithips> | python sanitycheck.py -o > outfile

may or may not handle spaces, haven't checked. 
handles some dashes. (the 1.1.1.1-5 kind, not the 1.1.1.1-1.1.1.5 kind.)
only takes ips separated by /n currently. 


--if on mac and not running cuz netaddr;
wget http://python-distribute.org/distribute_setup.py
python distribute_setup.py
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install netaddr

(looks like this might only be necessary for older verisons of mac.)
(don't forget the sudo, it gets upset.)

*****
okay, so, issue: 
74.125.224.72 is 74.125.224.072 but not 74.125.224.720
i mean, duh, right but that means:
12.232.246.2 and 12.232.246.20 are different
and duh, right but. 
something is not adding up. I think there's a difference in how the IPs are formatted.
this presents a problem. 

turned out this was a masscan issue, not a me issue.
still might be a problem, but. probably not.

12.6.16
aparently couldn't handle newlines. hackfixed.
should also consider handling ips separated by commas. (that sounds. well. actually not that bad probably, just replace every , with a \n.)

1.2.18
apparently doesn't like cidr over /16? not positive but. 
anyway, you shouldn't be printing out any ranges over /16 anyway, and there should be a python module that interprets cidr (if you aren't already using it), so maybe if it's over /16, refuse to do -o and just skip manually counting through an O(N) loop
'''

import sys
import argparse 
from netaddr import *

parser = argparse.ArgumentParser()
parser.add_argument("-o","--output", action="store_true", help="output IPs to screen instead of giving sanity check. ")
args = parser.parse_args()

count = 0
dashfound = ""
output = 0
ip_list = []

if args.output:
  output = 1

for line in sys.stdin:
  if "-" in line: #breaks in here somewhere i think #fixed
    #print "line: ", line
    ips = line.replace(" ", "")
    #print len(ips)
    print "ips:", ips
    dashchar = "-"
    dash = ips.find(dashchar)
    lastp = ips.rfind('.')+1+1 #what is this??
    #lastp = len(ips) #?? or length of base??
    base = ips[0:lastp-1] #is this ever different from ips?? #oohhh
    bfrom = ips[lastp-1:dash]
    #bfrom = ips[0:dash]
    bto = ips[dash+1:] #what was i thinking
    
    #print "dash:", dash, " lastp:", lastp, " base:", base, " bfrom:", bfrom, " bto:", bto

    for i in range(int(bfrom), int(bto)+1):
      ip_list.append(str(base)+str(i))
      count = count + 1 #also fixed this, only workes for x.x.x.#-#, not x.x.#.#-#.#. not sure if i wanna deal with that tbh.
      

  #if "-" is not in line:
  else:
    try:
      ip = IPNetwork(line)
      count = count + ip.size
      for i in ip:
        ip_list.append(str(i))
    except:
      print "invalid IP: ", line
        
ip_list = sorted(set(ip_list))
if output == 0:
  print count
  dups = len(ip_list)
  if len != count: 
    print len(ip_list), " (hi, there were some duplicates in your list, you might want to check that out.)"
  
if output == 1:
  for i in ip_list:
    print '%s' % i
