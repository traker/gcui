import tkFileDialog
from serial.tools.list_ports_windows import *


class File_to_list:
    def __init__( self ):
        self.Glist = []
        self.loadingFile = False

    def toList( self, text ):
        nb = 0
        for line in text:
            self.Glist.append( line )
            nb += 1

    def loadfile( self ):
        file = tkFileDialog.askopenfile( mode='rb', title='Choose a file', filetypes=[( 'numeric command', '*.nc' ), ( 'gcode', '*.gc' )] )
        if file != None:
            filegcode = file.readlines()
            self.loadingFile = True
            file.close()
            self.toList( filegcode )

    def unload( self ):
        self.Glist = []
        self.loadingFile = False

    def get_Glist( self ):
        return self.Glist

    def fileisload( self ):
        return self.loadingFile

