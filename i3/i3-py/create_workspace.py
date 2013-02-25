#!/usr/bin/python2.7
# This script creates the first available workspace
# It assumes a setup of one or two monitors
#
#  With one monitor, the following setup is assumed
#   monitor with workspaces [ 1 2 3 4 5 6 7 8 9 10 ]
#
#  With two monitor, the following setup is assumed
#   monitor 1 with workspaces [ 1 2 3 4 5  ] 
#   monitor 2 with workspaces [ 6 7 8 9 10 ]

import i3

# If possible - create first available workspace on output
def create_next_workspace_on_output():

    # Get all workspace(s) 
    workspaces = i3.get_workspaces()

    # Current workspace
    current = [ws for ws in workspaces if ws['focused']][0]
    output = current['output']

    # Get list containing num of the workspaces on current output 
    ws_names = [ ws['num'] for ws in workspaces if ws['output'] == output ]

    # Set start and end 'num' for workspaces depending on setup of one or two
    # monitors
    if ( len(ws_names) == len(workspaces) ): # One monitor
        start = 1
        end = 10
    else:   # Two monitors
        start = 1 if current['num'] < 6 else 6
        end = start+5

    # Create workspace on output with lowest available 'num'
    for k in range(start,end):
        if not k in ws_names:
            i3.command('workspace {}'.format(k))
            break;


if __name__ == '__main__':
    create_next_workspace_on_output()

