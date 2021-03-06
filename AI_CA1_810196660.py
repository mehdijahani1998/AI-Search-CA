from os import stat
import time
import heapq

class time_frame_state:
    
    def __init__ (self, drstranges, potions, drugs):
        self.drstranges = drstranges
        self.drugs = drugs
        self.potions = potions
        self.parent = None
        self.current_distance = -1
        self.index = -1
            
    def __eq__(self, state):
        if not(len(self.drstranges)==len(state.drstranges) and len(self.drugs)==len(state.drugs) and len(self.potions)==len(state.potions)):
            return False
        
        
        for index in range(len(self.drstranges)):
            if (self.drstranges[index]!=state.drstranges[index]):
                print(state.__hash__())
                
        if hash(tuple(self.drugs))!=hash(tuple(self.drugs)):
            return False
        
        if hash(tuple(self.potions))!=hash(tuple(self.potions)):
            return False
        
        return True
    
    def __hash__(self):
        return hash((hash(tuple(self.drstranges)), hash(tuple(self.drugs)), hash(tuple(self.potions))))


    
class dungeon:
    
    def __init__(self, file_name): #reading input and creating a dungeon in which the fight happens.
        
        self.qeueu = []
            
        #openning and reading the input file
        
        file = open(file_name, "r") 
        
        self.row_num, self.col_num = map(int, file.readline().split())
        
        potion_num, drug_num = map(int, file.readline().split())
        
        
        #Store the location of initial Dr.Stranger
        
        drstranges = []    
        drstranges.append((0,0))
        
        
        #Storing the location of potions as indicated in the input file
        
        potions = set()  
        for i in range(potion_num):
            x, y = map(int, file.readline().split())
            potions.add((x,y))
            
        #Storing the location of double drugs as indicated in the input file
        
        drugs = set()   
        for i in range(drug_num):
            x, y = map(int, file.readline().split())
            drugs.add((x,y))
            
        if ((0,0) in drugs):
            drstranges.append((self.row_num-1, 0))
                        
        #initiating the fighting procedure with thanos. this is the creation of the initial state
        
        self.start_state = time_frame_state(drstranges, potions, drugs) 
        self.strat_state.current_distance = 0
        self.strat_state.index = 0
        

        #Storing the location of blocks as indicated in the input file
        
        block_num = int(file.readline())
        
        self.blocks = set()
        
        for i in range(block_num):
            x, y = map(int, file.readline().split())
            self.blocks.add((x,y))
            
    def check_cell (self, row, col):
        return (col > -1 and row > -1 and col < self.col_num and row < self.row_num and not((row, col) in self.blocks))
    
    
    def retrieve_children (self, state):
        children = []
        
        moves = [-1,1,0,0,0,0,1,-1]
        
        drstranges_copy = state.drstranges.copy()
        drugs_copy = state.drugs.copy()
        potions_copy = state.potions.copy()
        
        for i in range(len(state.drstranges)):
            
            for j in range(4):
                
                #move dr to a new cell
                
                new_row = state.drstranges[i][0] + moves[j]
                new_col = state.drstranges[i][1] + moves[j+4]
                
                if self.check_cell(new_row, new_col):
                    
                    drstranges_copy[i] = (new_row, new_col)
                    
                    #check if any drug exists in the new cell. 
                    
                    if ((new_row, new_col) in state.drugs):
                        
                        drstranges_copy.append((self.row_num-1,0))
                        drugs_copy.remove((new_row, new_col))
                    
                    #check if any potion exists in the new cell.
                    if ((new_row, new_col) in state.potions):
                        
                        potions_copy.remove((new_row,new_col))
                        
                    children.append(time_frame_state(drstranges_copy, potions_copy, drugs_copy))

                    #return copies back to their normal
                    potions_copy = state.potions.copy()
                    drugs_copy = state.drugs.copy()
                    drstranges_copy = state.drstranges.copy()

        return children

    #check if the corresponding state to a node is the goal or not
    def goal_state_check(self, state):
        
        #check if there's still potions in the dungeon
        if(len(state.potions) != 0):
            return False
        #check if dr.Stranges are in the anticipated positions
        for index in range(len(state.drstranges)):
            if not (state.drstranges[index][1] == self.col_num-1 and state.drstranges[index][0] == self.row_num-1):
                return False
        return True

    #here we calaulate heuristic. In this case we consider manhattan distance as discussed in the course
    def retrieve_heuristic (self, state):
        hr = 0
        for dr in state.drstranges:
            hr += (self.row_num-1-dr[0])+(self.col_num-1-dr[1])
        return hr

    def list_difference_index(self, l1, l2):
        min_length = min(len(l1), len(l2))

        #finds the first index in which lists are different
        for index in range(min_length):
            if (l1[index] != l2[index]):
                return index
        return -1


    def breadth_first_search(self):
        head = 0

        explored = set()
        explored.add(self.start_state)
        self.qeueu.append(self.start_state)

        while (len(self.qeueu) != 0):

            node = self.qeueu[head] 
            children_nodes = self.retrieve_children(node)
            for child in children_nodes:
                if not(child in explored):
                    child.index = len(self.qeueu) # index in qeueu list
                    child.parent = node.index
                    child.current_distance = node.current_distance+1
                    self.qeueu.append(child)
                    explored.add(child)
                    if self.goal_state_check(child):
                        return child
            head += 1
    

    def depth_first_search(self, current, depth_limit, explored):
        
        if (current.current_distance > depth_limit):
            return None # goal state is not in this subtree

        children_node = self.retrieve_children(current)
        for child in children_node:
            if not(child in explored) or current.current_distance < explored[child] -1 :
                child.index = len(self.qeueu)
                child.parent = current.index
                child.current_distance = current.current_distance + 1
                explored[child] = child.current_distance
                self.qeueu.append(child)
                if self.goal_state_check(child):
                    return child
                out = self.depth_first_search(child, current, depth_limit, explored)
                if out is not None:
                    return out

    def depth_search(self):
        limit = 1
        while True:
            print("depth limit:", limit)
            explored = dict()
            explored[self.start_state] = 0
            self.qeueu = []
            self.qeueu.append(self.start_state)
            out = self.depth_first_search(self.start_state, None, limit, explored)
            if out is not None:
                return out
            limit += 1

    
    def a_star_search(self, weight=1):
        frontier = [] 

        heapq.heappush(frontier, (self.retrieve_heuristic(self.start_state)*weight, 0))

        explored = set()
        explored.add(self.start_state)
        
        self.qeueu.append(self.start_state)

        while (len(frontier) != 0):
            node_index = heapq.heappop(frontier)[1] # get smallest f(n) in frontier list
            node = self.qeueu[node_index]

            children = self.retrieve_children(node)
            for child_node in children:
                if not(child_node in explored):
                    child_node.index = len(self.qeueu) # index in qeueu list
                    child_node.parent = node.index
                    child_node.current_distance = node.current_distance+1
                    heapq.heappush(frontier, (child_node.current_distance + self.retrieve_heuristic(child_node)*weight, child_node.index))
                    self.qeueu.append(child_node)
                    explored.add(child_node)
                    if self.goal_state_check(child_node):
                        return child_node
        

    def retrieve_path(self, goal_state):
        path_indices = []

        curr_index = goal_state.id
        path_indices.append(curr_index)
        while (curr_index != 0):
            curr_index = self.qeueu[curr_index].parent
            path_indices.append(curr_index)
        path_indices.reverse()
        return path_indices

    def print_path(self, path_indices):
        for i in range(len(path_indices)-1):
            index = self.list_difference_index(self.qeueu[path_indices[i]].drstranges, self.qeueu[path_indices[i+1]].drstranges)
            if (index==-1):
                print("*not found different index!")
                continue
            print(str(i+1) + ".", "doctor #" + str(index+1), "move ",
                self.qeueu[path_indices[i]].drstranges[index], " -> ", self.qeueu[path_indices[i+1]].drstranges[index])    
    

    def print_bfs_solution(self):
        start_time = time.time()
        goal_state = self.breadth_first_search()

        print("minimum steps: ", goal_state.current_distance)
        print("visited states: ", len(self.qeueu))
        print("path length to goal: ")
        path_indices = self.retrieve_path(goal_state)
        self.print_path(path_indices)

        end_time = time.time()

        print("total time = ", end_time - start_time)

    def print_ids_solution(self):
        start_time = time.time()
        goal_state = self.depth_search()

        print("minimum steps: ", goal_state.current_distance)
        print("visited states: ", len(self.qeueu))
        print("path length to goal: ")
        path_indices = self.retrieve_path(goal_state)
        self.print_path(path_indices)

        end_time = time.time()

        print("total time = ", end_time - start_time)

    def print_astar_solution(self, parameter):
        start_time = time.time()
        goal_state = self.a_star_search(parameter)

        print("minimum steps: ", goal_state.current_distance)
        print("visited states: ", len(self.qeueu))
        print("path length to goal: ")
        path_indices = self.retrieve_path(goal_state)
        self.print_path(path_indices)

        end_time = time.time()
        print("total time = ", end_time - start_time)
    
FILE_NUMBER = 1
game = dungeon("test" + str(FILE_NUMBER) + ".in")
game.print_solution()