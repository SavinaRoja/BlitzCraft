import sys
import gtk.gdk

### Screenshot methods for different platforms ###
def mac_screenshot():
    '''
    Takes a screenshot on a mac platform.
    
    This method expects coordinates for the upper left corner of the game
    window and the lower right. These should be provided as a pair either
    as a list, [x,y] or as a tuple, (x,y). A buffer may be specified and its
    integer value will be used to extend the screenshot's length and width.
    '''
    #I REALLY don't know how to do this yet
    pass

def windows_screenshot():
    '''
    Takes a screenshot on a windows platform.
    
    This method expects coordinates for the upper left corner of the game
    window and the lower right. These should be provided as a pair either
    as a list, [x,y] or as a tuple, (x,y). A buffer may be specified and its
    integer value will be used to extend the screenshot's length and width.
    '''
    #I don't know how I want to do this yet
    pass

def unix_screenshot(upper_left=[0,0], lower_right=[1,1], buffer=1, save=False):
    '''
    
    Takes a screenshot on a unix/linux platform.
    
    This method expects coordinates for the upper left corner of the game
    window and the lower right. These should be provided as a pair either
    as a list, [x,y] or as a tuple, (x,y) .A buffer may be specified and its
    integer value will be used to extend the screenshot's length and width.
    
    This method returns a NumPy array of the pixels in the screenshot, be
    aware that the array will invert the axes to (y,x) and the indices will
    begin at 0.
    '''
    #Get individual coordinates
    ul_x, ul_y = upper_left[0], upper_left[1]
    lr_x, lr_y = lower_right[0], lower_right[1]
    #Get the gtk.gdk window
    w = gtk.gdk.get_default_root_window()
    size = (lr_x - ul_x + buffer, lr_y - ul_y + buffer)
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,size[0],size[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),ul_x,ul_y,0,0,size[0],size[1])
    #You can save the images with code like:
    if save:
        pb.save('test.png', 'png')
    #Returns the NumPy array, axes are inverted (y,x)
    return pb.get_pixels_array()
    

def define_game_window(mouse):
    '''
    Asks for user input to define the dimension of the game window; writes
    these dimensions to the blitz_window.txt file.
    '''
    
    #Get the upper left corner
    print('''\nPlease place the mouse on the upper left hand corner of the \
Bejeweled Blitz game window. Then press Enter.\n''')
    raw_input('Upper left corner: ')
    mouse_x1, mouse_y1 = mouse.position()
    print('(X: {0}, Y: {1})'.format(mouse_x1, mouse_y1))
    
    #Get the lower right corner
    print('''\nNow place the mouse on the lower right hand corner of the \
Bejeweled Blitz game window. Then press Enter.\n''')
    raw_input('Lower right corner: ')
    mouse_x2, mouse_y2 = mouse.position()
    #Get the upper left corner
    print('(X: {0}, Y: {1})'.format(mouse_x2, mouse_y2))
    
    #Ask if these should be saved
    print('Would you like to save these coordinates?')
    if raw_input('[y/N] ') in ['y', 'Y']:
        with open('blitz_window.txt', 'w') as out:
            for i in [mouse_x1, ',', mouse_y1, '\n', mouse_x2, ',', mouse_y2]:
                out.write(str(i))
        return True
    else:
        return False

### For different platforms, load up different methods ###
if sys.platform == 'darwin':  # Mac
    screenshot = mac_screenshot
elif sys.platform == 'win32':  # Windows
    screenshot = windows_screenshot
else:  # Unix/Linux
    screenshot = unix_screenshot
