from Tkinter import *
import ttk, tkMessageBox, grbl_tools

class ui:
    def __init__( self , root, gcui ):
        self.gcui = gcui
        self.root = root
        self.protocole = gcui.protocol
        self.speed = 0.10
        root.resizable( width=False, height=False )
        root.title( 'CncGui' )
        self.status_text = StringVar()

        self.lTitre = Label( root, text="INSTRUCTIONS", fg="red" )

        self.lCommandes = Label( root, text="1: \n2: \n3: \n\narrow keys: \npage up & page down: \n\nh: \nt: \nr: \ng: \np: \nx: \ns: ", justify=RIGHT, fg="red" )
        self.lInstruc = Label( root, text="set speed to 0.01 mm  per jog\nset speed to 0.10 mm per jog\nset speed to 1.00 mm per jog\n\njog in x-y plane\njog in z axis\n\ngo home\nset virtual home/disable\nreset grbl\nstream un     fichier g-code\nmet en pause le stream\nstop streaming g-code (this is NOT immediate)\nstatus de la machine", justify=LEFT )

        self.lStatus = Label( root, textvariable=self.status_text, fg="dark green", bg="yellow" )
        self.lJogSpeed = Label( root, text="current jog speed: " + str( self.speed ) + " mm per step" )
        self.lPortname = Label( root, text="" )

        self.menubar = Menu( root )

        self.filemenu = Menu( self.menubar, tearoff=0 )
        self.filemenu.add_command( label="Open", command=self.gcui.loadfile )
        self.filemenu.add_separator()
        self.filemenu.add_command( label="Exit", command=self.exit )
        self.menubar.add_cascade( label="File", menu=self.filemenu )

        self.CadreBar = Frame( root )
        self.cadreCom = Frame( root )
        self.cadreAffich = Frame( root )


        self.scrollAffiche = Scrollbar( self.cadreAffich )
        self.tAffiche = Text( self.cadreAffich, width=80, height=10, yscrollcommand=self.scrollAffiche.set )
        self.tAffiche.insert( INSERT, "cncgui v0.1 \n" )
        self.tAffiche.config( state=DISABLED )
        self.varcombo = StringVar()

        self.barconf = ttk.Combobox( self.CadreBar, state='readonly', textvariable=self.varcombo )

        self.barconf["value"] = self.protocole.serie.scan()
        self.lStatusConnec = Label( self.CadreBar, text="Not Connected", fg="red" )

        self.tCommand = ttk.Entry( self.cadreCom, width=48 )
        self.bValide = Button( self.cadreCom, text="envoi"''', command=cValide ''' )
        self.bAnnule = Button( self.cadreCom, text="annule"''', command=cAnnule ''' )

        self.lTitre.grid( row=1, columnspan=2 )
        self.lCommandes.grid( row=2, column=0 )
        self.lInstruc.grid( row=2, column=1 )
        self.lStatus.grid( row=3, columnspan=2 )
        self.lJogSpeed.grid( row=4, columnspan=2 )
        self.cadreCom.grid( row=5, columnspan=4 )
        self.cadreAffich.grid( row=6, columnspan=4 )
        self.lPortname.grid( row=8, columnspan=1 )
        self.CadreBar.grid( row=9, columnspan=4 )

        self.tCommand.pack( side=LEFT )
        self.bValide.pack( side=LEFT )
        self.bAnnule.pack( side=LEFT )

        self.tAffiche.pack( side=LEFT, fill=BOTH )
        self.scrollAffiche.pack( side=RIGHT, fill=Y )
        self.scrollAffiche.config( command=self.tAffiche.yview )

        self.barconf.pack( side=LEFT )
        self.lStatusConnec.pack( side=LEFT )
        self.lStatus.focus_set()

        root.grid_rowconfigure( 0, weight=1 )
        root.grid_columnconfigure( 3, weight=1 )
        self.lStatus.bind( '1', self.__set_speed0__ )
        self.lStatus.bind( '2', self.__set_speed1__ )
        self.lStatus.bind( '3', self.__set_speed2__ )

        self.lStatus.bind( '<Up>', self.gcui.comup )
        self.lStatus.bind( '<Down>', self.gcui.comdown )
        self.lStatus.bind( '<Left>', self.gcui.coml )
        self.lStatus.bind( '<Right>', self.gcui.comr )
        self.lStatus.bind( '<Next>', self.gcui.comzdown )
        self.lStatus.bind( '<Prior>', self.gcui.comzup )
#
        self.lStatus.bind( '<h>', self.gcui.gohome )
#        self.lStatus.bind( '<t>', sethome )
        self.lStatus.bind( '<p>', self.gcui.pause )
        self.lStatus.bind( '<g>', self.gcui.gcodestream )
#        self.lStatus.bind( '<q>', quit )
#        self.lStatus.bind( '<r>', resetg )
        #root.bind_all( '<s>', status )
#        self.lStatus.bind( '<x>', stops )
        root.protocol( "WM_DELETE_WINDOW", self.exit )
        self.barconf.bind( '<<ComboboxSelected>>', self.serialConnec )
        root.config( menu=self.menubar )

    def setlabel( self ):
        self.lJogSpeed.config( text="current jog speed: " + str( self.speed ) + " mm per step" )

    def exit( self ):
        if tkMessageBox.askokcancel( "Quit?", "Are you sure you want to quit?" ):
            self.gcui.exit()


    def __set_speed0__( self, event ):
        self.speed = 0.01
        self.setlabel()

    def __set_speed1__( self, event ):
        self.speed = 0.10
        self.setlabel()

    def __set_speed2__( self, event ):
        self.speed = 1.00
        self.setlabel()

    def get_speed( self ):
        return self.speed

    def serialConnec( self, event ):
        self.lStatus.focus_set()
        #print self.varcombo.get()
        if self.protocole.serie.Connec.getPort() != None:
            self.protocole.serie.Connec.close()
            #print self.varcombo.get()
            if self.varcombo.get() != "":
                if self.protocole.serie.set_port( self.varcombo.get() ):
                    self.lStatusConnec.config( text="connected", fg="green" )
                    self.protocole.start_liaison( self.status_text )
                    #tAffiche.
                else:
                    self.lStatusConnec.config( text="not connected", fg="red" )
        else:
            if self.varcombo.get() != "":
                if self.protocole.serie.set_port( self.varcombo.get() ):
                    self.lStatusConnec.config( text="connected", fg="green" )
                    self.protocole.start_liaison( self.status_text )
                    #tAffiche.
                else:
                    self.lStatusConnec.config( text="not connected", fg="red" )

    def set_status( self, ftext ):
        self.lStatus.config( text=ftext )

    def set_color_bg( self, colorbg ):
        self.lStatus.config( bg=colorbg )

if __name__ == "__main__":
    testa = gcode_parser.gcode_parser()
    test = ui( testa )
    test.root.mainloop()
