'''
Find all possible configurations of the board
'''
from more_itertools import distinct_permutations as idp
from Read_in_bff_file import get_grid
from Read_in_bff_file import get_blocks

def get_permutations(list_for_perm):
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

def get_configs(grid, blocks):
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
    for x in grid:
        for y in x:
            if y == 'o':
                available = available + 1

    block_types = []
    block_numbers = []
    for i in blocks:
        block_types.append(i)
        block_numbers.append(blocks[i])

    blocks_sum = 0
    for num in block_numbers:
        blocks_sum = blocks_sum + num

    open_spots = available - blocks_sum
    list_for_perm = []
    for i in range(open_spots):
        list_for_perm.append(int(0))

    for j in block_types:
        if j == 'reflective_blocks':
            for k in range(blocks[j]):
                list_for_perm.append(int(1))
        if j == 'opaque_blocks':
            for l in range(blocks[j]):
                list_for_perm.append(int(2))
        if j == 'refractive_blocks':
            for h in range(blocks[j]):
                list_for_perm.append(int(3))

    configs = get_permutations(list_for_perm)
    return configs


def get_boards(grid, configs):
    '''
    Find all the configurations of the available spots on the board

    **Parameters**

        grid: *array*
            The grid of board elements
        configs: *list*
            A list containing all lists of configurations of the availabe spots.

    **Returns**

        boards: *list*
            A list containing all lists of configurations of the board.
    '''  
    list_of_board = []
    boards = []

    for row in grid:
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


def board_dictionary(grid, boards):
    '''
    Convert all board configurations to dictionaries of coordinates

    **Parameters**

        grid: *array*
            The grid of board elements
        boards: *list*
            A list containing all lists of configurations of the board.

    **Returns**

        board_dictionary: *dict*
            A dictionary where the keys are x, y coordinates and the values
            are the board elements
    '''  
    board_dim_x = grid.shape[0]
    board_dim_y = grid.shape[1]
    x_vals = []
    y_vals = []
    for i in range(board_dim_x):
        x_vals.append(i)
    for j in range(board_dim_y):
        y_vals.append(j)
        
    coordinates = []
    for i in range(len(x_vals)):
        for j in range(len(y_vals)):
            coordinates.append((x_vals[i], y_vals[j]))
    board_dictionary = []
    for board in boards:
        board_dictionary.append(dict(zip(coordinates, board)))
    
    return board_dictionary

def board_coordinates(board_dictionary):
    '''
    Changes the dimensions of the board_dictionary to translate to a grid.
    The board_dictionary does not account for step size. 
    
    For example, an element of a dictionary from board_dictionary could be 
    (0,0): B, where (0,0) is the location of the B block

    However, step size is by half blocks so the block dimension will actually
    be 2 x 2. Therefore, this will yeild 9 coordinates such that
    (0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)): 
    B
    
    where all 9 coordinates have the B value.

    **Parameters**

        board_dictionary: *dict*
            A dictionary where the keys are x, y coordinates and the values
            are the board elements

    **Returns**

        board_coordinates: *list*
            A list of dictionaries where the keys are x, y coordinates and the values
            are the board elements
    '''  
    board_coordinates = []
    for board in board_dictionary:

        block_coordinates = []
        for i in board:
            block_coordinates.append(i)
        board_dictionary = {}
        for block in block_coordinates:
            block = block
            element = board.get(block)
            new_block_x = block[0] * 2
            new_block_y = block[1] * 2
            new_x_list = []
            new_y_list = []
            range_of_block = 3
            for i in range(range_of_block):
                new_x_list.append(new_block_x + i)
                new_y_list.append(new_block_y + i)
            coordinates = []
            for i in range(len(new_y_list)):
                for j in range(len(new_x_list)):
                    coordinates.append((new_x_list[j], new_y_list[i]))
            coord_tup = tuple(coordinates)
            
            board_dictionary[coord_tup] = element
        board_coordinates.append(board_dictionary)
    
    
    return board_coordinates


if __name__ == "__main__":
    grid = get_grid('tiny_5.bff')
    blocks = get_blocks('tiny_5.bff')
    config = get_config(grid, blocks)
    boards = get_boards(grid, configs)
    board_dictionary = board_dictionary(grid, boards)
    board_coordinates = board_coordinates(board_dictionary)
