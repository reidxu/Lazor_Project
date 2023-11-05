
class Edge: 
    def __init__(self, edge_type, edge_side, edge_pos):
        self.type = edge_type
        self.side = edge_side
        self.pos = edge_pos
    
    def laser(self, board, vx, vy):
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
        new_pos = (-1,-1)
        if self.block_type  == 0: #no block condition
            new_pos[0] = self.x + vx
            new_pos[1] = self.y + vy
            return new_pos, vx, vy # no change in direction for no blocks
        
        if self.block_type == 1: #Refelctive block condition
            
                       
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

class Block:
    def __init__(self, block_type, x = -1, y = -1):
        self.block_type = block_type
        self.x = x
        self.y = y
        self.edges = self.get_edges()
    
    def add_to_board(self, board):
        for edge in self.edges: 
            board[edge.pos[0],edge.pos[1]] = self.block_type
        return board

    
    def get_edges(self):
        edges_pos = [(-1,0),(1,0),(0,-1),(0,1)]
        edges = []
        for edge in edges_pos: 
            edge_pos = (self.x + edge[0],self.y + edge[1])
            edges.append(Edge(self.block_type, edge, edge_pos))
        return edges
        
            
        