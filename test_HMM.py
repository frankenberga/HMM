from Maze import Maze
from HMM import HMM

test_maze1 = Maze("maze1.maz")
hmm_maze1 = HMM(test_maze1)
hmm_maze1.filtering(4)
sensed = hmm_maze1.sensed
hmm_maze1.viterbi(sensed)
hmm_maze1.forward_backward_smoothing(sensed, hmm_maze1.initial_state(), 1)