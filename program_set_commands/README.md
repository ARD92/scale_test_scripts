# Program configs to node either to commit db or ephemeral DB

```
(pyez) root@ubuntu:/opt/aprabh/generate_report# python3 program_set_commands.py --help
usage: program_set_commands.py [-h] [-ip IP] [-u USER] [-p PASSWD] [-f FILE]
                               [-edb EDB]

optional arguments:
  -h, --help  show this help message and exit
  -ip IP      ip address to connect to
  -u USER     username of the device to connect to, default root
  -p PASSWD   password of device to connect to. default juniper123
  -f FILE     file name which contains all set commands. Default file name is set
              to config
  -edb EDB    set to true if need to program ephemeral db
```

## Example:

### Program commit DB
```
python3 program_set_commands.py -ip 192.167.1.10 -u root -p juniper123 -f config
```

### Program ephemeral DB
```
python3 program_set_commands.py -ip 192.167.1.10 -u root -p juniper123 -f config -edb true
```
