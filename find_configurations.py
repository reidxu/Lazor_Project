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


if __name__ == "__main__":
    grid = get_grid('tiny_5.bff')
    blocks = get_blocks('tiny_5.bff')
    config = get_config(grid, blocks)
    boards = get_boards(grid, configs)
