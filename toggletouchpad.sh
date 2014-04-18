#!/bin/sh
# This script toggles touchpad on/off

# Get current status for touchpad
val=$(synclient | awk '/TouchpadOff/ { print $3 }');

# Toggle touchpad status
/usr/bin/synclient TouchPadOff=$((! val))

