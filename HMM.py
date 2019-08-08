from Maze import Maze
import random
import numpy as np

#this class does the HMM problem layout and search process etc.
class HMM:
    
    def __init__(self, maze):
        self.maze = maze
        self.width = maze.width
        self.height = maze.height
        self.robot_loc = maze.robotloc
        print ("robot location", self.robot_loc)
        self.sense_list = ['r', 'g', 'b', 'y']
        self.maze_map = maze.maze_map
        #print ("maze map:", self.maze_map)
        #the probability of a given color given the sensor output. order of prob list is [r, g, b, y]
        self.color_map = maze.color_map
        #print ("color map:", self.color_map)
        self.color_map_probs = maze.color_map_probs
        #print ("color map probs:", self.color_map_probs)
        self.color_probs = maze.color_probs
        #print ("color probabilities:", self.color_probs)
        self.state = self.initial_state()
        #print ("initial state:", self.state)
        self.update_red = self.create_update_matrix('r')
        #print ("red update matrix:", self.update_red)
        self.update_green = self.create_update_matrix('g')
        #print ("green update matrix:", self.update_green)
        self.update_blue = self.create_update_matrix('b')
        #print ("blue update matrix:", self.update_blue)
        self.update_yellow = self.create_update_matrix('y')
        #print ("yellow update matrix:", self.update_yellow)
        self.transition_matrix = self.create_transition_matrix()
        #print ("transition matrix:", self.transition_matrix)
        self.sensed = []
        

    #this creates the initial probability distribution of the possible start states
    #based on the size of the maze
    def initial_state(self):
        initial_state = []
        for h in range (0, self.height):
            for w in range (0, self.width):
                initial_state.append(1/(self.height * self.width))
        return initial_state

    #this method moves the robot one square
    def move(self):
        direction = random.randint(0, 3)
        new_x = self.robot_loc[0]
        new_y = self.robot_loc[1]
        #moving south
        if direction == 0:
            print ("robot moving south")
            new_y = self.robot_loc[1] + 1
        #moving north
        elif direction == 1:
            print ("robot moving north")
            new_y = self.robot_loc[1] - 1
        #moving east
        elif direction == 2:
            print ("robot moving west")
            new_x = self.robot_loc[0] + 1
        #moving west
        elif direction == 3:
            print ("robot moving east")
            new_x = self.robot_loc[0] - 1
        if (new_x < self.width and new_x >= 0 and new_y < self.height and new_y >= 0):
            if (self.maze_map[new_x + 4*new_y] == "."):
                self.robot_loc[0] = new_x
                self.robot_loc[1] = new_y
                self.maze.robotloc[0] = new_x
                self.maze.robotloc[1] = new_y
        print ("robot location", self.robot_loc)

    #this method moves the robot and then returns the sensed color based on the probabilities
    def sense(self, xloc, yloc):
        rand_int = round(random.uniform(0, 1),2)
        #print ("random integer", rand_int)
        color_list = self.color_map_probs[yloc][xloc]
        ordered_color_list = []
        for x in range (0, len(color_list)):
            if (color_list[x] == 0.88):
                ordered_color_list.insert(0, self.sense_list[x])
            else:
                ordered_color_list.append(self.sense_list[x])
        if rand_int < .88:
            return ordered_color_list[0]   
        elif rand_int >= .88 and rand_int < .92:
            return ordered_color_list[1]
        elif rand_int >= .92 and rand_int < .96:
            return ordered_color_list[2]
        elif rand_int >= .96 and rand_int < 1:
            return ordered_color_list[3]

    #this method creates an update matrix for a given color sensed
    #it is a 16x16 matrix with the diagonal containing the update values
    def create_update_matrix(self, color):
        update_matrix = []
        hcount = 0
        wcount = 0
        for h in range (0, len(self.state)):
            update_list = []
            for w in range (0, len(self.state)):
                if h == w:
                    if color == self.color_map[hcount*4 + wcount]:
                        update_list.append(0.88) #putting the value 0.88 if it is that color
                    else:
                        update_list.append(0.04) #otherwise putting value 0.04
                    if (wcount == 3):
                        hcount += 1
                        wcount = 0
                    else:
                        wcount += 1
                else:
                    update_list.append(0)
            update_matrix.append(update_list)
        return np.array(update_matrix)

    #this method creates the transition matrix (transposed so that we can use matrix mult)
    def create_transition_matrix(self):
        transition_matrix = []
        for loc in range (0, len(self.state)):
            transition_vec = self.create_transition_vector(loc)
            transition_matrix.append(np.array(transition_vec))
        #print (transition_matrix)
        tm = np.array(transition_matrix)
        tm = tm.T
        return tm

    #this method creates a transition vector for the given location, with equal prob for each of 4 directions
    def create_transition_vector(self, location):
        #first figure out how many adjacent locations are possible
        #then create vector with values in it
        transition_vector = []
        yloc = int(location / 4)
        xloc = int(4 - location/4)
        numlocs = 0
        #this creates an vector with all 0s
        for i in range (0, len(self.state)):
            transition_vector.append(0)
        for dir in range (0, 4):
            #check move south
            if dir == 0:
                if (yloc + 1 < self.height and self.maze_map[location] == "."):
                    new_loc = location + 4
                    transition_vector[new_loc] = 0.25
                    numlocs += 1
            #check move north
            elif dir == 1:
                if (yloc - 1 > 0 and self.maze_map[location] == "."):
                    new_loc = location - 4
                    transition_vector[new_loc] = 0.25
                    numlocs += 1
            #check move east
            elif dir == 2:
                if (xloc + 1 < self.width and self.maze_map[location] == "."):
                    new_loc = location + 1
                    transition_vector[new_loc] = 0.25
                    numlocs += 1
            #check move west
            elif dir == 3:
                if (xloc - 1 > 0 and self.maze_map[location] == "."):
                    new_loc = location - 1
                    transition_vector[new_loc] = 0.25
                    numlocs += 1
        if numlocs == 1:
            transition_vector[location] = 0.75
        elif numlocs == 2:
            transition_vector[location] = 0.5
        elif numlocs == 3:
            transition_vector[location] = 0.25
        return transition_vector

    #this method normalizes the state
    def normalize(self):
        total = 0
        for elem in range (0, len(self.state)):
            total += self.state[elem]
        normalize = 1/total
        for elem in range (0, len(self.state)):
            curr_value = self.state[elem]
            norm_value = normalize * curr_value
            self.state[elem] = norm_value
    
    #this method does the overall filtering process
    def filtering(self, num_iter):
        #for a certain number of time steps i.e. iterations
        for iter in range (0, num_iter):
            #the robot moves after the first iteration
            if iter > 0:
                self.move()
            #prediction step
            self.state = np.matmul(self.state, self.transition_matrix)
            #the color that is sensed at this location
            color = self.sense(self.robot_loc[0], self.robot_loc[1])
            print ("sensed color:", color)
            self.sensed.append(color)
            #update step
            update_matrix = self.get_update_matrix(color)
            self.state = np.matmul(self.state, update_matrix)
            self.print_state()
            print (self.maze)
        #normalize step
        self.normalize()   
        self.print_state()
        
        print ("sensed list:", self.sensed)

    #this prints the probability in a readable fashion
    def print_state(self):
        for h in range (0, self.height):
            print_line = "["
            for w in range (0, self.width):
                print_line += str(self.state[h*4 + w]) + ", "
            print (print_line + "]")
        print ("\n")


    #BONUS SECTION:

    #This is the viterbi algorithm for calculating the most likely path for the robot       
    def viterbi(self, sensed_list):
        print (sensed_list)
        i_s = self.initial_state()
        total_num_obs = len(sensed_list)
        print (total_num_obs)
        viterbi_graph = [{}]
        #this puts all of the possible start states into the list at level 0
        for elem in range (0, len(i_s)):
            sense_color = sensed_list[0]
            update_matrix = self.get_update_matrix(sense_color)
            viterbi_graph[0][elem] = {"p": i_s[elem]*update_matrix[elem][elem], "backpointer": None}
        #for the given number of observations
        for num_obs in range(1, total_num_obs):
            sense_color = sensed_list[num_obs]
            update_matrix = self.get_update_matrix(sense_color)
            viterbi_graph.append({})
            for elem in range (0, len(i_s)):
                #starting with the max transition value being the trans to the fist element
                max_trans = viterbi_graph[num_obs-1][0]["p"] * self.transition_matrix[0][elem] * update_matrix[elem][elem]
                prev_state = 0 #and this prev state being 0
                for prev in range (1, len(i_s)): #searching through all of the other previous states
                    trans = viterbi_graph[num_obs-1][prev]["p"] * self.transition_matrix[prev][elem] * update_matrix[elem][elem]
                    #updating if there is a better way to get there
                    if trans > max_trans:
                        max_trans = trans
                        prev_state = prev
                xloc = int(4 - num_obs / 4)
                yloc = int(num_obs / 4)
                viterbi_graph[num_obs][elem] = {"p": max_trans, "backpointer": prev_state}
        backtrack_path = self.backtrack(viterbi_graph, total_num_obs)
        processed_path = self.process_path(backtrack_path)
        print ("Viterbi algorithm found path:", processed_path)
        self.graphical_path(processed_path)

    #this returns the appropriate update matrix given the color sensed
    def get_update_matrix(self, color):
        update_matrix = None
        if color == 'r':
            update_matrix = self.update_red
        elif color == 'g':
            update_matrix = self.update_green
        elif color == 'b':
            update_matrix = self.update_blue
        elif color == 'y':
            update_matrix = self.update_yellow
        return update_matrix

    #this takes a graph that contains the highest probability element at every observation step 
    #with backpointers point to where they came from
    def backtrack(self, viterbi_graph, total_num_obs):
        path = []
        curr_obs = total_num_obs - 1
        highest_val = max(value["p"] for value in viterbi_graph[curr_obs].values())
        highest_state = 0
        for elem in viterbi_graph[curr_obs].keys():
            if viterbi_graph[curr_obs][elem]["p"] == highest_val:
                highest_state = elem
        path.append(highest_state)
        count = 1    
        while highest_state != None:
            highest_state = viterbi_graph[curr_obs][highest_state]["backpointer"]
            path.append(highest_state)
            curr_obs -= 1
            count += 1
        path.reverse()
        return path

    #this method takes a backtrack path and returns a path of (x,y) locations in maze
    def process_path(self, backtrack_path):
        processed_path = []
        for elem in backtrack_path:
            if (elem != None):    
                yloc = int(elem/4)
                xloc = elem - yloc*4
                loc = (xloc, yloc)
                processed_path.append(loc)
        return processed_path

    #this prints out images of the robot moving in the actual maze
    def graphical_path(self, processed_path):
        for elem in processed_path:
            self.maze.robotloc[0] = elem[0]
            self.maze.robotloc[1] = elem[1]
            print (self.maze)

    #this calculates the value via the forward process
    def forward(self, vector_elem, evidence):
        #prediction step
        elem_prob = np.matmul(vector_elem, self.transition_matrix)
        #update step
        update_matrix = self.get_update_matrix(evidence)
        elem_prob = np.matmul(elem_prob, update_matrix)
        # #normalize step
        # self.normalize_matrix(elem_prob)   
        return elem_prob

    #this calculates the value via the forward process
    def backward(self, backward_message, evidence):
        #update step
        update_matrix_1 = self.get_update_matrix(evidence)
        elem_prob = np.matmul(backward_message, self.transition_matrix)
        elem_prob = np.matmul(update_matrix_1, elem_prob)
        return elem_prob

    #this method normalizes the state
    def normalize_matrix(self, matrix):
        norm_matrix = matrix
        total = np.sum(matrix)
        normalize = 1/total
        for elem in range (0, len(matrix)):
            curr_value = matrix[elem]
            norm_value = normalize * curr_value
            norm_matrix[elem] = norm_value
        return norm_matrix

    #this is the overarching forward backward algorithm 
    def forward_backward_smoothing(self, evidence, prior, elem_desired):
        print ("Forward Backward Smoothing:")
        print("Probability for time =", elem_desired)
        t = len(evidence) 
        backward_message = [1] * 16
        forward_messages = [0] * t
        smoothed_vector = [0] * t
        forward_messages[0] = prior
        for i in range (1, t):
            forward_messages[i] = self.forward(forward_messages[i-1], evidence[i-1])
        t = len(evidence)
        for j in range (t - 1, -1, -1):
            matrix = forward_messages[j] * backward_message
            smoothed_vector[j] = self.normalize_matrix(matrix)
            backward_message = self.backward(backward_message, evidence[j])
        self.print_smoothed_state(smoothed_vector[elem_desired])
    
    #this prints the probability in a readable fashion
    def print_smoothed_state(self, smoothed_vector):
        for h in range (0, 4):
            print_line = "["
            for w in range (0, 4):
                print_line += str(smoothed_vector[w]) + ", "
            print (print_line + "]")
        print ("\n")

    





            


            

