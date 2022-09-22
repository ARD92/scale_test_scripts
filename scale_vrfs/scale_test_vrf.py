__author__ = "Aravind Prabhakar"

import argparse
from netaddr import *

parser = argparse.ArgumentParser()
parser.add_argument('-count', action='store',dest='CNT', help='Count of /32 prefixes')
parser.add_argument('-ip', action='store',dest='IP', help='subnet. a  /32 prefix for loopback would be allocated. Example. 1.1.1.0/24')
parser.add_argument('-rd', action='store',dest='RD', help='beginning range of RD. example 1000. will return 1000:x ')
parser.add_argument('-rt', action='store',dest='RT', help='beginning range of RT, example 1000, will return target:1000:x')
args=parser.parse_args()

IPV4_PL_ADDRESS = args.IP
VRF_RT_RANGE = args.RT+":"
VRF_RD_RANGE = args.RD+":"
SCALE_CONFIG = [] 


for count in range(0, int(args.CNT)):
    vpn = {}
    name = "VPN-"+str(count)
    ip = IPNetwork(IPV4_PL_ADDRESS).ip+count
    rd = VRF_RD_RANGE + str(count)
    rt = VRF_RT_RANGE + str(count)
    
    CONFIG = [
        'set interfaces lo0.{} family inet address {}'.format(str(count), str(ip)),
        'set routing-instances VPN-{} instance-type vrf'.format(str(count)),
        'set routing-instances VPN-{} interface lo0.{}'.format(str(count), str(count)),
        'set routing-instances VPN-{} route-distinguisher {}'.format(str(count), rd),
        'set routing-instances VPN-{} vrf-target target:{}'.format(str(count), rt),
        'set routing-instances VPN-{} vrf-table-label'.format(str(count))
        ]

    vpn[name] = CONFIG
    SCALE_CONFIG.append(vpn)

with open('scaled_vrf_{}'.format(args.CNT),'w') as f:
    for i in SCALE_CONFIG:
        for j in i.values():
            for k in j:
                f.write(k)
                f.write('\n')
f.close()

