'''
Read in and extract all relevant data from bff file
'''
    
import numpy as np   
from more_itertools import distinct_permutations as idp
from blocks import Block, Edge
import time
import os
import glob

### TODO: Add check to make sure laser direction abs(slope) = 1
### TODO: Can you add two blocks next to eachother??
### TODO: Convert final board to desired output, not sure what it needs to be
### TODO: general error checking

class Grid:

    def __init__(self, fname):
        '''
        A grid class for the lazor puzzle.

        **Attributes**
            fname: *str*
                The file name to read in
            grid: *np.array*
                Array of lazor grid, with 'o', 'x', and ' ' values
            block_dict: *dictionary*
                A dictionary of blocks. Keys are block types and values are the
                number of blocks
            laser_dict: *dictionary*
                A dictionary that contains the laser number and its corresponding
                integer x, y, vx, vy values as a tuple.
            point_dict: *dictionary*
                A dictionary that contains the goal point number and it's
                corresponding coordinates.
            
        **Parameters**

            fname: *str*
                The file name to read in
        '''
        self.fname=fname
        self.grid = self.get_grid()
        self.block_dict = self.get_blocks()
        self.laser_dict = self.get_laser_pos()
        self.point_dict = self.get_goal_points()

    def get_grid(self): 
        '''
        Get an array of grid elements.

        **Parameters**

            fname: *str*
                The file name to read in

        **Returns**

            grid: *array*
                An array of elements. o is an open spot, x is unavailable, and ' ' is between blocks
                spot.
        '''         
        infile = open(self.fname)
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


        num_cols = len(grid_list[0])
        num_rows = len(grid_list)

        # add space ' ' in between grid elements ('o' or 'x')
        grid = np.full((num_rows*2 + 1, num_cols*2 +1), ' ')
        for i, row in enumerate(grid_list):
            for j, ele in enumerate(row):
                grid[i*2+1, j*2+1] = ele

        return grid
    
    def get_blocks(self):
        '''
        Get a dictionary of block type and number.
        * elements are aliased as integers to save time
        * 0 = empty spot ('o')
        * 1 = reflective block ('A')
        * 2 = opaque block ('B')
        * 3 = refractive block ('C')
        

        **Parameters**

            fname: *str*
                The file name to read in

        **Returns**

            block_dict: *dictionary*
                A dictionary of blocks. Keys are block types and values are the
                number of blocks.
        '''  
        dict_A = {}
        dict_B = {}
        dict_C = {}
        start_search = False
        for line in open(self.fname):
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
    
    def get_laser_pos(self):
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
        infile = open(self.fname)
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
        
    def get_goal_points(self):
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
        infile = open(self.fname)
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

    def get_permutations(self,list_for_perm):
        '''
        Find all the permutations of the avaliable spots on the board

        **Parameters**

            list_for_perm: *list*
                The list of options for open spots

        **Returns**

            config_list: *list*
                A list containing all lists of permutations of the availabe spots.
        '''  
        config_list = []
        perm = idp(list_for_perm)
        config_list = list(perm)
        return config_list

        
    def get_configs(self):
        '''
        Find all the configurations of the available spots on the board
        * elements are aliased as integers to save time
        * 0 = empty spot ('o')
        * 1 = reflective block ('A')
        * 2 = opaque block ('B')
        * 3 = refractive block ('C')
        

        **Parameters**

            grid: *array*
                The grid of board elements
            blocks: *dict*
                A dictionary containing the types and number of blocks

        **Returns**

            config_list: *list*
                A list containing all lists of configurations of the availabe spots.
        '''  
        available = 0
        for x in self.grid:
            for y in x:
                if y == 'o':
                    available = available + 1

        block_types = []
        block_numbers = []
        for key, val in self.block_dict.items():
            block_types.append(key)
            block_numbers.append(val)

        blocks_sum = sum(block_numbers)

        open_spots = available - blocks_sum

        list_for_perm = []
        for i in range(open_spots):
            list_for_perm.append(int(0))

        for j in block_types:
            if j == 'reflective_blocks':
                for k in range(self.block_dict[j]):
                    list_for_perm.append(int(1))
            if j == 'opaque_blocks':
                for l in range(self.block_dict[j]):
                    list_for_perm.append(int(2))
            if j == 'refractive_blocks':
                for h in range(self.block_dict[j]):
                    list_for_perm.append(int(3))

        configs = self.get_permutations(list_for_perm)
        return configs
    
    def config_to_board(self, config): 
        '''
        Converts config to board/grid layout and converts elements to Block/Edge types. 

        **Parameters**

            config: *list*
                A list containing one configuration of the available spots.

        **Returns**

            boards: *np.array*
                An array containing the configuration on the grid
        ''' 
        board = np.empty(self.grid.shape, dtype=object)
        idx = 0
        for i, row in enumerate(self.grid):  #y
            for j, ele in enumerate(row): #x
                if ele == 'o':
                    block = Block(config[idx], j , i)
                    board = block.add_to_board(board)
                    idx += 1
        return board
    

    def get_laser_path(self, board, slow = False):
        '''
        Finds the path of the laser given a board configuration. 

        **Parameters**

            board: *np.array*
                An array containing block information. 

        **Returns**

            laser_path: *np.array*
                An array of the path the laser took based on block configuration. 0 for no laser, 1 for laser. 
        '''
        laser_path = np.zeros_like(self.grid, dtype=int)
        active_lasers = self.laser_dict.copy()
        positions = [] # list of all coords the laser hits  except for refracted ones
        if slow: 
            # for testing only
            print(self.board_to_int(board))
            for k in range(4):
                key, val = next(iter(active_lasers.items()))
            temp_path = np.zeros_like(self.grid, dtype = int)
            positions.append([val[0],val[1]]) # [x,y]
            vx, vy, = val[2], val[3]
            ref_positions = []

            if isinstance(key, float): #check if refractory block
                refracted_laser = active_lasers.pop(key) #x, y, vx, vy
                ref_active_lasers = {key:refracted_laser}
               
               
                ref_positions.append([refracted_laser[0],refracted_laser[1]])
                #print('ref block x, y', refracted_laser[0],refracted_laser[1])
                ref_vx, ref_vy = refracted_laser[2], refracted_laser[3]
                #print('old ref vx ,vy', ref_vx, ref_vy)
                #space = board[ref_positions[-1][1]][ref_positions[-1][0]]
                
                #print(space.value)
                while self.in_grid(ref_positions[-1]):
                    ref_origin = ref_positions[-1]
                    if isinstance(board[ref_positions[-1][1]][ref_positions[-1][0]], Edge):
                        ref_new_pos, ref_vx, ref_vy, ref_active_lasers = board[ref_positions[-1][1]][ref_positions[-1][0]].laser(ref_vx, ref_vy, ref_active_lasers) 
                        ref_positions.append(ref_new_pos)

                        
                        if self.in_grid(ref_new_pos):
                            ref_space = board[ref_new_pos[1]][ref_new_pos[0]]
                            if isinstance(ref_space, Edge):
                                print(ref_space.value)
                    else:
                        ref_positions.append([ref_origin[0]+ref_vx, ref_origin[1]+ref_vy])
                del ref_active_lasers[key]
        
            while self.in_grid(positions[-1]): 
                origin = positions[-1]
                # np arrays are arr[y][x]
               
                if isinstance(board[positions[-1][1]][positions[-1][0]], Edge):
                    new_pos, vx, vy, active_lasers = board[positions[-1][1]][positions[-1][0]].laser(vx, vy, active_lasers)
                    positions.append(new_pos)
                else:
                    positions.append([origin[0] + vx, origin[1] + vy])
            if key in active_lasers.keys():
                del active_lasers[key]
            else:
                pass

            for coord in positions:
                if self.in_grid(coord):
                    temp_path[coord[1]][coord[0]] = 1

            for coord in ref_positions:
                if self.in_grid(coord):
                    temp_path[coord[1]][coord[0]] = 1
            
            laser_path = laser_path + temp_path
            
        else:
            while len(active_lasers) != 0:
                key, val = next(iter(active_lasers.items()))
                temp_path = np.zeros_like(self.grid, dtype = int)
                positions.append([val[0],val[1]]) # [x,y]
                vx, vy, = val[2], val[3]
                ref_positions = []

                if isinstance(key, float): #check if refractory block
                    refracted_laser = active_lasers.pop(key) #x, y, vx, vy
                    ref_active_lasers = {key:refracted_laser}
                
                
                    ref_positions.append([refracted_laser[0],refracted_laser[1]])
                    #print('ref block x, y', refracted_laser[0],refracted_laser[1])
                    ref_vx, ref_vy = refracted_laser[2], refracted_laser[3]
                    #print('old ref vx ,vy', ref_vx, ref_vy)
                    #space = board[ref_positions[-1][1]][ref_positions[-1][0]]
                    
                    #print(space.value)
                    while self.in_grid(ref_positions[-1]):
                        ref_origin = ref_positions[-1]
                        if isinstance(board[ref_positions[-1][1]][ref_positions[-1][0]], Edge):
                            ref_new_pos, ref_vx, ref_vy, ref_active_lasers = board[ref_positions[-1][1]][ref_positions[-1][0]].laser(ref_vx, ref_vy, ref_active_lasers) 
                            ref_positions.append(ref_new_pos)

                            
                            if self.in_grid(ref_new_pos):
                                ref_space = board[ref_new_pos[1]][ref_new_pos[0]]
                                if isinstance(ref_space, Edge):
                                    print(ref_space.value)
                        else:
                            ref_positions.append([ref_origin[0]+ref_vx, ref_origin[1]+ref_vy])
                    del ref_active_lasers[key]
        
                while self.in_grid(positions[-1]): 
                    origin = positions[-1]
                    # np arrays are arr[y][x]
                
                    if isinstance(board[positions[-1][1]][positions[-1][0]], Edge):
                        new_pos, vx, vy, active_lasers = board[positions[-1][1]][positions[-1][0]].laser(vx, vy, active_lasers)
                        positions.append(new_pos)
                    else:
                        positions.append([origin[0] + vx, origin[1] + vy])
                if key in active_lasers.keys():
                    del active_lasers[key]
                else:
                    pass

            for coord in positions:
                if self.in_grid(coord):
                    temp_path[coord[1]][coord[0]] = 1

            for coord in ref_positions:
                if self.in_grid(coord):
                    temp_path[coord[1]][coord[0]] = 1
            
            laser_path = laser_path + temp_path
            return laser_path
    

    def in_grid(self, pos):
        '''
        Checks if position is inside the grid

        **Parameters**

            pos: *list*
                x and y position

        **Returns**

            *bool*
                True if in grid, False if outside.
        ''' 
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= len(self.grid[0]) or pos[1] >= len(self.grid):
            return False
        return True
    
    def board_to_int(self, board):
        '''
        Convert objects to ints for visability (internal only) 

        **Parameters**

            board: *np.array*
                An array containing block information. 

        **Returns**

            new_board: *np.array*
                An array that contains the edge/block type as ints instead of class objects. 
        '''
        new_board = np.empty(board.shape, dtype = object)
        for i,row in enumerate(board): 
            for j,val in enumerate(row): 
                if val != None:
                    new_board[i,j] = board[i,j].value
        return new_board

    def check_solution(self, laser_path):
        '''
        Checks board solution based on if the laser path intersects the goal points. 

        **Parameters**

            laser_path: *np.array*
                An array of the path the laser took based on block configuration. 0 for no laser, 1 for laser.

        **Returns**

            *bool*
                True if laser path hits contains all goal points, otherwise False
        '''
        for key, val in self.point_dict.items():
            if laser_path[val[1], val[0]] == 0:
                return False
        return True
    
    def find_solution(self, configs, slow = False):
        '''
        Checks all possible configs until a solution to the lazor puzzle is found. 

        **Parameters**

            configs: *list*
                A list containing all lists of configurations of the availabe spots.

        **Returns**

            *np.array*
                The board configuration that solves the puzzle. 
            laser_path: *np.array*
                The laser path of the solution
        '''
        for i, config in enumerate(configs):
            # if i %1000==0: print(f'Testing config #{i}') 
            board = self.config_to_board(config)
            laser_path = self.get_laser_path(board, slow)

            if self.check_solution(laser_path):
                print("SOLVED LAZOR!")
                print(config)
                return self.board_to_int(board), laser_path
        raise ValueError("No Solution Found")

if __name__ == "__main__":
    dir = os.getcwd()
    fnames = glob.glob(os.path.join(dir, "*.bff"))
    max_time = 0

    fname = 'tiny_5.bff'
    grid = Grid(fname)
    #print(grid.find_solution(grid.get_configs()))
    grid.find_solution(grid.get_configs(), slow=True)


