# Author: Aravind Prabhakar
# Version : v1.0
# Description: Program configs in set formmat into commit db or ephemeral DB
#              If eDB , then the instance name would be named as PGMD-EDB

import time
import argparse 

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.utils.config import Config

parser = argparse.ArgumentParser()
parser.add_argument('-ip', action='store', dest='IP', type=str, help='ip address to connect to')
parser.add_argument('-u', action='store', dest='USER', type=str, default='root', help='username of the device to connect to, default root')
parser.add_argument('-p', action='store', dest='PASSWD', type=str, default='juniper123', help='password of device to connect to. default juniper123')
parser.add_argument('-f', action='store', dest='FILE', type=str, default='config', help='file name which contains all set commands. Default file name is set to config')
parser.add_argument('-edb', action='store', dest='EDB',type=str, default="false", help='set to true if need to program ephemeral db')
args=parser.parse_args()


def main():
    # Push configs to device
    dev = Device(host=args.IP, user=args.USER, password=args.PASSWD)
    try:
        dev.open()
        if args.EDB == "true":
            print("programming into ephemeral db with instance name PGMD_EDB")
            with Config(dev, mode='ephemeral', ephemeral_instance='PGMD_EDB') as cu:
                with open(args.FILE, "r") as f:
                    fread = f.read()
                    print("loading config... time(s)=", time.time())
                    print("load complete.. commiting config...time(s)=",time.time())
                    cu.load(fread, format='set', merge=True)
                    cu.commit()
                    print("commit complete..time(s)=",time.time())

        else:
            with Config(dev) as cu:
                with open(args.FILE, "r") as f:
                    fread = f.read()
                    print(fread)
                    print("loading config... ", time.time())
                    cu.load(fread, format='set', merge=True)
                    print("commit config...",time.time())
                    cu.commit()
                    print("commit complete..",time.time())
        dev.close()

    except Exception as e:
        print("Exception occured..", e)

if __name__ == "__main__":
    main()

