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
        self.list_gc = grbl_tools.File_to_list()                    # charge la classe gestion de fichier
        self.protocol = grbl_protocol.grbl_protocol()               # charge la classe de protocole de communication
        self.root = root
        self.streaming = False
        self.varpause = False
        self.envoi = self.protocol.serie.envoyer
        self.ui = ui.ui( root, self )                               # lance l'interface graphique
        self.virtualhome = False

    def loadfile( self ):
        """
        @loadfile
            recupre une liste charger a partir d'un fichier gcode 
        """
        self.list_gc.loadfile()

    def control_( self ):
        """
        @control_
            verifie si grbl est en coord relative pour le mode jog
            et si la ma chiene est en mm
        """
        if self.protocol.grbl_stat.absolut != 'G91':
            self.envoi( 'G91\n' )
        if self.protocol.grbl_stat.metric != 'G21':
            self.envoi( 'G21\n' )

    #===========================================================================
    #  Commande en temps reel
    #===========================================================================

    def comup( self, event ):
        """
        @comup
            deplacement  +Y
        """
        if self.protocol.streaming == False:
            if self.protocol.grbl_stat.absolut == 'G91':
                self.control_()
                self.envoi( "G00 Y" + str( self.ui.speed ) + "\n" )

    def comdown( self, event ):
        """
        @comdown
            deplacement  -Y
        """
        if self.protocol.streaming == False:
            self.control_()
            self.envoi( "G00 Y-" + str( self.ui.speed ) + "\n" )

    def coml( self, event ):
        """
        @coml
            deplacement -X
        """
        if self.protocol.streaming == False:
            self.control_()
            self.envoi( "G00 X-" + str( self.ui.speed ) + "\n" )

    def comr( self, event ):
        """
        @comr
            deplacement -X
        """
        if self.protocol.streaming == False:
            self.control_()
            self.envoi( "G00 X" + str( self.ui.speed ) + "\n" )

    def comzup( self, event ):
        """
        @comzup
            depalcement +Z
        """
        if self.protocol.streaming == False:
            self.control_()
            self.envoi( "G00 Z" + str( self.ui.speed ) + "\n" )

    def comzdown( self, event ):
        """
        @comzdown
            depalcement -Z
        """
        if self.protocol.streaming == False:
            self.control_()
            self.envoi( "G00 Z-" + str( self.ui.speed ) + "\n" )

    def gohome( self, event ):
        """
        @gohome
            retourne au point zero
        """
        if self.protocol.streaming == False:
            self.envoi( "G90\nG21\nG00 Z2.000\nG00 X0.000 Y0.000\nG00 Z0.000" + "\n" )

#    def status( self, event ):
#        if self.protocol.streaming == False:
#            self.envoi( "$G\n" )

    def sethome( self, event ):
        """
        @sethome
            assigne le point zero virtuel
        """
        if self.streaming == False:
            if self.virtualhome == False:
                self.envoi( "G92 X0.000 Y0.000 Z0.000\n" )
                self.virtualhome = True
                #afficheText( "G92 X0.000 Y0.000 Z0.000" + "\n" )
            else:
                self.virtualhome = False
                self.envoi( "G92.1\n" )
                #afficheText( "G92.1" + "\n" )

    def pause( self, event ):
        """
        @pause
            met grbl en pause
        """
        if self.varpause == False:
            #self.ui.set_color_bg( "gray" )
            self.varpause = True
            self.protocol.serie.envoyer( "!" )
            print "PAUSE" + "\n"
            return
        if self.varpause == True:
            #self.ui.set_color_bg( "green" )
            self.varpause = False
            self.protocol.serie.envoyer( "~" )
            print "GO" + "\n"

    def stops( self, event ):
        """
        @stops
            met fin au stream. grbl termine les commandes dans le buffer
        """
        if self.protocol.streaming == True:
            #self.ui.set_color_bg( "red" )
            self.protocol.pile.clear()
            self.protocol.streaming == False

    def resetg( self, event ):
        if self.streaming == False:
            self.envoi( "\030" )
    #===========================================================================
    # FIN
    #===========================================================================

    def gcodestream( self, event ):
        if self.protocol.streaming == False:
            if not self.list_gc.fileisload():
                self.loadfile()
            if self.list_gc.fileisload():
                self.protocol.streaming = True
                self.protocol.serie.Connec.flushInput()
                self.protocol.pile.clear()
                thread.start_new_thread( self.stream, () )

    def stream( self ):
        list = self.list_gc.get_Glist()
        self.protocol.pile.clear()
        #self.ui.set_color_bg( "green" )                 # affiche le text en vert
        for line in list:                               # pour chaque entre dans la liste 
            self.protocol.add_commande( line.strip() )  # ajouter la ligne dans la liste de commande a passer a grbl
        while self.protocol.pile.__len__() > 0 or self.protocol.liste_attente.__len__() > 0:  # tant que la pile ou la liste d'attente n'est pas vide
            #print self.protocol.liste_attente.__len__()
            time.sleep( 1 )                             # attendre 1 seconde
        self.protocol.streaming = False                 # une fois les differente liste vides met le flag a False
        #self.ui.set_color_bg( "yellow" )                # change la couleur a jaune

    def exit( self ):
        self.protocol.stop_liaison()
        time.sleep( 0.2 )
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    test = gcui( root )
    root.mainloop()
