'''
A library of move logic functions. Move logic can be directly incorporated into
a bot class or it may be placed here. Remember to pass all information that the
method needs to find a move as arguments.

The X axis of the board increases to the right, the Y axis increases downwards.
'''

import random

def are_same_color(c1, c2, c3, board):
    '''
    This will return True if the gems at each of the x,y coordinates have
    the same color on the current board (False if not). A basic use case
    would be to pass three gem positions to see if they are the same color
    to determine if there is a possible match.
    
    e.g.    are_same_color([[x1,y1], [x2,y2], [x3,y3]])
    '''
    #Negative indices are valid in python, but not in the case of a game
    #board. Return False if a negative index has been passed
    coords = [c1, c2, c3]
    for coord in coords:
        if coord[0] < 0 or coord[1] < 0:
            return False
    #Start color checking, here we also discard indices which are too large
    try:
        #Refer to python's documentation about sets and frozensets if this
        #use of set() is unfamiliar
        #http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        colors = set([board[c[0]][c[1]] for c in coords])
        if len(colors) == 1:
            return True
        else:
            return False
    except IndexError:
        return False


def random_move(board, gem_keys, swap):
        '''
        The bare minimum approach to any game. This method will make a random
        move on the Bejeweled Blitz game board. It is a useful fallback if
        smarter code fails to find anything to do.
        '''
        #Get random indices
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        #Pick a random direction
        direction = random.choice(['up', 'left', 'down', 'right'])
        #Each condition has a quick boundary check
        if direction == 'up' and j-1 > -1:
            self.swap(gem_keys[i][j], gem_keys[i][j-1])
        elif direction == 'left' and i-1 > -1:
            self.swap(gem_keys[i][j], gem_keys[i-1][j])
        elif direction == 'down' and j+1 < 8:
            self.swap(gem_keys[i][j], gem_keys[i][j+1])
        elif direction == 'right' and i+1 < 8:
            swap(gem_keys[i][j], gem_keys[i+1][j])
        else:  # Random move was not valid, try again
            #Recursive implementation, invalid moves should be rare enough
            random_move()
            

def basic_detect_three(board, gem_keys, swap):
    '''
    This move logic is simple and can certainly be improved, even small tweaks
    might make a statistical performance difference.
    
    Assuming that the bot read the board perfectly and was not confused by any
    special effects or special gems, this method will always find a move. It
    might help to think about why this is true.
    '''
    for i in xrange(8):
        for j in xrange(8):
            #Sorted by the way the gem moves
            #Moves left (i - 1)
            if are_same_color([i-3, j], [i-2, j], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i-1][j])
                #return None
                continue
            elif are_same_color([i-1, j-1], [i-1, j-2], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i-1][j])
                #return None
                continue
            elif are_same_color([i-1, j+1], [i-1, j+2], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i-1][j])
                #return None
                continue
            elif are_same_color([i-1, j-1], [i-1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i-1][j])
                #return None
                continue
            #Moves up (j - 1)
            elif are_same_color([i, j-3], [i, j-2], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j-1])
                #return None
                continue
            elif are_same_color([i-2, j-1], [i-1, j-1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j-1])
                #return None
                continue
            elif are_same_color([i+2, j-1], [i+1, j-1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j-1])
                #return None
                continue
            elif are_same_color([i-1, j-1], [i+1, j-1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j-1])
                #return None
                continue
            #Moves right (i + 1)
            elif are_same_color([i+3, j], [i+2, j], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i+1][j])
                #return None
                continue
            elif are_same_color([i+1, j-2], [i+1, j-1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i+1][j])
                #return None
                continue
            elif are_same_color([i+1, j+2], [i+1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i+1][j])
                #return None
                continue
            elif are_same_color([i+1, j-1], [i+1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i+1][j])
                #return None
                continue
            #Moves down (j + 1)
            elif are_same_color([i, j+3], [i, j+2], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j+1])
                #return None
                continue
            elif are_same_color([i-2, j+1], [i-1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j+1])
                #return None
                continue
            elif are_same_color([i+2, j+1], [i+1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j+1])
                #return None
                continue
            elif are_same_color([i-1, j+1], [i+1, j+1], [i, j], board):
                swap(gem_keys[i][j], gem_keys[i][j+1])
                #return None
                continue