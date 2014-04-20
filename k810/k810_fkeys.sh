#!/bin/bash
# The script turn function keys on
# Based on Michael's script http://blog.chschmid.com/?p=1537

line=`dmesg | grep -i k810 | grep hidraw | tail -n 1`
[[ $line =~ (.*)(hidraw[^:]+)(.*) ]]
device=${BASH_REMATCH[2]}
./k810_conf -d /dev/${device} -f on
