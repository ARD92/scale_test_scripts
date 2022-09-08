import argparse
from netaddr import *


parser = argparse.ArgumentParser()
parser.add_argument('-pl', action='store', dest='PL', type=str, default='PL', help='prefix list name')
parser.add_argument('-count', action='store',dest='CNT', help='Count of /32 prefixes')
parser.add_argument('-ip', action='store', dest='IP', help='IP block to start. example. 1.0.0.0/8')
args=parser.parse_args()

IPV4_PL_ADDRESS = args.IP
CLIST = []
CONFIG = 'set policy-options prefix-list {} '.format(args.PL)

for count in range(0, int(args.CNT)):
    ip = IPNetwork(IPV4_PL_ADDRESS).ip+count
    CLIST.append(CONFIG + str(ip))

with open('scaled_{}'.format(args.PL +'_'+ args.CNT),'w') as f:
    for i in CLIST:
        f.write(i)
        f.write('\n')
f.close()

