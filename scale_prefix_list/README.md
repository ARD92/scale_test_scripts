script to test prefix list scaling

Example
```
python3 scale_test_prefix_list.py -pl PL11 -count 83000 -ip 11.0.0.0/8
```

This will generate a prefix list name PL11 with 83000 prefixes starting from 11.0.0.0 and store in a file name scale_<PL name>_<count>

This can further be used to load the configs in the router/switch using `load set <filename>`
