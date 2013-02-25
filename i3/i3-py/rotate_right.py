#!/usr/bin/python2.7
# This script move all visible workspaces to the right and keeps the workspace
# names in place

# This method has problems in case one screen has no open windows
# Maybe a solution could be to check for open windows and use the standard
# move to output right command (or whatever it is called).

# It may be possible to move containers rather than workspaces to improve
# performance

# Doesn't work if there is only one open workspace on one of the outputs
# This has to be fixed

import i3

# Define a constant temporary name for the first workspace
WS_TMP_NAME = 'ws_tmp_name'


# This function rotates all workspaces one output to the right and keep focus
# to the focused output
def rotate_workspaces_to_right():

    # Get all visible workspace(s) - the workspace(s) currently visible on output(s)
    workspaces = i3.filter(i3.get_workspaces(), visible=True)
 
    # Get list containing num of the visible workspaces
    ws_names =  [ ws['num'] for ws in workspaces ]
     
    # Get focused workspace id/name
    ws_focused = i3.filter(workspaces, focused=True)[0]['num']

    # Get index of focused node in ws_names
    idx = ws_names.index(ws_focused)

    # Create a range that starts from the index of the focused node so the
    # focused output is the last to be rotated to the right. This results in
    # the focus to stay on the same output
    ws_range = [ index%len(ws_names) for index in range(idx-1,idx+len(ws_names)-1) ]

    # Rename the first workspace to the temporary name
    i3.command('rename workspace {0} to {1}'.format(ws_names[idx],WS_TMP_NAME))

    # For each visible workspace
    for i in ws_range:
        
        # Get name of workspace to be in focus
        ws_name = WS_TMP_NAME if i==idx else ws_names[i]

        # Set focus to workspace by id/name
        i3.workspace( str(ws_name) )

        # Rename focused workspace to id/name of workspace to the right
        i3.command('rename workspace {0} to {1}'.format( ws_name, ws_names[(i+1) % len(ws_names)] ) )

        # Move focused workspace to output on the right
        i3.command('move workspace to output right')


# This function rotates all workspaces one output to the right and keep focus
# to the focused output
def rotate_workspaces_to_right_and_keep_ws_names():

    # Get all visible workspace(s) - the workspace(s) currently visible on output(s)
    workspaces = i3.filter(i3.get_workspaces(), visible=True)
 
    # Get list containing num of the visible workspaces
    ws_names =  [ ws['num'] for ws in workspaces ]
     
    # Get focused workspace id/name
    ws_focused = i3.filter(workspaces, focused=True)[0]['num']

    # Get index of focused node in ws_names
    idx = ws_names.index(ws_focused)

    # Create a range that starts from the index of the focused node so the
    # focused output is the last to be rotated to the right. This results in
    # the focus to stay on the same output
    ws_range = [ index%len(ws_names) for index in range(idx-1,idx+len(ws_names)-1) ]

    # For each visible workspace
    for i in ws_range:
        
        # Set focus to workspace by id/name
        i3.workspace( str(ws_names[i]) )

        # Move focused workspace to output on the right
        i3.command('move workspace to output right')



if __name__ == '__main__':
    rotate_workspaces_to_right()
    #rotate_workspaces_to_right_and_keep_ws_names()
