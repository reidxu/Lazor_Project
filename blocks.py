
class Edge: 
    def __init__(self, block_type, edge_side, edge_pos):
        self.value = block_type
        self.side = edge_side
        self.pos = edge_pos
    
    def hit_edge(self, vx, vy):
        if vx*-1 == self.side[0] or vy*-1 == self.side[1]:
            return True
        return False
    
    def laser(self, vx, vy, active_lasers, temp_path):
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
        def no_change():
            temp_path[self.pos[1]][self.pos[0]] = 1
            new_pos[0] = self.pos[0] + vx
            new_pos[1] = self.pos[1] + vy
            return new_pos, vx, vy, active_lasers # no change in direction for no blocks
        new_pos = [-1,-1]
        if self.value  == 0: #no block condition
            return no_change() # no change in direction for no blocks
        
        if self.value == 1: #Refelctive block condition
            if self.hit_edge(vx, vy):
                temp_path[self.pos[1]][self.pos[0]] = 1
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
                temp_path[self.pos[1]][self.pos[0]] = 1
                return (-1,-1), 0, 0, active_lasers
            else: 
                return no_change()

        if self.value == 3:
            if self.hit_edge(vx, vy):
                temp_path[self.pos[1]][self.pos[0]] = 1
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
        self.value = block_type
        self.x = x
        self.y = y
        self.edges = self.get_edges()
    
    def add_to_board(self, board):
        if self.value != 0:
            for edge in self.edges: 
                # np arrays are arr[y][x]
                board[edge.pos[1]][edge.pos[0]] = edge
        return board
    


    
    def get_edges(self):
        edges_pos = [(-1,0),(1,0),(0,-1),(0,1)]
        edges = []
        for edge in edges_pos: 
            edge_pos = (self.x + edge[0],self.y + edge[1])
            edges.append(Edge(self.value, edge, edge_pos))
        return edges
        
            
        