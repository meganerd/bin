#!/bin/bash
# This script sets variables in i3 config file, and should therefore be called
# before (re)loading i3 - hence before the statement 'exec i3' in .xinitrc

ValidateFile() {
	if [ ! -f "$1" ]; then
		echo "Error: File \"$1\" does not exist!"
		exit 1
	fi
	return 0
}

if [ $# == 2 ]; then
	MONITOR1=$2
    MONITOR2=$2
elif [ $# == 3 ]; then
	MONITOR1=$2
    MONITOR2=$3
else
	echo "$0 <i3 config file> <screen name>"
	echo "$0 <i3 config file> <screen 1> <screen 2>"
	exit 1
fi

CONFIGFILE=$1

ValidateFile $CONFIGFILE

# One could validate the monitors by checking if they exists when calling 'xrandr -q'

sed -i "s/^set \$monitor1 [A-Z0-9-]\+$/set \$monitor1 $MONITOR1/g" $CONFIGFILE
sed -i "s/^set \$monitor2 [A-Z0-9-]\+$/set \$monitor2 $MONITOR2/g" $CONFIGFILE

