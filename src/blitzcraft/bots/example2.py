from blitzcraft.blitzbot import BlitzBot
import blitzcraft.logic as logic

class MyBot(BlitzBot):
    '''A bot of my own'''
    
    def __init__(self):
        BlitzBot.__init__(self)
        print('Running my own bot based on BlitzBot')

    #Here I have overridden the parent class' method for reading the board to
    #allow it to average pixel data for a piece of each gem instead of using
    #only a single gem.
    def read_blitz_board(self):
        '''
        Takes a screenshot of the game window containing the gems and extracts
        pixel data in order to compile a fresh 8x8 array for self.board. This
        method uses a 4x4 pixel window for each gem and uses the average RGB.
        '''
        #We only need a minimal screenshot which contains all the gem pixels
        upper = self.gem_keys[0][0]
        lower = self.gem_keys[7][7]
        screen = self.screenshot(upper, lower, buffer=4)
        #Iterate over our gem key positions in order to color the board
        board = []
        for i in self.gem_keys:  # X dimension
            board_col = []
            for j in i:  # Y dimension
                gem_x, gem_y = j[0], j[1]
                #Extract a 4x4 pixel slice
                slice = []
                for a in xrange(4):
                    col = []
                    for b in xrange(4):
                        gem_pixel = screen[gem_y-upper[1]+a][gem_x-upper[0]+b]
                        col.append(gem_pixel)
                    slice.append(col)
                board_col.append(self.determine_average_color(slice))
            board.append(board_col)
        self.board = board

    def make_move(self):
        logic.basic_detect_three(self.board, self.gem_keys, self.swap)

m = MyBot()
m.play()