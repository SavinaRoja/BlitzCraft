

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
