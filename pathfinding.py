import math
from queue import PriorityQueue
import pygame as p

ROWS = 50 # grid dimensions, must change in main file too (only thing I could figure out to avoid circular import error) 

def h(p1,p2): # heuristic function to calculate distance
    #(row,col)
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from,start, end, draw,slow):
    current = came_from[end]
    current.make_path()
    if slow:
        draw()
    while current in came_from: # goes back through all the came froms and draws the shortest path
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
                
        current = came_from[current]
        if current == start:
            return True
        current.make_path()
        if slow:
            draw()
    if not slow:
        draw()

def a_star(draw,grid,start,end,slow):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from = {}
    # g score is shortest distance from node to start node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    #f score is estimated distance from node to end node using heuristic (manhattan distance)
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from,start,end,draw,slow) # make path
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]: # update path for neighbors if needed
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score 
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos()) 
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        if slow:
            draw()
        
        if current != start:
            current.make_closed()
    return False
                
def dfs(draw,grid,start,end,slow):
    open_list = []
    closed_list = []
    open_list.append(start)
    came_from = {}
    
    while len(open_list) > 0:
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
        
        current = open_list[0] # start with newest index in list
        open_list.remove(current)
        
        if current == end:
            reconstruct_path(came_from,start,end,draw,slow) # make path
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in open_list and neighbor not in closed_list and neighbor.row >= 0 and neighbor.row < ROWS and neighbor.col >= 0 and neighbor.col < ROWS:
                came_from[neighbor] = current
                open_list.insert(0,neighbor) # insert at front of list
                neighbor.make_open()
        
        
        start.make_start()
        end.make_end()
        if current != start:
            current.make_closed()
            closed_list.append(current)
        
        if slow:
            draw()
        
    return False

def bfs(draw,grid,start,end,slow):
    open_list = []
    closed_list = []
    open_list.append(start)
    came_from = {}
    
    while len(open_list) > 0:
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
        
        current = open_list[-1] # start with oldest index in list
        open_list.remove(current)
        
        if current == end:
            reconstruct_path(came_from,start,end,draw,slow) # make path
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            # a bunch of conditions to make sure we are looking at valid cells
            if neighbor not in open_list and neighbor not in closed_list and neighbor.row >= 0 and neighbor.row < ROWS and neighbor.col >= 0 and neighbor.col < ROWS:
                came_from[neighbor] = current
                open_list.insert(0,neighbor) # insert at front of list
                neighbor.make_open()
        
        
        start.make_start()
        end.make_end()
        if current != start:
            current.make_closed()
            closed_list.append(current)
        
        if slow:
            draw()
        
    return False
        
        
def dijkstra(draw,grid,start,end,slow):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from = {}
    # g score is shortest distance from node to start node
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from,start,end,draw,slow) # make path
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]: # update path for neighbors if needed
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score 
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        start.make_start()
        end.make_end()
        if slow:
            draw()
        
        if current != start:
            current.make_closed()
    return False

def greedy(draw,grid,start,end,slow):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    closed_list = []
    came_from = {}
    #f score is estimated distance from node to end node using heuristic (manhattan distance)
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        
        for event in p.event.get():
            if event.type == p.QUIT: # allow user to quit
                p.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from,start,end,draw,slow) # make path
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            f_score[neighbor] = h(neighbor.get_pos(),end.get_pos()) 
            if neighbor not in open_set_hash and neighbor not in closed_list:
                came_from[neighbor] = current
                count += 1
                open_set.put((f_score[neighbor],count,neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_open()
        
        if current != start:
            current.make_closed()
            closed_list.append(current)
        start.make_start()
        end.make_end()
        
        if slow:
            draw()
        
        
            
    return False
