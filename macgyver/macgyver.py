import sys
import random
sys.path.append('..')
from common import board
from copy import deepcopy
import time


ply_alpha=4

#Static Weights Heuristic Function 
WEIGHTS = [4, -3, 2, 2, 2, 2, -3, 4,
               -3, -4, -1, -1, -1, -1, -4, -3,
               2, -1, 1, 0, 0, 1, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 1, 0, 0, 1, -1, 2,
               -3, -4, -1, -1, -1, -1, -4, -3,
               4, -3, 2, 2, 2, 2, -3, 4]

def cornerweight(color, the_board):
    """
    Returns the heuristic following the static weights heuristic function.
    :return: float
    """
    total = 0
    i = 0
    while i < 64:
        if the_board.tiles[int(i/8)][int(i%8)] == color:
            total += WEIGHTS[i]
        if the_board.tiles[int(i/8)][int(i%8)] == the_board.opponent(color):
            total -= WEIGHTS[i]
        i += 1
    return total

def heuristic(color,the_board):
    return cornerweight(color,the_board)

def minimax_ab(color,the_board,ply):
    """
    Returns a move following minimax with alpha and beta from the list of possible ones
    :return: (int, int)
    """
    moves=the_board.legal_moves(color)
    bestscore  = float('-inf')
    return_move=moves[0]
    for move in moves:
        newboard= deepcopy(the_board)
        newboard.process_move(move, color)
        score=min_value(newboard.opponent(color),float('-inf'),float('inf'),newboard,ply-1)
        if score>bestscore:
            bestscore=score
            return_move=move
    return return_move
    
def max_value(color, alpha, beta, the_board,ply):
    """
    Returns a max utility valor for minimax
    :return: float
    """
    if len(the_board.legal_moves(color))==0 or ply==0:
        return heuristic(color,the_board)
    bestscore = float('-inf')
    for move in the_board.legal_moves(color):
        newboard= deepcopy(the_board)
        newboard.process_move(move, color)
        score = min_value(newboard.opponent(color), alpha, beta, newboard,ply-1)
        if score > bestscore:
            bestscore=score
        if bestscore>=beta:
            return bestscore
        alpha=max(alpha,bestscore)
    return bestscore
    
def min_value(color, alpha, beta, the_board,ply):
    """
    Returns a min utility valor for minimax
    :return: float
    """
    if len(the_board.legal_moves(color))==0 or ply==0:
        return heuristic(color,the_board)
       
    bestscore = float('inf')
    for move in the_board.legal_moves(color):
        newboard= deepcopy(the_board)
        newboard.process_move(move, color)
        score = max_value(newboard.opponent(color), alpha, beta, newboard,ply-1)
        if score < bestscore:
            bestscore=score
        if bestscore<=beta:
            return bestscore
        beta=min(beta,bestscore)
    return bestscore

def make_move(the_board, color):
    """
    Returns a random move from the list of possible ones
    :return: (int, int)
    """
    color = board.Board.WHITE if color == 'white' else board.Board.BLACK
    legal_moves = the_board.legal_moves(color)
    return minimax_ab(color,the_board,ply_alpha) if len(legal_moves) > 0 else (-1, -1)

if __name__ == '__main__':
    start_time = time.time()

    b = board.from_file(sys.argv[1])
    f = open('move.txt', 'w')
    f.write('%d,%d' % make_move(b, sys.argv[2]))
    f.close()
    
    print("--- %s seconds ---" % (time.time() - start_time))