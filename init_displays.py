#!/usr/bin/env python2.7
import os
import re
import commands


# The screen name of the laptop (get it by 'xrandr -q')
screen_laptop = 'LVDS-0'

# Screen names in prioritized order of which should be primary screen
# (Should contain all screens from xrandr that might be used
screen_names = [ 'LVDS-0', 'HDMI-0', 'VGA-0' ]


# Get current xrandr setup 
( stat, output ) = commands.getstatusoutput( "xrandr -q" )

# Get information of all screens ( 'name', 'conn', 'res + offset', 'best res' )
#regex = "^(VGA-0|TV-0|LVDS-0|HDMI-0) (\w+) ([0-9x+]*).*\n\s*([0-9]+x[0-9]+)?"
#m = re.findall(regex, output, re.M)
#print m

# We are only interrested in connected displays and prefer numerical values isolated
# Information of each connected screen is saved on the form:
# ( 'name', 'res+off', 'xres', 'yres', 'xoff', 'yoff', 'best res', 'xres', 'yres' )
regex=("^({0}) connected " 
       "(([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+))?.*\n\s*(([0-9]+)x([0-9]+))?"
       ).format('|'.join(screen_names))
screens = re.findall(regex, output, re.M)


# Sort screens according to priority of which screen to be primary
# (j starts from i+1 as there is no point in swapping screens in case of i==k.
# Also, the last screen should be placed correct so no need to confirm last
# screen
for i in range(len(screen_names)-1):
    for j in range(i+1,len(screens)):
        if (screen_names[i] == screens[j][0]):
            screens[i], screens[j] = screens[j], screens[i]


# In case more than one screen is connected, check if the laptop's lid is closed
if (len(screens) > 1):
    with open('/proc/acpi/button/lid/LID/state', 'r') as f:
        data = f.read()
        if (data.find("closed") >= 0): # If lid is closed
            for i in range(len(screens)):
                if (screens[i][0] == 'LVDS-0'):
                    del screens[i]
                    break

# Gets a list of disconnected screens
disabled_screen_names = screen_names
for screen in screens:
    disabled_screen_names.remove(screen[0])

# Make a substring of disconnected screens for xrandr that is to be executed later
disabled_screen_names_str = ""
for screen_name in disabled_screen_names:
    disabled_screen_names_str += "--output {0} --off ".format(screen_name)


# Execute xrandr command depending on number of connected screens
# Also, a wallpaper is set according to the display settings
if (len(screens) == 1): # Only a single screen remaining
    xrandr_cmd = ("xrandr {0}--output {1} --auto --primary"
                    ).format(disabled_screen_names_str, screens[0][0])
    path = '~/Downloads/wallpapers/{0}/'.format(screens[0][6])

elif (len(screens) == 2):   # Two screens remaining 
    xrandr_cmd = ("xrandr {0}--output {1} --auto --primary --output {2} "
                    "--auto --right-of {1}"
                    ).format(disabled_screen_names_str, screens[0][0], screens[1][0])
    path = '~/Downloads/wallpapers/generated/{0}_{1}/'.format(screens[0][6], screens[1][6])

else:   # Three or more screens remaining
    print "This has not been handled yet"

# There might be created a safety to handle zero screens found!

os.system(xrandr_cmd)
os.system('~/bin/generate_wallpaper/generate_wallpaper.py -d ' + path)

print ' '.join( screen[0] for screen in screens )

