#!/usr/bin/python2.7
# This code is based on the script from https://faq.i3wm.org/question/389/focus-next-window/ 
import i3

# Set focus to the next window on focused output
def focus_prev_on_output():
    
    # Get num of the focused workspace
    ws_num = i3.filter(i3.get_workspaces(), focused=True)[0]['num']

    # Get nodes on workspace
    ws_nodes = i3.filter(num=ws_num)[0]['nodes']

    # Get focused node
    curr = i3.filter(ws_nodes, focused=True)[0]

    # Get ids of all nodes
    ids = [win['id'] for win in i3.filter(ws_nodes, nodes=[])]

    # Get index of next node
    next_idx = (ids.index(curr['id']) - 1) % len(ids)

    # Set id of next node
    next_id = ids[next_idx]

    # Focus next node
    i3.focus(con_id=next_id)

# Set focus to the next window on any output
def focus_prev_on_any_output():

    # Get all visible workspace(s) - the workspace(s) currently visible on output(s)
    workspaces = i3.filter(i3.get_workspaces(), visible=True)

    # Get list containing num of the visible workspaces
    workspaces_num = [ ws['num'] for ws in workspaces ]

    # Get visible nodes 
    nodes = [ i3.filter(num=ws_num)[0]['nodes'] for ws_num in workspaces_num ]

    # Get focused node
    curr = i3.filter(nodes, focused=True)[0]

    # Get ids of all nodes
    ids = [win['id'] for win in i3.filter(nodes, nodes=[])]

    # Get index of next node
    next_idx = (ids.index(curr['id']) - 1) % len(ids)

    # Set id of next node
    next_id = ids[next_idx]

    # Focus next node
    i3.focus(con_id=next_id)

if __name__ == '__main__':
    focus_prev_on_output()
    #focus_prev_on_any_output()
