'''
Find all possible configurations of the board
'''
from itertools import permutations
from Read_in_bff_file import get_grid
from Read_in_bff_file import get_blocks

def get_permutations(list_for_perm):
    config_list = []
    for p in permutations(list_for_perm):
        if p not in config_list:
            config_list.append(p)
        else:
            continue
    return config_list


def get_config(grid, blocks):
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
        list_for_perm.append('o')
    for j in block_types:
        if j == 'reflective_blocks':
            for k in range(blocks[j]):
                list_for_perm.append('A')
        if j == 'opaque_blocks':
            for l in range(blocks[j]):
                list_for_perm.append('B')
        if j == 'refractive_blocks':
            for h in range(blocks[j]):
                list_for_perm.append('C')

    return get_permutations(list_for_perm)


def get_boards(grid, configs):
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
