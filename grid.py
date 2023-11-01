'''
Read in and extract all relevant data from bff file
'''
        
import numpy as np   
from blocks import Block

class Grid():

    def __init__(self, fname):
        self.grid = self.get_grid(fname)
        self.blocks = self.load_blocks(fname)
    
    def load_blocks(self, fname):
        '''
        Get an array of grid elements.

        **Parameters**

            fname: *str*
                The file name to read in

        **Returns**

            blocks: *list*
                An list of Block classes.
        '''
        block_dict = self.get_blocks(fname)
        print(block_dict)
        blocks = []
        for block, num in block_dict.items():
            for i in range(num):
                blocks.append(Block(block))
        return blocks



    def get_grid(self, fname): 
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
    
    def get_blocks(self, fname):
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

if __name__ == "__main__":
    fname = 'mad_1.bff'
    grid = Grid(fname)
    print(grid.grid)
    for block in grid.blocks:
        print(block.block_type)
    print(grid.grid[2][2])