'''
This implements the base class for a BlitzCraft bot player. It won't do very
well at playing the game, but it provides all the basics which can be extended
by another bot.
'''

import sys
import time
import random
import pymouse
import gtk.gdk
import utils

class BlitzBot(object):
    '''The base class for a BlitzCraft bot'''
    def __init__(self, delay=0.1):
        self.delay = delay
        self.mouse = pymouse.PyMouse()
        self.screenshot = utils.screenshot
        self.define_window()
        self.define_keys()
        self.initialize_board()

    def play(self, boosts=[]):
        '''
        Call this function when ready to begin a game of Blitz. Typically one
        will need to bring the game to the point of picking boosts before
        starting the play.
        '''
        self.pick_boosts(boosts)
        self.left_click(self.start_key)
        if 4 in boosts:  # The 5 second time extension boost is selected
            duration = 70
        else:
            duration = 65
        #Wait a bit for the game to start
        time.sleep(1)
        #Timer for the game
        start = time.time()
        end = time.time() + duration
        #Play until time is up
        while time.time() < end:
            self.read_blitz_board()
            self.make_move()

    def pick_boosts(self, boost_nums=[]):
        '''
        Clicks on the boosts provided, note that only three boosts may be
        selected at any given time, so providing more than three is a waste.
        '''
        for boost in boost_nums:
            self.left_click(self.boost_keys[boost])

    def define_window(self):
        '''
        This method is used to acquire the location of the game window for
        the bot to be able to dynamically calculate the correct positions
        for various actions.
        '''
        #Read the game area dimensions from blitz_window.txt, quit if undefined
        try:
            blitz_window = open('blitz_window.txt', 'r')
        except IOError:
            print('blitz_window.txt not found. Define the game window now?')
            if raw_input('[y/N] ') in ['y', 'Y']:  # Define the window
                if utils.define_game_window(self.mouse):
                    #Parse the blitz_window.txt file
                    with open('blitz_window.txt', 'r') as blitz_window:
                        fl, sl = blitz_window.readlines()
                        self.upper_x, self.upper_y = [int(i) for i in fl.split(',')]
                        self.lower_x, self.lower_y = [int(i) for i in sl.split(',')]
                else:  # Quits if canceled
                    print('Aborting BlitzBot initialization...')
                    sys.exit(0)  # Quits
            else:  # Do not define the window
                print('Aborting BlitzBot initialization...')
                sys.exit(0)  # Quits
        else:
            #Parse the blitz_window.txt file
            fl, sl = blitz_window.readlines()
            self.upper_x, self.upper_y = [int(i) for i in fl.split(',')]
            self.lower_x, self.lower_y = [int(i) for i in sl.split(',')]
            blitz_window.close()

    def redefine_window(self):
        '''Like define_window except it assumes you want to overwrite it'''
        if utils.define_game_window(self.mouse):
            with open('blitz_window.txt', 'r') as blitz_window:
                fl, sl = blitz_window.readlines()
                self.upper_x, self.upper_y = [int(i) for i in fl.split(',')]
                self.lower_x, self.lower_y = [int(i) for i in sl.split(',')]
            self.define_keys()
            

    def define_keys(self):
        '''
        Once the BlitzBot has acquired the screen pixel coordinates for the
        upper left and lower right corners of the game window, this method
        initializes the locations for important click positions.
        '''
        #Calculate width and length
        self.width = self.lower_x - self.upper_x
        self.length = self.lower_y - self.upper_y
        #Calculate start_key position
        sk_x = int(round(0.353 * self.width)) + self.upper_x
        sk_y = int(round(0.664 * self.length)) + self.upper_y
        self.start_key = [sk_x, sk_y]
        #Calculate boost_keys positions
        self.boost_keys = []
        for i in range(5):
            bk_x = int(round((0.102 + 0.082 * i) * self.width)) + self.upper_x
            bk_y = int(round(0.51 * self.length)) + self.upper_y
            self.boost_keys.append([bk_x, bk_y])
        #Calculate gem_keys positions as a 2D array of points
        gem_keys = []
        for i in range(8):
            col = []
            for j in range(8):
                x = int(round(self.upper_x + (((0.0525 * i) + 0.254) * self.width)))
                y = int(round(self.upper_y + (((0.0654 * j) + 0.210 ) * self.length)))
                col.append((x,y))
            gem_keys.append(tuple(col))
        self.gem_keys = tuple(gem_keys)
        #self.gem_keys has been cast as tuple at all levels to prevent
        #accidental modification

    def initialize_board(self):
        ''''Create an 8x8 list for self.board'''
        #This is a python "list comprehension"
        #Initializes the board structure as all gray
        self.board = [['gray'] * 8 for i in xrange(8)]

    def read_blitz_board(self):
        '''
        Takes a screenshot of the game window containing the gems and extracts
        pixel data in order to compile a fresh 8x8 array for self.board
        '''
        #We only need a minimal screenshot which contains all the gem pixels
        upper = self.gem_keys[0][0]
        lower = self.gem_keys[7][7]
        screen = self.screenshot(upper, lower)
        #Iterate over our gem key positions in order to color the board
        board = []
        for i in self.gem_keys:  # X dimension
            board_col = []
            for j in i:  # Y dimension
                gem_x, gem_y = j[0], j[1]
                #Extract a single pixel, remembering to invert the axes
                gem_pixel = screen[gem_y - upper[1]][gem_x - upper[0]]
                board_col.append(self.determine_pixel_color(gem_pixel))
            board.append(board_col)
        self.board = board

    def make_move(self):
        '''The master control function for making a move.'''
        self.random_move()

    def left_click(self, coords):
        '''
        Applies a left click from the mouse at the given coordinate pair. It
        will sleep for a period specified by the BlitzBot's delay attribute
        after executing the click.
        '''
        self.mouse.press(coords[0], coords[1])
        self.mouse.release(coords[0], coords[1])
        time.sleep(self.delay)

    def swap(self, coords1, coords2):
        '''
        Swaps the gems at the provided coordinates. Sleeps according to
        self.delay afterwards.
        '''
        self.mouse.press(coords1[0], coords1[1])
        self.mouse.release(coords1[0], coords1[1])
        self.mouse.press(coords2[0], coords2[1])
        self.mouse.release(coords2[0], coords2[1])
        time.sleep(self.delay)

    def random_move(self):
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
            self.swap(self.gem_keys[i][j], self.gem_keys[i][j-1])
        elif direction == 'left' and i-1 > -1:
            self.swap(self.gem_keys[i][j], self.gem_keys[i-1][j])
        elif direction == 'down' and j+1 < 8:
            self.swap(self.gem_keys[i][j], self.gem_keys[i][j+1])
        elif direction == 'right' and i+1 < 8:
            self.swap(self.gem_keys[i][j], self.gem_keys[i+1][j])
        else:  # Random move was not valid, try again
            #Recursive implementation, invalid moves should be rare enough
            self.random_move()

    def determine_pixel_color(self, (r,g,b)):
        '''
        Determines the color of a pixel. This code adapted from dotOrion's
        BejeweledBot. https://github.com/dotOrion/BejeweledBot
        Returns a string value based on the RGB number values of the pixel.
        '''
        if r > 192 and g < 64 and b < 64:
            return "red"
        elif r > 127 and g < 127 and b > 127:
            return "purple"
        elif r > 192 and g > 192 and b < 64:
            return "yellow"
        elif r > 192 and g < 192 and b < 64:
            return "orange"
        elif r < 64 and g < 192 and b > 192:
            return "blue"
        elif r < 64 and g > 127 and b < 64:
            return "green"
        elif r == g == b:
            return "white"
        else:
            return "gray"

    def determine_average_color(self, pix_array):
        '''
        This method should work on any 2D array of pixels; it will average the
        RGB values of every pixel in the array and then return a color string
        for the average values.
        '''
        r_sum = g_sum = b_sum = 0
        pixel_count = 0
        for i in pix_array:
            for j in i:
                pixel_count += 1
                r_sum += j[0]
                g_sum += j[1]
                b_sum += j[2]
        #Divide the sums by the number of pixels summed
        r = r_sum / float(pixel_count)
        g = g_sum / float(pixel_count)
        b = b_sum / float(pixel_count)
        return self.determine_pixel_color((r,g,b))

    def are_same_color(self, coords=[]):
        '''
        This will return True if the gems at each of the x,y coordinates have
        the same color on the current board (False if not). A basic use case
        would be to pass three gem positions to see if they are the same color
        to determine if there is a possible match.
        
        e.g.    self.are_same_color([[x1,y1], [x2,y2], [x3,y3]])
        '''
        #Negative indices are valid in python, but not in the case of a game
        #board. Return False if a negative index has been passed
        for coord in coords:
            if coord[0] < 0 or coord[1] < 0:
                return False
        #Start color checking, here we also discard indices which are too large
        try:
            #Refer to python's documentation about sets and frozensets if this
            #use of set() is unfamiliar
            #http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
            colors = set([self.board[c[0]][c[1]] for c in coords])
            if len(colors) == 1:
                return True
            else:
                return False
        except IndexError:
            return False
