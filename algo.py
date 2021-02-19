from queue import PriorityQueue
import math
import Node
import random
from collections.abc import Iterable

DATA = []


class Data:
    def __init__(self):
        self.path = 0
        self.explored = 0
        self.graph_type = ""


class Queue:

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


class StackFringe:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def pop(self):
        return self.stack.pop()

    def push(self, loc):
        if loc in self.stack:
            return
        else:
            return self.stack.append(loc)


# return a list of path nodes
def reconstruct_path(came_from, current, draw):
    path = []
    cnt = 0
    while current in came_from:
        cnt += 1
        current = came_from[current]
        # print("printing:" + '[' + str(current.row) + ']' + ' [' + str(current.col) + ']')
        current.set_path()
        path.append(current.get_pos())
        draw()
        # print(cnt)
    # print(path)
    return path


def DFS(draw, grid, start, dim):
    my_data = Data()
    visited = set()
    # stack = [start]
    stack = StackFringe()
    stack.push(start)
    came_from = {}
    while not stack.is_empty():
        node = stack.pop()
        # node.set_color()
        # print("exploring:" + '[' + str(node.row) + ']' + ' [' + str(node.col) + ']')
        if node.row == dim - 1 and node.col == dim - 1:
            # print(len(came_from))
            path = reconstruct_path(came_from, node, draw)
            my_data.graph_type = "DFS"
            my_data.path = len(path)
            my_data.explored = len(visited)
            DATA.append([my_data.graph_type, my_data.path, my_data.explored])

            print(str(len(path)) + " in path")
            print(str(len(visited)) + " explored")
            return True

        if node not in visited:
            visited.add(node)
            node.set_explored()

        for neighbor in node.neighbors:
            if neighbor not in visited:
                stack.push(neighbor)
                came_from[neighbor] = node
    draw()
    print(str(len(visited) - 1) + " explored")

    my_data.graph_type = "DFS"
    my_data.path = 0 - 1
    my_data.explored = len(visited) - 1
    DATA.append([my_data.graph_type, my_data.path, my_data.explored])

    return False


def BFS(draw, grid, start, dim):
    my_data = Data()
    queue = Queue()
    visited = set()
    queue.enqueue(start)
    visited.add(start)

    came_from = {}
    cnt = 0
    while queue.size() > 0:
        curr = queue.dequeue()
        cnt += 1
        # print(cnt)
        # print('[' + str(curr.row) + ']' + ' [' + str(curr.col) + ']' + ' ' + str(curr.color))
        if curr.row == dim - 1 and curr.col == dim - 1:
            path = reconstruct_path(came_from, curr, draw)

            my_data.graph_type = "BFS"
            my_data.path = len(path)
            my_data.explored = len(visited)
            DATA.append([my_data.graph_type, my_data.path, my_data.explored])

            print(str(len(path)) + " in path")
            print(str(len(visited)) + " explored")
            return True

        for neighbor in curr.neighbors:
            if neighbor not in visited:
                neighbor.set_explored()
                visited.add(neighbor)
                queue.enqueue(neighbor)
                came_from[neighbor] = curr

    draw()
    print(str(len(visited) - 1) + " explored")

    my_data.graph_type = "BFS"
    my_data.path = 0
    my_data.explored = len(visited) - 1
    DATA.append([my_data.graph_type, my_data.path, my_data.explored])

    return False


def heuristic(start, end):
    euclidean_distance = math.sqrt((start.row - end.row) ** 2 + (start.col - end.col) ** 2)
    return euclidean_distance


def astar(draw, grid, start, dim, target):
    my_data = Data()
    came_from = {}
    closed_list = []
    open_list = PriorityQueue()
    open_list.put((0, start))
    g_score = {Node: float("inf") for row in grid for Node in row}
    g_score[start] = 0
    f_score = {Node: float("inf") for row in grid for Node in row}
    f_score[start] = heuristic(start, target)
    while not open_list.empty():
        curr = open_list.get()[1]
        curr.set_explored()
        if curr == target:
            path = reconstruct_path(came_from, curr, draw)
            my_data.graph_type = "Astar"
            my_data.path = len(path)
            my_data.explored = len(closed_list)
            DATA.append([my_data.graph_type, my_data.path, my_data.explored])

            print(str(len(path)) + " in path")
            print(str(len(closed_list)) + " explored")
            return True

        for neighbor in curr.neighbors:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, target)
                if neighbor not in closed_list:
                    open_list.put((f_score[neighbor], neighbor))
                    closed_list.append(neighbor)
        draw()
        if curr != start:
            curr.set_closed()

    print(str(len(closed_list)) + " explored")

    my_data.graph_type = "Astar"
    my_data.path = 0
    my_data.explored = len(closed_list)
    DATA.append([my_data.graph_type, my_data.path, my_data.explored])

    return False


def agent_astar(start, grid, target, strat):
    came_from = {}
    closed_list = []
    open_list = PriorityQueue()
    open_list.put((0, start))
    g_score = {Node: float("inf") for row in grid for Node in row}
    g_score[start] = 0
    f_score = {Node: float("inf") for row in grid for Node in row}
    f_score[start] = heuristic(start, target)
    while not open_list.empty():
        curr = open_list.get()[1]
        # print('[' + str(curr.row) + ']' + ' [' + str(curr.col) + ']' + ' ' + str(curr.state))
        # curr.set_explored()
        if curr == target:
            path = agent_path(came_from, curr)
            if strat == 1:
                return path
            if strat == 2:
                step = []
                # print(path)
                if (len(path) >= 2):
                    step.append(path[-2])
                else:
                    step.append((len(grid) - 1, len(grid) - 1))
                return step
        for neighbor in curr.neighbors:
            # print('THIS IS current ['+str(curr.row) + ']' + ' [' + str(curr.col) + ']' + ' ' + str(curr.state))
            # print('THIS IS THE NEIGHBOR[' + str(neighbor.row) + ']' + ' [' + str(neighbor.col) + ']' + ' ' + str(neighbor.state))
            # print('THIS  THE  GSCORE'+str(g_score[neighbor]))
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, target)
                if neighbor not in closed_list:
                    open_list.put((f_score[neighbor], neighbor))
                    closed_list.append(neighbor)
        if curr != start:
            curr.set_closed()


def agent_path(came_from, current):
    path = []
    cnt = 0
    while current in came_from:
        cnt += 1
        current = came_from[current]
        path.append(current.get_pos())

    return path


def StrategyOne(agent, grid, target, draw, q):
    agent_pos = grid[int(agent.row)][int(agent.col)]
    path = []
    astar_list = agent_astar(agent_pos, grid, target, 1)
    if not isinstance(astar_list, Iterable):
        print("error occurred try again")
        return
    path.extend(astar_list)
    agent_pos.set_as_agent()
    draw()
    path_so_far = {}
    if len(path) <= 0:
        print("Agent insta died")
        return
    if len(path) > 0:
        path.pop()
    while len(path) > 0:
        next_step = path.pop()
        # print("next step = " + str(next_step))
        agent.row = next_step[0]
        agent.col = next_step[1]
        agent.set_pos(grid[int(agent.row)][int(agent.col)])
        agent_pos = agent.get_pos()
        if agent_pos.is_on_fire():
            print("Agent died")
            return
        agent_pos.set_as_agent()
        advance_fire_one_step(grid, q)
        draw()
    print("GOAL REACHED!")


# redefine  the fire as a block and compute shortest path given just that.
# move
# rinse repeat

def StrategyTwo(agent, grid, target, draw, q):
    agent_pos = grid[int(agent.row)][int(agent.col)]
    path = []
    came_from = {}
    dim = len(grid)
    # printgrid(alter,len(alter))
    # print("\n\n\n\n\n\n\n")
    # printgrid(grid,len(grid))
    cnt = 0
    while not agent.get_pos() == target:
        alter = alterMaze(grid)
        # print(cnt)
        # printgrid(alter, len(alter))
        # print("\n\n\n\n")
        # printgrid(grid,len(grid))
        agent_copy = Node.Agent(alter[int(agent.row)][int(agent.col)], int(agent.row), int(agent.col))
        agent_copy_pos = agent_copy.get_pos()
        target_copy = alter[dim - 1][dim - 1]
        # print('Agent_copy is:[ ' +str(int(agent_copy.row))+ '] '+ ' ['+str(int(agent_copy.col)) + '] ')
        # print(cnt)
        astar_move = agent_astar(agent_copy_pos, alter, target_copy, 2)
        if not isinstance(astar_move, Iterable):
            print("no path found")
            break
        if len(astar_move) < 1:
            print("no path is possible")
            break
        move = astar_move.pop()
        agent_row = move[0]
        agent_col = move[1]
        curr = grid[agent.row][agent.col]
        agent.set_pos(grid[agent_row][agent_col])
        agent.row = agent_row
        agent.col = agent_col
        came_from[grid[agent.row][agent.col]] = curr
        if agent.get_pos().is_on_fire():
            print("agent died")
            return
        if agent.get_pos() == target:
            print("goal reached!")
            agent.get_pos().set_as_agent()
            reconstruct_path(came_from, curr, draw)
            break
        agent.get_pos().set_as_agent()
        advance_fire_one_step(grid, q)
        draw()
        cnt += 1
    print("END?")


def advance_fire_one_step(grid, q):
    # grid_copy = copy_grid(grid, 0)
    fire = []
    for row in grid:
        for cell in row:
            k = 0
            if cell.state == Node.OPEN or cell.state == Node.AGENT:
                for neighbor in cell.neighbors:
                    # print(neighbor.color)
                    if neighbor.is_on_fire():
                        k += 1
            else:
                continue
            probability = 1 - ((1 - q) ** k)
            random_num = random.uniform(0, 1)
            if random_num <= probability:
                fire.append(grid[cell.row][cell.col])
                # print('SETTING [' + str(cell.row) + ']' + ' [' + str(cell.col) + ']')
    for cell in fire:
        cell.set_on_fire()
    return fire


def alterMaze(grid):
    grid_copy = copy_grid(grid, 1)
    for row in grid_copy:
        for cell in row:
            if cell.is_on_fire():
                cell.set_blocked()
    for row in grid_copy:
        for cell in row:
            cell.update_neighbors(grid_copy)
    # printgrid(grid, len(grid))
    # print("\n\n\whatn\n\n\n")
    # printgrid(grid_copy,len(grid_copy))
    # print("\nend")
    return grid_copy

    # mode = 0 if need to update neighbors now
    # mode = 1 if need to update  neighbors later


def copy_grid(grid, mode):
    num_row = len(grid)
    grid_copy = []
    for i in range(num_row):
        grid_copy.append([])
        for j in range(num_row):
            curr = grid[i][j]
            cell = Node.Cell(i, j, curr.width, curr.total_rows)
            cell.row = curr.row
            cell.col = curr.col
            cell.x = curr.x
            cell.y = curr.y
            cell.state = curr.state
            cell.is_closed = curr.is_closed
            cell.width = curr.width
            cell.total_rows = curr.total_rows
            cell.danger_value = curr.danger_value
            grid_copy[i].append(cell)
    if mode == 0:
        for row in grid_copy:
            for cell in row:
                cell.update_neighbors(grid_copy)
    return grid_copy


# def create_grid(rows, width):
#     grid = []
#     gap = width // rows
#     for i in range(rows):
#         grid.append([])
#         for j in range(rows):
#             cell = Node.Cell(i, j, gap, rows)
#             grid[i].append(cell)
#
#     return grid
def printgrid(grid, rows):
    for i in range(rows):
        for j in range(rows):
            cell = grid[i][j]
            print('[' + str(cell.row) + ']' + ' [' + str(cell.col) + ']' + ' ' + str(cell.state) + ' ' + str(
                cell.neighbors))
            # print(str(cell.color))


# def Strat3Simulation(grid, q, dim):
#     #pick starting fire cell
#     curr = grid[0][0]
#     while True:
#         rand_row = random.randrange(dim)
#         rand_col = random.randrange(dim)
#         if grid[rand_row][rand_col].state == Node.OPEN:
#             curr = grid[rand_row][rand_col]
#             break
# 
#     curr.set_on_fire()
#     curr.set_danger_value(1)
#     print("initial cell on fire")
#     print(curr.get_pos())
# 
#     for i in range(0, dim):
#         advance_fire_one_step(grid, .3)
# 
#     #augMatrix = [dim][dim]
#     rows, cols = (dim, dim)
#     augMatrix = [[0 for i in range(cols)] for j in range(rows)]
# 
# 
#     for row in grid:
#         for cell in row:
#             if cell.is_on_fire():
#                 pos = cell.get_pos()
#                 augMatrix[pos[0]][pos[1]] += 1
# 
# 
#     print(augMatrix)
#     for row in augMatrix:
#         print(row)
# 
# 
#     return augMatrix

# simulates the fire to create  a danger value matrix
def fire_simulation(grid, q):
    num_row = len(grid)
    danger_matrix = []
    for i in range(num_row):
        danger_matrix.append([])
        for j in range(num_row):
            danger_matrix[i].append(0)
    rows = len(grid)
    sim_num = 0
    while sim_num < 40:
        grid_copy = copy_grid(grid, 0)
        for i in range(0, rows):
            fire = advance_fire_one_step(grid_copy, q)
        for row in grid_copy:
            for cell in row:
                if cell.is_on_fire():
                    danger_matrix[cell.row][cell.col] += 1
        sim_num += 1
    print(danger_matrix)
    return danger_matrix


def myFunc(e):
    return e[0]


# 1.generate  a danger matrix
# 2.compute  a  path  with astar
# 3. folow the path, if we step on  a cell  that has  value higher than 10. TRY to pivot to smallest danger value of cell's neighbor
def StrategyThree(agent, grid, target, draw, q):
    restrict = {}
    danger_matrix = fire_simulation(grid, q)
    print("dangermatrix: \n")
    print(danger_matrix)
    for i in range(len(danger_matrix)):
        for j in range(len(danger_matrix)):
            grid[i][j].set_danger_value(danger_matrix[i][j])
    agent_pos = grid[int(agent.row)][int(agent.col)]
    path = []
    astar_list = asta(agent_pos, grid, target, 1,danger_matrix)
    if not isinstance(astar_list, Iterable):
        print("error occurred try again")
        return
    path.extend(astar_list)
    agent_pos.set_as_agent()
    draw()
    while True:
        if not isinstance(path, Iterable):
            print("no path found")
            break
        if len(path) < 1:
            print("GOAL")
            break
        # print("this is the path"+path)
        if agent.get_pos().is_on_fire():
            print("agent died")
            return
        step = path.pop()
        agent.row = step[0]
        agent.col = step[1]
        agent.set_pos(grid[agent.row][agent.col])
        agent.get_pos().set_as_agent()
        if agent.get_pos().is_on_fire():
            print("agent died")
            return
        advance_fire_one_step(grid,q)
        draw()
        print(path)
        print('\n')
        if(agent.get_pos==target):
            print('GOAL')
            break
        # if danger_matrix[agent.row][agent.col] > 15:
        #     print(danger_matrix[agent.row][agent.col])
        #     print("no")
        #     candidates = []
        #     for neighbor in agent.get_pos().neighbors:
        #         candidates.append(neighbor.get_danger_neighbor())
        #     candidates.sort(reverse=True, key=myFunc)
        #     candidate = candidates.pop()
        #     print("current:" +  '[' + str(agent.row) + ']' + ' [' + str(agent.col) + ']' + str(danger_matrix[agent.row][agent.col]))
        #     print("candidate:\n")
        #     print(candidate)
        #     print('[' + str(candidate[1].row) + ']' + ' [' + str(candidate[1].col) + ']')
        #     if candidate[0] >= 15 or candidate[0] >= danger_matrix[agent.row][agent.col]:
        #         continue
        #     if candidate[0] < danger_matrix[agent.row][agent.col]:
        #         alterPath = asta(candidate[1],grid,target,1,danger_matrix)
        #         # path = alterPath
        #     print("alterpath:")
        #     print(alterPath)
        #     if len(alterPath) < 0:
        #         continue


def asta(start, grid, target, strat,danger_matrix):
    came_from = {}
    closed_list = []
    open_list = PriorityQueue()
    open_list.put((0, start))
    g_score = {Node: float("inf") for row in grid for Node in row}
    g_score[start] = 0
    f_score = {Node: float("inf") for row in grid for Node in row}
    f_score[start] = heuristic(start, target)
    while not open_list.empty():
        curr = open_list.get()[1]
        # print('[' + str(curr.row) + ']' + ' [' + str(curr.col) + ']' + ' ' + str(curr.state))
        # curr.set_explored()
        if curr == target:
            path = agent_path(came_from, curr)
            if strat == 1:
                return path
        for neighbor in curr.neighbors:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, target)+danger_matrix[neighbor.row][neighbor.col]
                if neighbor not in closed_list:
                    open_list.put((f_score[neighbor], neighbor))
                    closed_list.append(neighbor)
        if curr != start:
            curr.set_closed()

# Strategy 3

# modified astar for strategy 3
def modifed_astar(draw, grid, start, dim, target):
    my_data = Data()
    came_from = {}
    closed_list = []
    open_list = PriorityQueue()
    open_list.put((0, start))
    g_score = {Node: float("inf") for row in grid for Node in row}
    g_score[start] = 0
    f_score = {Node: float("inf") for row in grid for Node in row}
    f_score[start] = heuristic(start, target)
    while not open_list.empty():
        curr = open_list.get()[1]
        curr.set_explored()
        if curr == target:
            path = reconstruct_path(came_from, curr, draw)
            '''
            my_data.graph_type = "Astar"
            my_data.path = len(path)
            my_data.explored = len(closed_list)
            DATA.append([my_data.graph_type, my_data.path, my_data.explored])

            print(str(len(path)) + " in path")
            print(str(len(closed_list)) + " explored")
            '''
            return path

        for neighbor in curr.neighbors:
            temp_g_score = g_score[curr] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, target)
                if neighbor not in closed_list:
                    open_list.put((f_score[neighbor], neighbor))
                    closed_list.append(neighbor)
        draw()
        if curr != start:
            curr.set_closed()

    '''
    print(str(len(closed_list)) + " explored")
    my_data.graph_type = "Astar"
    my_data.path = 0
    my_data.explored = len(closed_list)
    DATA.append([my_data.graph_type, my_data.path, my_data.explored])
    '''
    return []

# #strategy three
# def StrategyThree(grid, target, draw, q, dim):
#     path = []
#     agent = grid[0][0]
#     curr_path = modifed_astar(draw, grid, agent, dim, target)
#     if len(curr_path) == 0:
#         print("No path")
#         return
#     print(curr_path)
#
#     curr_path.pop()
#     while curr_path == []:
#         loc = curr_path.pop()#
#         agent = grid[loc[0]][loc[1]]#agent take step
#         path.append(agent.get_pos())
#         advance_fire_one_step(grid, q) #fire take step
#         if agent.is_on_fire():
#             print("agent died in fire")
#             return
#         if agent.get_danger_value() > 10: #if danger value > 10 recompute for new path
#             new_path = modifed_astar(draw, grid, agent, dim, target)
#             if new_path == []:
#                 print("There is no path")
#                 break
#             curr_path = new_path
#
#     print("Agent exited maze safely")
#     return
