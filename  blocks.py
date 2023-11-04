import grid 

class Block:
    def __init__(self, block_type, x = -1, y = -1):
        
        self.block_type = block_type
        self.x = x
        self.y = y

    def laser(self, board, curr_pos, direction):
        """
        Sets current pos as laser present and performs change in direction based off the block type 

        Params: 
            board:  **dict**
                The dictionary board from find_configs
            curr_pos: **tuple**
                The coords of the current block (or no block)
            direction: **tuple**
                vx, vy of laser direction behavior

        Returns:
            board: **dict** 
                Updated board with current pos having the laser present
            direciton: **tuple**
                New direction depending on the block the laser hits
        """
        if self.block_type  == 0: #no block condition
            board[curr_pos][1] = 1 #list of block type sets laser present
            return board, direction # no change in direction for no blocks
        
        if self.block_type == 1: #Refelctive block condition
            
            board[curr_pos][1] = 1
            
            vx = direction[0]
            vy = direction[1]
            
            # Change laser direction, need to add interpretation of direction here
            vx *= -1 
            vy += -1

            direction = (vx,vy)

            return board, direction
        
        if self.block_type == 2:
            board[curr_pos][1] = 1
            vx = direction[0]
            vy = direction[1]
            vx = 0
            vy = 0
            direction = (vx, vy)
            return board, direction

        if self.block_type == 3:
            board[curr_pos][1] = 1 
            vx = direction[0]
            vy = direction[1]

            vx_1 = vx
            vy_1 = vy
            vx_2 = vx_1 * (-1)
            vy_2 = vy_1 * (-1)

            direction = (vx_1, vy_1, vx_2, vy_2)
            return board, direction




if __name__ == "__main__":
    board={(0, 0): [3, 0], (0, 1): ['B', 0], (0, 2): [1, 0], (1, 0): [1, 0], (1, 1): [0, 0], (1, 2): [1, 0], (2, 0): [0, 0], (2, 1): [0, 0], (2, 2): [0, 0]}, {(0, 0): [3, 0], (0, 1): ['B', 0], (0, 2): [1, 0], (1, 0): [1, 0], (1, 1): [1, 0], (1, 2): [0, 0], (2, 0): [0, 0], (2, 1): [0, 0], (2, 2): [0, 0]}
    test = Block()