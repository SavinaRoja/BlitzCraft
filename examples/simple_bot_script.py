from blitzcraft import BlitzBot
import blitzcraft.logic as logic


class MyBot(BlitzBot):
    """A custom class based on BlitzBot"""
    #I need to override the make_move function to make it smarter
    def make_move(self):
        #First check for 5-in-a-row
        if not logic.basic_detect_five(self.board, self.gem_keys, self.swap):
            #Failing that, check for 4-in-a-row
            if not logic.basic_detect_four(self.board, self.gem_keys, self.swap):
                #Failing that, check for 3-in-a-row
                logic.basic_detect_three(self.board, self.gem_keys, self.swap)
        #Always make a random move every time make_move is called, this can help
        #get us unstuck if that happens
        self.random_move()

#Initialize the custom bot class
b = MyBot()
#Set the time delay for each click to 0.08 seconds
b.delay = 0.08
#Pick the boosts I like, up to three
boosts = [4, 5]  # Use time boost and bonus multiplier
#Bejeweled Blitz can pop up all sorts of messages, make sure you click *up to*
#the point where you select the boosts before playing
#Pass the list of boosts into the play function call, play begins!
b.play(boosts)
