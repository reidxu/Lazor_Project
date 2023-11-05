'''
Read in and extract all relevant data from bff file
'''
    
import numpy as np   
from more_itertools import distinct_permutations as idp
from blocks import Block

### TODO: Add check to make sure laser direction abs(slope) = 1
### TODO: Can you add two blocks next to eachother??
class Grid:

    def __init__(self, fname):

        self.fname=fname
        self.grid = self.get_grid()
        self.solved_grid = self.grid.copy()
        self.block_dict = self.get_blocks()
        self.laser_dict = self.get_laser_pos()

    
    def load_blocks(self):
        '''
        Get an array of grid elements.

        **Parameters**

            fname: *str*
                The file name to read in

        **Returns**

            blocks: *list*
                An list of Block classes.
        '''
        block_dict = self.get_blocks()
        blocks = []
        for block, num in block_dict.items():
            for i in range(num):
                blocks.append(Block(block))
        return blocks



    def get_grid(self): 
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
        grid = np.full((num_cols*2 + 1, num_rows*2 +1), ' ')
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
        Converts config to board/grid layout. 

        **Parameters**

            config: *list*
                A list containing one configuration of the available spots.

        **Returns**

            boards: *np.array*
                An array containing the configuration on the grid
        ''' 
        board = self.grid.copy()
        idx = 0
        for i, row in enumerate(board): 
            for j, ele in enumerate(row):
                if ele == 'o':
                    block = Block(config[idx], i , j)
                    board = block.add_to_board(board)
                    idx += 1
        return board
    

    def get_laser_path(self, board):
        '''
        '''
        laser_path = np.zeros_like(self.grid)
        for laser, val in self.laser_dict.items():
            laser_path = np.zeros_like(self.grid)
            pos = (val[0],val[1])
            vx, vy, = val[2], val[3]
            while self.in_grid(pos):
                laser_path[val[0],val[1]] = 1
                if isinstance(board[pos[0]][pos[1]], Block):
                    pos, vx, vy = board[pos[0]][pos[1]].laser(vx, vy)
                else:
                    pos[0] = pos[0] + vx
                    pos[1] = pos[1] + vy
        return
    

    def in_grid(self, pos):
        '''
        Checks if position is inside the grid

        **Parameters**

            pos: *list*
                x and y position

        **Returns**

            bool
                True if in grid, False if outside.
        ''' 
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= len(self.grid) or pos[1] >= len(self.grid[0]):
            return False


    def get_boards(self):
        '''
        Find all the configurations of the available spots on the board

        **Parameters**

            grid: *array*
                The grid of board elements
            configs: *list*
                A list containing all lists of configurations of the available spots.

        **Returns**

            boards: *list*
                A list containing all lists of configurations of the board.
        '''  
        configs =self.get_configs()
        list_of_board = []
        boards = []
        
        for row in self.grid:
            for element in row:
                list_of_board.append(element)
        
        for config in configs:
            count = 0
            new = []
            for entry in list_of_board:
                if entry == 'o':
                    new.append(config[count])
                    count = count + 1
                else:
                    new.append(entry)

            boards.append(new)
        return boards

    def board_dictionary(self):
        '''
        Convert all board configurations to dictionaries of coordinates

        **Parameters**

            grid: *array*
                The grid of board elements
            boards: *list*
                A list containing all lists of configurations of the board.

        **Returns**

            board_dictionary: *list*
                A list of dictionaries where
                each dictionary has the keys are x, y coordinates and the values
                are the board elements and if laser is present
                
                * 0 = empty spot ('o')
                * 1 = reflective block ('A')
                * 2 = opaque block ('B')
                * 3 = refractive block ('C')

                * 0 = laser not present
                * 1 = laser present

                Example board dictionary: 
                {(x,y):  [0,1]} This means at the coord (x,y), it is empty and laser present.
        
        '''  
        boards = self.get_configs()
        board_dim_x = self.grid.shape[0]
        board_dim_y = self.grid.shape[1]
        x_vals = []
        y_vals = []

        for i in range(board_dim_x):
            x_vals.append(i)
        for j in range(board_dim_y):
            y_vals.append(j)
            
        coordinates = []
        for i in range(len(y_vals)):
            for j in range(len(x_vals)):
                coordinates.append((x_vals[j], y_vals[i]))
        board_dictionary = []
        for board in boards:
            board_dictionary.append(dict(zip(coordinates, board)))
        for dictionary in board_dictionary:

            for coord in dictionary:
        
                dictionary[coord] = [dictionary[coord], 0]
        return board_dictionary
    
if __name__ == "__main__":
    fname = 'mad_1.bff'
    grid = Grid(fname)
    print(grid.grid)
    print(grid.block_dict)
    print(grid.get_configs()[0])
    print(grid.config_to_board(grid.get_configs()[0]))
    print(grid.laser_dict)
