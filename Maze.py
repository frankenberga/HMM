from time import sleep

# Maze.py
#  original version by db, Fall 2017
#  Feel free to modify as desired.

# Maze objects are for loading and displaying mazes, and doing collision checks.
#  They are not a good object to use to represent the state of a robot mazeworld search
#  problem, since the locations of the walls are fixed and not part of the state;
#  you should do something else to represent the state. However, each Mazeworldproblem
#  might make use of a (single) maze object, modifying it as needed
#  in the process of checking for legal moves.

# Test code at the bottom of this file shows how to load in and display
#  a few maze data files (e.g., "maze1.maz", which you should find in
#  this directory.)

#  the order in a tuple is (x, y) starting with zero at the bottom left

# Maze file format:
#    # is a wall
#    . is a floor
# the command \robot x y adds a robot at a location. The first robot added
# has index 0, and so forth.


class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.rows

    def __init__(self, mazefilename):

        self.robotloc = []
        self.colors = []
        # read the maze file into a list of strings
        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                segment = line.split(" ")
                if segment[0] == "\\colors":
                    self.colors = segment[1:]
                elif segment[0] == "\\robot":
                    x = int(segment[1])
                    y = int(segment[2])
                    self.robotloc.append(x)
                    self.robotloc.append(y)
            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)
        self.map = list("".join(lines))
        
        self.maze_map = self.create_maze_map()

        sensor_probs = {'r': [0.88, 0.04, 0.04, 0.04], 'g': [0.04, 0.88, 0.04, 0.04], 
            'b': [0.04, 0.04, 0.88, 0.04], 'y': [0.04, 0.04, 0.04, 0.88]}
        self.color_map_probs = self.create_color_map_probs(self.colors, sensor_probs)
        self.color_map = self.create_color_map(self.colors)
        self.color_probs = self.create_color_probs()

    #this method creates a 2d array representing the maze and floor vs wall locations
    def create_maze_map(self):
        maze_map = []
        for h in range (0, self.height):
            for w in range (0, self.width):
                maze_map.append(self.map[h*self.height + w])
        return maze_map

    #this creates a list of overarching color probabilities given the maze
    def create_color_probs(self):
        num_r = 0
        num_g = 0
        num_b = 0
        num_y = 0
        total_num = len(self.color_map)
        for x in range (0, total_num):
            if self.color_map[x] == 'r':
                num_r += 1
            elif self.color_map[x] == 'r':
                num_r += 1
            elif self.color_map[x] == 'r':
                num_r += 1
            elif self.color_map[x] == 'r':
                num_r += 1
        color_probs = [num_r/total_num, num_g/total_num, num_b/total_num, num_y/total_num]
        return color_probs

    #this creates a 2d array of the color probabilities for the maze based on the input
    def create_color_map_probs(self, color_line, sensor_probs):
        color_map_probs = []
        for h in range (0, self.height):
            row = []
            for w in range (0, self.width):
                color = color_line[h*self.height + w]
                prob_list = sensor_probs[color]
                row.append(prob_list)
            color_map_probs.append(row)
        return color_map_probs

    #this creates a 2d array of the colors for the maze based on the input
    def create_color_map(self, color_line):
        color_map = []
        for h in range (0, self.height):
            for w in range (0, self.width):
                color = color_line[h*self.height + w]
                color_map.append(color)
        return color_map

    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    #this returns the robot location index in the list
    def robot_loc_index(self, x, y):
        return (y*4 + x)


    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.map[self.index(x, y)] == "."


    def has_robot(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        for i in range(1, len(self.robotloc), 2):
            #print i
            rx = self.robotloc[i]
            ry = self.robotloc[i + 1]
            if rx == x and ry == y:
                return True
        return False


    # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self):
        robot_number = 0
        renderlist = list(self.map)
        for index in range(0, len(self.robotloc), 2):
            x = self.robotloc[index]
            y = self.robotloc[index + 1]
            renderlist[self.robot_loc_index(x, y)] = robotchar(robot_number)
            robot_number += 1
        return renderlist

    def __str__(self):

        # render robot locations into the map
        renderlist = self.create_render_list()

        # use the renderlist to construct a string, by
        #  adding newlines appropriately

        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s+= renderlist[self.index(x, y)]

            s += "\n"
        return s

def robotchar(robot_number):
    return chr(ord("A") + robot_number)


# Some test code

if __name__ == "__main__":
    test_maze1 = Maze("maze1.maz")
    print(test_maze1)