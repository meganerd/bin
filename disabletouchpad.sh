#!/bin/sh
# This script disable touchpad if mouse is present

if /usr/bin/lsusb --verbose | grep --quiet "Mouse" ; then
        /usr/bin/synclient TouchPadOff=1
fi
