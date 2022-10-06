import pygame as p
from maze_generator import make_maze
from pathfinding import a_star,dfs,bfs,dijkstra,greedy

ROWS = 50 # grid dimensions, must change in pathfinding file too (only thing I could figure out to avoid circular import error) 
          # can make as large as desired

WIDTH = 800 # size of main grid window # can make as large as desired
SIDEBAR = 155 # size of sidebar (if smaller, text in buttons may go off screen)
WIN = p.display.set_mode((WIDTH+SIDEBAR,WIDTH))
p.display.set_caption("Path Finding Visualization")
p.init()
FONT = p.font.SysFont("Arial", 20, True, False)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = p.Color("White")
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == p.Color("Red")
    
    def is_open(self):
        return self.color == p.Color("Green")
    
    def is_barrier(self):
        return self.color == p.Color("Black")
    
    def is_start(self):
        return self.color == p.Color("Orange")
    
    def is_end(self):
        return self.color == p.Color("light blue")
    
    def is_path(self):
        return self.color == p.Color("Purple")
    
    def is_empty(self):
        return self.color == p.Color("white")
    
    
    
    def reset(self):
        self.color = p.Color("White")
        
    def make_closed(self):
        self.color = p.Color("Red")
        
    def make_open(self):
        self.color = p.Color("green")
    
    def make_barrier(self):
        self.color = p.Color("Black")
        
    def make_start(self):
        self.color = p.Color("Orange")
        
    def make_end(self):
        self.color = p.Color("light blue")
    
    def make_path(self):
        self.color = p.Color("Purple")
        
    
    def draw(self, win):
        p.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # check down
            self.neighbors.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # check up
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): # check right
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col -1].is_barrier(): # check left
            self.neighbors.append(grid[self.row][self.col-1])        
        
        
    
    def __lt__(self,other):
        return False
    
    



def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i,j,gap,rows)
            grid[i].append(spot)
            
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    # drawing lines on grid
    for i in range(rows):
        p.draw.line(win,p.Color("Grey"),(0,i*gap),(width,i*gap))
        for j in range(rows+1):
            p.draw.line(win,p.Color("Grey"),(j*gap,0),(j*gap,width))

def draw_buttons(win, list): # drawing buttons on sidebar
    for i in range(len(list)):
        p.draw.line(win,p.Color("black"),(WIDTH,i*(WIDTH//len(list))),(WIDTH+SIDEBAR,i*(WIDTH//len(list))),width=10)
        if list[i][1]: # if that option is selected, make it yellow
            p.draw.rect(win,p.Color("yellow"),(WIDTH,i*WIDTH//len(list),SIDEBAR,WIDTH//len(list))) # if the button is active, make it yellow
        else:
            if i < len(list)-3:
                p.draw.rect(win,p.Color("blue"),(WIDTH,i*WIDTH//len(list),SIDEBAR,WIDTH//len(list))) # make all other buttons blue
            else:
                p.draw.rect(win,p.Color("dark green"),(WIDTH,i*WIDTH//len(list),SIDEBAR,WIDTH//len(list))) # make bottom 3 buttons green
            
        text_object = FONT.render(list[i][0],0,p.Color("Black"))  
        text_location = p.Rect(WIDTH,i*WIDTH//len(list),SIDEBAR,WIDTH//len(list)).move(0,(WIDTH//len(list))/3)
        win.blit(text_object, text_location)
            
def draw_screen(win, grid, rows, width,list): # bring drawing functions together
    win.fill(p.Color("white"))
    
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win,rows, width)
    draw_buttons(win,list)
    p.display.update()
    
def get_clicked_pos(pos,rows,width): # get the position of a click
    gap= width // rows
    y,x = pos
    
    row = y // gap
    col = x // gap
    return row,col

def main(win, width, ROWS):
    
    
    
    grid = make_grid(ROWS, width)
    
    start = None
    end = None

    maze = False
    slow = False
    
    pathfind = "astar" # default pathfinding algorithm
    change = False
    selected = [["DFS",False],["BFS",False],["Dijkstra",False],["Greedy",False],["A Star",True],["Visualize Algorithm",False],["Run Algorithm",False],["Build Maze",False],["Clear",False]]
    
    
    run = True
    started = False
    
    
    while run:
        draw_screen(win,grid,ROWS,width,selected)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
                
            
            
            if p.mouse.get_pressed()[0]: # left mouse button
                pos = p.mouse.get_pos() 
                row,col = get_clicked_pos(pos,ROWS,width)
                if pos[0] <= WIDTH: # inside the grid
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    
                    elif spot != end and spot != start:
                        spot.make_barrier()
                else: # options on side
                    selected[pos[1]//(WIDTH//len(selected))][1] = not selected[pos[1]//(WIDTH//len(selected))][1]
                    
                
                
                
            elif p.mouse.get_pressed()[2]: # right mouse button
                pos = p.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                if row < ROWS:
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None
                    



        
        for i in range(len(selected)): # handling inputs from buttons on side
            
            # select whether or not to show step by step of algorithms
            if selected[i][0] == "Visualize Algorithm": 
                if selected[i][1]:
                    slow = True
                else: slow = False
            
            # clear the board
            if selected[i][0] == "Clear":
                if selected[i][1]:
                    if started: # first after running, remove the pathfinding
                        started = False
                        for row in grid:
                            for spot in row:
                                if spot.is_open() or spot.is_closed() or spot.is_path(): # remove all the pathfinding visualizations
                                    spot.reset()
                        selected[i][1] = False
                    else:
                        start = None # otherwise, remove everything
                        end = None
                        grid = make_grid(ROWS,WIDTH)
                        maze = False
                        selected[i][1] = False
            
            # run the pathfinding algorithm
            if selected[i][0] == "Run Algorithm":
                if selected[i][1] and not started and start and end:
                    started = True
                    
                    if pathfind == "astar": # run a* algorithm
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        
                        a_star(lambda: draw_screen(win,grid,ROWS,width,selected),grid, start,end,slow)
                        
                    
                    elif pathfind == "dfs": # run Depth Search First algorithm
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        dfs(lambda: draw_screen(win,grid,ROWS,width,selected),grid, start,end,slow)
                    
                    elif pathfind == "bfs": # run breadth Search First algorithm
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        bfs(lambda: draw_screen(win,grid,ROWS,width,selected),grid, start,end,slow)

                    elif pathfind == "dijkstra": # run Dijkstra algorithm
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        dijkstra(lambda: draw_screen(win,grid,ROWS,width,selected),grid, start,end,slow)
                    
                    elif pathfind == "greedy": # run greedy algorithm
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        greedy(lambda: draw_screen(win,grid,ROWS,width,selected),grid, start,end,slow)
                        
                else:
                    selected[i][1] = False
            
            
            # select which pathfinding algorithm
            if selected[i][0] == "A Star":
                if selected[i][1] and not change:
                    if pathfind != "astar":
                        change = True
                        pathfind = "astar"
                
            if selected[i][0] == "DFS":
                if selected[i][1] and not change:
                    if pathfind !="dfs":
                        change = True
                        pathfind = "dfs"
            
            if selected[i][0] == "BFS":
                if selected[i][1] and not change:
                    if pathfind !="bfs":
                        change = True
                        pathfind = "bfs"
            
            if selected[i][0] == "Dijkstra":
                if selected[i][1] and not change:
                    if pathfind !="dijkstra":
                        change = True
                        pathfind = "dijkstra"
            
            if selected[i][0] == "Greedy":
                if selected[i][1] and not change:
                    if pathfind !="greedy":
                        change = True
                        pathfind = "greedy"
            
            
            # build the maze
            if selected[i][0] == "Build Maze":
                if selected[i][1] and not maze and not started:
                    print(selected[i])
                    maze = True
                    start = None 
                    end = None
                    grid = make_grid(ROWS,WIDTH)
                    maze = make_maze(lambda: draw_screen(win,grid,ROWS,width,selected),grid,ROWS,slow)
                    for j in range(ROWS):
                        for k in range(ROWS):
                            if maze[j][k] == 'w':
                                grid[j][k].make_barrier()
                    
                    selected[i][1] = False
        
        # update the button visual
        if pathfind != "dfs" and change:
            selected[0][1] = False
        if pathfind != "bfs" and change:
            selected[1][1] = False    
        if pathfind != "dijkstra" and change:
            selected[2][1] = False   
        if pathfind != "greedy" and change:
            selected[3][1] = False  
        if pathfind != "astar" and change: 
            selected[4][1] = False 
        

        change = False

    p.quit()

if __name__ == "__main__":
    main(WIN,WIDTH, ROWS)
