
class Edge: 
    def __init__(self, block_type, edge_side, edge_pos):
        """
        An Edge class that can interpret how blocks change laser direction.

        **Attributes**
            value:  **int**
                Block type coded to int
            side: **tuple**
                edge size (-1,0) for left, (1,0) for right, (0,-1) for bottom, (0,1) for top
            pos: **tuple**
                edge position in grid (x,y)
        """
        self.value = block_type
        self.side = edge_side
        self.pos = edge_pos
    
    def hit_edge(self, vx, vy):
        """
        Checks if laser is pointed to the edge or is starting from that position. 

        **Parameters**
            vx: **int**
                X laser direction
            vy: **int**
                Y laser direction

        **Returns**
            *bool*
                True if laser is pointing towards edge, false otherwise
        """
        if vx*-1 == self.side[0] or vy*-1 == self.side[1]:
            return True
        return False
    
    def laser(self, vx, vy, active_lasers):
        """
        Sets current pos as laser present and performs change in direction based off the block type 

        **Parameters**
            vx: **int**
                X laser direction
            vy: **int**
                Y laser direction
            active_lasers: **dict**
                Dictionary of active lasers that haven't hit edge of grid yet. Values are x,y,vx,vy
            temp_path: **np.array**
                An array of the current laser path

        Returns:
            new_pos: **tuple** 
                Laser position in grid (x,y)
            vx: **int**
                X laser direction
            vy: **int**
                Y laser direction
            active_lasers: **dict**
                Dictionary of active lasers that haven't hit edge of grid yet. Values are x,y,vx,vy
        """
        def no_change():
            # returns new_pos, vx, vy, and active_lasers if no special block is encountered
            new_pos[0] = self.pos[0] + vx
            new_pos[1] = self.pos[1] + vy
            return new_pos, vx, vy, active_lasers # no change in direction for no blocks
        new_pos = [-1,-1]
        if self.value  == 0: #no block condition
            return no_change() # no change in direction for no blocks
        
        if self.value == 1: #Refelctive block condition
            if self.hit_edge(vx, vy):
                if abs(self.side[0]) == 1: #if left or right edge, vx direction filps
                    vx = vx*-1
                if abs(self.side[1]) == 1: #if top or bottom edge, vy direction filps
                    vy = vy*-1 
                
                new_pos[0] = self.pos[0] + vx
                new_pos[1] = self.pos[1] + vy
                return new_pos, vx, vy, active_lasers
            else:
                return no_change()
        
        if self.value == 2: #opaque block
            if self.hit_edge(vx, vy):
                return (-1,-1), 0, 0, active_lasers
            else: 
                return no_change()

        if self.value == 3:
            if self.hit_edge(vx, vy):
                active_lasers[max(active_lasers.keys())+1] = (self.pos[0] + vx, self.pos[1] + vy, vx, vy)

                if abs(self.side[0]) == 1: #if left or right edge, vx direction filps
                    vx = vx*-1
                if abs(self.side[1]) == 1: #if top or bottom edge, vy direction filps
                    vy = vy*-1 
                
                new_pos[0] = self.pos[0] + vx
                new_pos[1] = self.pos[1] + vy

                return new_pos, vx, vy, active_lasers
            else: 
                return no_change()

class Block:
    def __init__(self, block_type, x = -1, y = -1):
        """
        A Blcck class that has edges that can be hit by laser.

        **Attributes**
            value:  **int**
                Block type coded to int
            x: **int**
                x position
            y: **int**
                y position
            edges: **list**
                List of four Edge classes
        """
        self.value = block_type
        self.x = x
        self.y = y
        self.edges = self.get_edges()
    
    def add_to_board(self, board):
        """
        Adds Edges to board configuration 

        **Parameters**
            board: **np.array**
                Current board configuration

        **Returns**
            board: **np.array**
                New board configuration with edges added
        """
        if self.value != 0:
            for edge in self.edges: 
                # np arrays are arr[y][x]
                board[edge.pos[1]][edge.pos[0]] = edge
        return board
        
    def get_edges(self):
        """
        Creates edges for Block

        **Returns**
            edges: **list**
                List of four Edge classes for the sides of the Block
        """
        edges_pos = [(-1,0),(1,0),(0,-1),(0,1)]
        edges = []
        for edge in edges_pos: 
            edge_pos = (self.x + edge[0],self.y + edge[1])
            edges.append(Edge(self.value, edge, edge_pos))
        return edges
        
            
        