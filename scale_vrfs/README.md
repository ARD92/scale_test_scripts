# Generate scaled VRF context 

```
python3 scale_test_vrf.py -count 128 -ip 2.2.2.0/24 -rd 1001 -rt 1000
```

This will generate 128 VRFs each with a loopback interface with IP in the 2.2.2.0/24 block. The RT would be 1000:x where 0<x<128 . Similarly RD would also be 0<x<128.
The configs would be saved in a file with scaled_vrf_<count>.txt 

## Outputs
```
#more scaled_vrf_128

set interfaces lo0.0 family inet address 2.2.2.0
set routing-instances VPN-0 instance-type vrf
set routing-instances VPN-0 interface lo0.0
set routing-instances VPN-0 route-distinguisher 1001:0
set routing-instances VPN-0 vrf-target target:1000:0
set routing-instances VPN-0 vrf-table-label
set interfaces lo0.1 family inet address 2.2.2.1
set routing-instances VPN-1 instance-type vrf
set routing-instances VPN-1 interface lo0.1
set routing-instances VPN-1 route-distinguisher 1001:1
set routing-instances VPN-1 vrf-target target:1000:1
set routing-instances VPN-1 vrf-table-label
< -------- snipped --------- >
```
