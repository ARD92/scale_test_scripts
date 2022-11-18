# Author: Aravind Prabhakar
# Version: 1.0
# Description: Scale test firewall filter. This will generate a 5 tuple value to program with an accept/reject randomly along with a counter action.

import argparse
import random
from netaddr import *
import time
import os

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

parser = argparse.ArgumentParser()
parser.add_argument('-ip', action='store', dest='IP', type=str, help='ip address to connect to')
parser.add_argument('-u', action='store', dest='USER', type=str, default='root', help='username of the device to connect to, default root')
parser.add_argument('-p', action='store', dest='PASSWD', type=str, default='juniper123', help='password of device to connect to. default juniper123')
parser.add_argument('-pt', action='store', dest='PORT', type=str, default=830, help='port to connect netonf. default is 830')
parser.add_argument('-nf', action='store', dest='NUMF', type=int, default='1', help='Number of firewall filters')
parser.add_argument('-nfr', action='store', dest='NUMRANGE', type=int, default=0, help='Filter start range')
parser.add_argument('-nt', action='store',dest='NUMT',type=int,  help='Number of terms per filter')
parser.add_argument('-ntr', action='store', dest='NUMTRANGE', type=int, default=0, help='Filter term start range')
parser.add_argument('-sip', action='store', dest='SIP', type=str, help='source IP block to start. example. 1.0.0.0/8')
parser.add_argument('-dip', action='store', dest='DIP',type=str, help='Dest IP block to start. example. 1.0.0.0/8')
parser.add_argument('-edb', action='store', dest='EDB',type=str, default="false", help='set to true if need to program ephemeral db')
args=parser.parse_args()

# List of protocols. THis will be chosen at random
PROTOCOL = ['tcp', 'udp']

def programScaledFilters(nf, nfr, nt, ntr, sip, dip):
    # program filters at scale over netconf
    flist = []
    print("entering", nf, nt)
    for numfilter in range(nfr,nf):
        for numterms in range(ntr,nt):
            sip = str(IPNetwork(sip).ip+numterms)
            dip = str(IPNetwork(dip).ip+numterms)
            proto = random.choice(PROTOCOL)
            sports = random.randint(1,65535)
            dports = random.randint(1,65535)
            cmd_sip = "set firewall family inet filter FF_{} term TERM_{} from source-address {}".format(numfilter,numterms,sip)
            cmd_dip = "set firewall family inet filter FF_{} term TERM_{} from destination-address {}".format(numfilter,numterms,dip)
            cmd_sp = "set firewall family inet filter FF_{} term TERM_{} from source-port {}".format(numfilter,numterms,sports)
            cmd_dp = "set firewall family inet filter FF_{} term TERM_{} from destination-port {}".format(numfilter,numterms,dports)
            cmd_proto = "set firewall family inet filter FF_{} term TERM_{} from protocol {}".format(numfilter,numterms,proto)
            cmd_action = "set firewall family inet filter FF_{} term TERM_{} then accept".format(numfilter,numterms)
            cmd_action_count = "set firewall family inet filter FF_{} term TERM_{} then count count-term-{}".format(numfilter,numterms, numterms)
            flist.append(cmd_sip)
            flist.append(cmd_dip)
            flist.append(cmd_sp)
            flist.append(cmd_dp)
            flist.append(cmd_proto)
            flist.append(cmd_action)
            flist.append(cmd_action_count)
    return flist

def main():
    # compile filter list
    filterList = programScaledFilters(args.NUMF, args.NUMRANGE, args.NUMT, args.NUMTRANGE, args.SIP, args.DIP)
    # Push to device
    dev = Device(host=args.IP, user=args.USER, password=args.PASSWD, port=int(args.PORT))
    try:
        dev.open()
        if args.EDB == "true":
            print("programming into ephemeral db with instance name EDB_FF_TEST")
            with Config(dev, mode='ephemeral', ephemeral_instance='EDB_FF_TEST') as cu:
                fp = open("/tmp/config.txt","w")
                for data in filterList:
                    #cu.load(data,format='set')
                    fp.write(data + "\n")
                fp.close()
                print("loading config... ", time.time())
                cu.load(path="/tmp/config.txt", format='set')
                print("commit config...",time.time())
                cu.commit()
                print("commit complete..",time.time())
                os.remove("/tmp/config.txt")

        else:
            with Config(dev) as cu:
                fp = open("/tmp/config.txt","w")
                for data in filterList:
                    #cu.load(data, format='set')
                    fp.write(data + "\n");
                fp.close()
                print("loading config...", time.time())
                cu.load(path="/tmp/config.txt", format='set', timeout=360)
                print("commit config...",time.time())
                cu.commit(timeout=360)
                print("commit complete..",time.time())
                os.remove("/tmp/config.txt")

        dev.close()
    except Exception as e:
        print("Exception occured..", e)

if __name__ == "__main__":
    main()

