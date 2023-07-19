# Author: Aravind Prabhakar
# Version: 1.0
# Description: Scale MAPT domains on MX 

import argparse
from netaddr import *

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

parser = argparse.ArgumentParser()
parser.add_argument('-ip', action='store', dest='IP', type=str, help='ip address to connect to')
parser.add_argument('-u', action='store', dest='USER', type=str, default='root', help='username of the device to connect to, default root')
parser.add_argument('-p', action='store', dest='PASSWD', type=str, default='juniper123', help='password of device to connect to. default juniper123')
parser.add_argument('-nr', action='store', dest='NUMRULES', type=int, help='number of mapt rules')
parser.add_argument('-ns', action='store', dest='NUMSVCSET', type=int, help='number of service sets')
parser.add_argument('-edb', action='store', dest='EDB',type=str, default="false", help='set to true if need to program ephemeral db')
args=parser.parse_args()

def programMapDomains(nr, ns):
    print("programming domains")

def main():
    programMapDomains(args.NUMRULES, args.NUMSVCSET)
    dev = Device(host=args.IP, user=args.USER, password=args.PASSWD, port=int(args.PORT))
    try:
        dev.open()
        if args.EDB == "true":
            print("programming into ephemeral db with instance name MAPT")
            with Config(dev, mode='ephemeral', ephemeral_instance='MAPT') as cu:
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
