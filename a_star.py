import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

#This function return the path of the search
def return_path(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    # here we create the initialized result maze with -1 in every position
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    start_value = 0
    # we update the path of start to end found by A-star serch with every step incremented by 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1

    return path

# Default search on a grid maze (implementation of Lab4)
def search(maze, start, end, scale_factor):
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze: the costMap
        :param start: starting position as cell positions
        :param end: goal position as cell positions
        :pram scale_factor: scaling factor to reduce the maze and search to speed up the search
        :return: path as tuples from the given start to the given end
    """

    maze = maze.copy().T
    maze = maze[::scale_factor, ::scale_factor]  

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_dict = {} # will save the node, key is the position (tuple)
    # # in this list we will put all node those already explored so that we don't explore it again    
    visited_dict = {}      # only save the True values, key is the position (tuple)

    # Add the start node
    yet_to_visit_dict[start_node.position] = start_node
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # what squares do we search . serarch movement is 8 point connectivity

    move  =  [[-1, 0 ], # go up
              [ 0, -1], # go left
              [ 1, 0 ], # go down
              [ 0, 1 ],
              [-1, 1],
              [-1, -1],
              [1, 1],
              [1, -1]] # go right


    """
        1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) add to valid children node list for the selected parent node
                d) else move the child to yet_to_visit list
    """
    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(maze)
    

    # Loop until you find the end
    
    while len(yet_to_visit_dict) > 0:
        
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1    
        
        # Get the current node
        current_node_position = (-999, -999)
        current_node = Node(None, tuple(current_node_position))
        current_node.f = 999999
        for i_position in yet_to_visit_dict.keys():
            i_node = yet_to_visit_dict[i_position] ## first is g, second is f
            if i_node.f < current_node.f: ## compare the f
                current_node = i_node
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,maze)

        # Pop current node out off yet_to_visit list, add to visited list
        yet_to_visit_dict.pop(current_node.position)
        visited_dict[current_node.position] = True

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            print ("Goal reached")
            return return_path(current_node,maze)

        # Generate children from all adjacent squares
        children = []

        for new_position in move: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if maze[node_position[0],node_position[1]] > 0.8:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        
        for child in children:
  
            # Child is on the visited list (search entire visited list)
            if visited_dict.get(child.position, False):
                continue

            # Create the f, g, and h values
            child.g = current_node.g + sqrt(((child.position[0] - current_node.position[0]) ** 2) + 
                                           ((child.position[1] - current_node.position[1]) ** 2))
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = sqrt(((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            child_node_in_yet_to_visit = yet_to_visit_dict.get(child.position, False)
            if (child_node_in_yet_to_visit is not False) and (child.g >= child_node_in_yet_to_visit.g):
                continue

            # Add the child to the yet_to_visit list
            yet_to_visit_dict[child.position] = child

def distance(start_node, end_node):
    """
        Returns the euclidean distance between start and end nodes
    """
    # Calculate cost from start to end node using euclidean distance
    return sqrt(((start_node.position[0] - end_node.position[0]) ** 2) + 
                ((start_node.position[1] - end_node.position[1]) ** 2)) 

# [Part 3] TODO Complete the this function so that it is adapted to search a graph provided as PRM instead of a grid maze
# Hint: look at the original A* search above and adapt to the PRM
def search_PRM(points, prm, start, end):
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param points: list of sample points (tuples of coordinates)
        :param prm: probabilistic roadmap (indexes of child points)
        :param start: starting position as cell positions (indexes of the costMap)
        :param end: goal position as cell positions (indexes of the costMap)
        :return: path as tuples from the given start to the given end
        :return:
    """
    # Create start and end node with initized values for g, h and f
    start_idx = points.index(tuple(start))
    start_node = Node(None, points[start_idx])
    start_node.g = start_node.h = start_node.f = 0

    end_idx = points.index(tuple(end))
    end_node = Node(None, points[end_idx])
    end_node.g = end_node.h = end_node.f = 0

    # Initialise memory for A* algorithm
    path_points = []
    # open and closed list will be lists of tuples with point index and node information
    open_list = [(start_idx, start_node)]
    closed_list = []    # not actually used anywhere but helpful for debugging
    parent_node = start_node
    parent_index = start_idx

    # Search until end is found
    while not parent_node == end_node:
        parent_index, parent_node = open_list[0]

        # Select node with lowest total cost to be the next parent node
        for test_index, test_node in open_list:
            if test_node.f < parent_node.f:
                parent_node = test_node
                parent_index = test_index

        # move the parent node (with lowest cost) to the closed list
        closed_list.append((parent_index, parent_node))
        open_list.pop(open_list.index((parent_index, parent_node)))
        # print("Searching point: " + str(parent_index) + " @ " + str(parent_node.position))

        if parent_node == end_node:
            break

        # add child nodes to open list
        for child in prm[parent_index]:
            # check if child already exists in the open list
            if any(item[0] == child for item in open_list):
                item_num = 0
                # manually index the existing item in the open list
                for num, item in enumerate(open_list):
                    if item[0] == child:
                        item_num = num
                        break
                
                # get existing node
                temp_index, temp_node = open_list[item_num]

                # update the node if the new cost g would be less than the existing cost
                if temp_node.g > (parent_node.g + distance(parent_node, temp_node)):
                    temp_node.g = parent_node.g + distance(parent_node, temp_node)
                    temp_node.h = distance(temp_node, end_node)
                    temp_node.f = temp_node.g + temp_node.h
                    temp_node.parent = parent_node
                    # save updated node back to the open list
                    open_list[temp_index] = temp_node
            else:
                # create new node
                temp_node = Node(parent_node, points[parent_index])
                temp_node.g = parent_node.g + distance(parent_node, temp_node)
                temp_node.h = distance(temp_node, end_node)
                temp_node.f = temp_node.g + temp_node.h
                # add new node at end of open list
                open_list.append((child, Node(parent_node, points[parent_index])))
    
    # generate path by following the parent node references starting at the final node from the PRM A* search
    path_node = parent_node
    while path_node is not None:
        path_points.append(path_node.position)
        path_node = path_node.parent
    # Return reversed path as we need to show from start to end path
    path_points = path_points[::-1]
    
    return path_points
