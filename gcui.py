'''
Created on 26 janv. 2014

@author: guill
'''
import sys, time, thread
sys.path.append( 'src/' )
import grbl_tools, grbl_protocol
import ui
from Tkinter import *

class gcui:
    def __init__( self , root ):
        self.list_gc = grbl_tools.File_to_list()
        self.protocol = grbl_protocol.grbl_protocol()
        self.root = root
        self.streaming = False
        self.stat = True
        self.varpause = False
        #thread.start_new_thread( self.status, () )
        self.envoi = self.protocol.serie.envoyer
        self.ui = ui.ui( root, self )

    def loadfile( self ):
        self.list_gc.loadfile()

    def status( self ):
        while self.stat:
            time.sleep( 0.3 )
            #self.ui.set_status( self.protocol.status.strip() )
            self.ui.status_text.set( self.protocol.status.strip() )

    def comup( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 Y" + str( self.ui.speed ) + "\n" )

    def comdown( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 Y-" + str( self.ui.speed ) + "\n" )

    def coml( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 X-" + str( self.ui.speed ) + "\n" )

    def comr( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 X" + str( self.ui.speed ) + "\n" )

    def comzup( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 Z" + str( self.ui.speed ) + "\n" )

    def comzdown( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G91\nG21\nG00 Z-" + str( self.ui.speed ) + "\n" )

    def gohome( self, event ):
        if self.protocol.streaming == False:
            self.envoi( "G90\nG21\nG00 Z2.000\nG00 X0.000 Y0.000\nG00 Z0.000" + "\n" )

    def exit( self ):
        self.protocol.stop_liaison()
        self.stat = False
        time.sleep( 0.5 )
        self.root.quit()

    def sethome( self, event ):
        if self.streaming == False:
            if virtualhome == False:
                Connec.writelines( "G92 X0.000 Y0.000 Z0.000\n" )
                Connec.flushInput()
                virtualhome = True
                afficheText( "G92 X0.000 Y0.000 Z0.000" + "\n" )
            else:
                virtualhome = False
                Connec.writelines( "G92.1\n" )
                Connec.flushInput()
                afficheText( "G92.1" + "\n" )

    def pause( self, event ):
        if self.varpause == False:
            self.varpause = True
            self.protocol.serie.envoyer( "!" )
            print "PAUSE" + "\n"
            return
        if self.varpause == True:
            self.varpause = False
            self.protocol.serie.envoyer( "~" )
            print "GO" + "\n"

    def gcodestream( self, event ):
        if self.protocol.streaming == False:
            if not self.list_gc.fileisload():
                self.loadfile()
            if self.list_gc.fileisload():
                self.protocol.streaming = True
                thread.start_new_thread( self.stream, () )

    def stream( self ):
        list = self.list_gc.get_Glist()
        self.ui.set_color_bg( "green" )
        for line in list:
            self.protocol.add_commande( line.strip() )
        while self.protocol.pile.__len__() > 0 or self.protocol.liste_attente.__len__() > 0:
            print self.protocol.liste_attente.__len__()
            time.sleep( 1 )
        self.protocol.streaming = False
        self.ui.set_color_bg( "yellow" )


    def stops( self, event ):
        if self.protocol.streaming == True:
            self.protocol.pile.clear()

    def quit( self, event ):
        if self.streaming == False:
            if tkMessageBox.askokcancel( "Quit?", "Are you sure you want to quit?" ):
                self.protocol.stop_liaison()
                self.stat = False
                time.sleep( 0.5 )
                Connec.close()
                root.quit()

    def resetg( event ):
        if self.streaming == False:
            Connec.writelines( "\030" )

if __name__ == "__main__":
    root = Tk()
    test = gcui( root )
    root.mainloop()
