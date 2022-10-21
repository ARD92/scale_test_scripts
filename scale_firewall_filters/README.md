# Scale test firewall filter
Using the script, one can generate filters at scale. you can either push the filter configs to commit db or push the configs to ephemeral DB.

## Usage 
```
usage: scale_test_ff.py [-h] [-ip IP] [-u USER] [-p PASSWD] [-nf NUMF] [-nt NUMT] [-sip SIP] [-dip DIP] [-edb EDB]

optional arguments:
  -h, --help  show this help message and exit
  -ip IP      ip address to connect to
  -u USER     username of the device to connect to, default root
  -p PASSWD   password of device to connect to. default juniper123
  -nf NUMF    Number of firewall filters
  -nt NUMT    Number of terms per filter
  -sip SIP    source IP block to start. example. 1.0.0.0/8
  -dip DIP    Dest IP block to start. example. 1.0.0.0/8
  -edb EDB    set to true if need to program ephemeral db
```

## Example
```
python3 scale_test_ff.py -ip 192.167.1.10 -u root -p juniper123 -nf 10 -nt 200 -sip 1.1.1.0/24 -dip 2.2.2.0/24 -edb true

programming into ephemeral db with instance name EDB_FF_TEST
loading config...  1666310972.6865582
commit config... 1666311995.6666257
commit complete.. 1666311995.978557
```
