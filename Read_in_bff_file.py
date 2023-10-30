'''
Read in and extract all relevant data from bff file
'''
        
import numpy as np              

def get_grid(fname): 
    '''
    Get an array of grid elements.

    **Parameters**

        fname: *str*
            The file name to read in

    **Returns**

        grid: *array*
            An array of elements. o is an open spot and x is an unavailable
            spot.
    '''         
    infile = open(fname)
    start_search = False
    grid_list = []
    for line in infile:
        if line.strip() == "GRID START":
            start_search = True
            continue
        elif line.strip() == "GRID STOP":
            start_search = False
            continue
        elif start_search:
            grid_list.append([i for i in line.strip() if i != ' '])

    grid = np.array(grid_list)
    return grid


def get_blocks(fname):
    '''
    Get a dictionary of block type and number.

    **Parameters**

        fname: *str*
            The file name to read in

    **Returns**

        block_dict: *dictionary*
            A dictionary of blocks. Keys are block types and values are the
            number of blocks.
    '''  
    '''
        infile = open(fname)
    is_grid = False
    grid_list = []
    for line in infile:
        if line.strip() == "GRID START":
            is_grid = True
            continue
        elif line.strip() == "GRID STOP":
            is_grid = False
            continue
        elif is_grid:
            grid_list.append([i for i in line.strip() if i != ' '])
    '''
    
    dict_A = {}
    dict_B = {}
    dict_C = {}
    start_search = False
    for line in open(fname):
        if '#' in line:
            continue
        elif line.strip() == 'GRID STOP':
            start_search = True
        elif start_search:
            if 'A ' in line:
                A_line = [i for i in line.strip() if i != ' ']
                dict_A['reflective_blocks'] = int(A_line[1])
            elif 'B ' in line:
                B_line = [i for i in line.strip() if i != ' ']
                dict_B['opaque_blocks'] = int(B_line[1])
            elif 'C ' in line:
                C_line = [i for i in line.strip() if i != ' ']
                dict_C['refractive_blocks'] = int(C_line[1])

    block_dict = {}
    if len(dict_A) != 0:
        block_dict.update(dict_A)
    if len(dict_B) != 0:
        block_dict.update(dict_B)
    if len(dict_C) != 0:
        block_dict.update(dict_C)

    return block_dict


def get_laser_pos(fname):
    '''
    Find the x and y coordinates of the laser and the vx and vy directions
    it's facing.

    **Parameters**

        fname: *str*
            The file name to read in

    **Returns**

        laser_dict: *dictionary*
            A dictionary that contains the laser number and its corresponding
            integer x, y, vx, vy values as a tuple.
    '''  
    infile = open(fname)
    x_list = []
    y_list = []
    vx_list = []
    vy_list = []
    start_search = False
    for line in infile:
        if '#' in line:
            continue
        elif line.strip() == 'GRID STOP':
            start_search = True
        elif start_search:
            if 'L ' in line:
                laser_pos_raw = [i for i in line.strip().split(' ')]
                x_list.append(int(laser_pos_raw[1]))
                y_list.append(int(laser_pos_raw[2]))
                vx_list.append(int(laser_pos_raw[3]))
                vy_list.append(int(laser_pos_raw[4]))

    laser_num = len(x_list)
    laser_dict = {}
    keys = range(laser_num)
    for i in keys:
        x = x_list[i]
        y = y_list[i]
        vx = vx_list[i]
        vy = vy_list[i]
        laser_dict[i] = (x, y, vx, vy)
    return laser_dict


def get_goal_points(fname):
    '''
    Find the x and y coordinates of the goal points for the laser to intersect.

    **Parameters**

        fname: *str*
            The file name to read in

    **Returns**

        point_dict: *dictionary*
            A dictionary that contains the goal point number and it's
            corresponding coordinates.
    '''  
    infile = open(fname)
    x_list = []
    y_list = []
    start_search = False
    for line in infile:
        if '#' in line:
            continue
        elif line.strip() == 'GRID STOP':
            start_search = True
        elif start_search:
            if 'P ' in line:
                point_pos_raw = [i for i in line.strip().split(' ')]
                x_list.append(int(point_pos_raw[1]))
                y_list.append(int(point_pos_raw[2]))

    point_num = len(x_list)
    point_dict = {}
    keys = range(point_num)
    for i in keys:
        x = x_list[i]
        y = y_list[i]
        point_dict[i] = (x, y)

    return point_dict


if __name__ == "__main__":
    grid = get_grid('dark_1.bff')
    print(grid)
    blocks = get_blocks('dark_1.bff')
    print(blocks)
    laser_pos = get_laser_pos('dark_1.bff')
    print(laser_pos)
    goal_points = get_goal_points('dark_1.bff')
    print(goal_points)
