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
        self.stat = self.protocole.stat_coord

        #=======================================================================
        # config menu
        #=======================================================================
        self.menubar = Menu( root )

        self.filemenu = Menu( self.menubar, tearoff=0 )
        self.filemenu.add_command( label="Open", command=self.gcui.loadfile )
        self.filemenu.add_separator()
        self.filemenu.add_command( label="Exit", command=self.exit )
        self.menubar.add_cascade( label="File", menu=self.filemenu )
        self.helpmenu = Menu( self.menubar, tearoff=0 )
        self.helpmenu.add_command( label='Help', command=self.help )
        self.menubar.add_cascade( label='?', menu=self.helpmenu )
        root.config( menu=self.menubar )


        #=======================================================================
        # frame bot
        #=======================================================================
        self.CadreBar = Frame( root )

        self.varcombo = StringVar()
        self.barconf = ttk.Combobox( self.CadreBar, state='readonly', textvariable=self.varcombo )
        self.barconf["value"] = self.protocole.serie.scan()
        self.lStatusConnec = Label( self.CadreBar, text="Not Connected", fg="red" )
        self.barconf.pack( side=LEFT )
        self.lStatusConnec.pack( side=LEFT )

        #=======================================================================
        # frame text output
        #=======================================================================
        self.cadreAffich = Frame( root )

        self.scrollAffiche = Scrollbar( self.cadreAffich )
        self.tAffiche = Text( self.cadreAffich, yscrollcommand=self.scrollAffiche.set )
        self.tAffiche.insert( INSERT, "cncgui v0.2 \n" )
        self.tAffiche.config( state=DISABLED )
        self.tAffiche.pack( side=LEFT, expand=1, fill=BOTH )
        self.scrollAffiche.pack( side=RIGHT, fill=Y )
        self.scrollAffiche.config( command=self.tAffiche.yview )



        #=======================================================================
        # frame status
        #=======================================================================

        self.lMC_lx = Label( self.root, text="X:", relief=RIDGE )


        self.lMC_x = Label( self.root, textvariable=self.stat.mc_x, font=( "Purisa", 28 ), fg="gray", relief=RIDGE )

        self.lMC_ly = Label( self.root, text="Y:", relief=RIDGE )
        self.lMC_y = Label( self.root, textvariable=self.stat.mc_y, font=( "Purisa", 28 ), fg="gray", relief=RIDGE )

        self.lMC_lz = Label( self.root, text="Z:", relief=RIDGE )
        self.lMC_z = Label( self.root, textvariable=self.stat.mc_z, font=( "Purisa", 28 ), fg="gray", relief=RIDGE )

        self.lTC_lx = Label( self.root, text="X:", relief=RIDGE )
        self.lTC_x = Label( self.root, textvariable=self.stat.tc_x, font=( "Purisa", 28 ), fg="steel blue", relief=RIDGE )

        self.lTC_ly = Label( self.root, text="Y:", relief=RIDGE )
        self.lTC_y = Label( self.root, textvariable=self.stat.tc_y, font=( "Purisa", 28 ), fg="steel blue", relief=RIDGE )

        self.lTC_lz = Label( self.root, text="Z:", relief=RIDGE )
        self.lTC_z = Label( self.root, textvariable=self.stat.tc_z, font=( "Purisa", 28 ), fg="steel blue", relief=RIDGE )

        self.lMachineCoord = Label( self.root, text="Position Machine", font=( "Purisa", 28 ), fg="gray", relief=RIDGE )
        self.lTravailCoord = Label( root, text="Position Travail", font=( "Purisa", 28 ), fg="steel blue", relief=RIDGE )

        self.lTravailStatus = Label( root, textvariable=self.stat.status_travail, font=( "Purisa", 28 ), fg="gray", relief=RIDGE )

        self.lJogSpeed = Label( root, text="current jog speed: " + str( self.speed ) + " mm per step" )


        #=======================================================================
        # agencement
        #=======================================================================
        self.lMachineCoord.grid( row=0, column=0, columnspan=2, sticky=W + E + N + S )
        self.lTravailCoord.grid( row=0, column=2, columnspan=2, sticky=W + E + N + S )

        self.lMC_lx.grid( row=1, column=0, sticky=W + E + N + S )
        self.lMC_x.grid( row=1, column=1, sticky=W + E + N + S )
        self.lTC_lx.grid( row=1, column=2, sticky=W + E + N + S )
        self.lTC_x.grid( row=1, column=3, sticky=W + E + N + S )

        self.lMC_ly.grid( row=2, column=0, sticky=W + E + N + S )
        self.lMC_y.grid( row=2, column=1, sticky=W + E + N + S )
        self.lTC_ly.grid( row=2, column=2, sticky=W + E + N + S )
        self.lTC_y.grid( row=2, column=3, sticky=W + E + N + S )

        self.lMC_lz.grid( row=3, column=0, sticky=W + E + N + S )
        self.lMC_z.grid( row=3, column=1, sticky=W + E + N + S )
        self.lTC_lz.grid( row=3, column=2, sticky=W + E + N + S )
        self.lTC_z.grid( row=3, column=3, sticky=W + E + N + S )

        self.lTravailStatus.grid( row=4, column=0, columnspan=4, sticky=W + E + N + S )

        self.lJogSpeed.grid( row=5, columnspan=4, sticky=S + N )
        self.cadreAffich.grid( row=6, columnspan=4, sticky=W + E + N + S )
        self.CadreBar.grid( row=7, columnspan=4, sticky=S )



        root.grid_rowconfigure( 6, weight=100 )
        root.grid_columnconfigure( 0, weight=1 )
        root.grid_columnconfigure( 1, weight=2 )
        root.grid_columnconfigure( 2, weight=1 )
        root.grid_columnconfigure( 3, weight=2 )

        self.root.bind( '1', self.__set_speed0__ )
        self.root.bind( '2', self.__set_speed1__ )
        self.root.bind( '3', self.__set_speed2__ )

        self.root.bind( '<Up>', self.gcui.comup )
        self.root.bind( '<Down>', self.gcui.comdown )
        self.root.bind( '<Left>', self.gcui.coml )
        self.root.bind( '<Right>', self.gcui.comr )
        self.root.bind( '<Next>', self.gcui.comzdown )
        self.root.bind( '<Prior>', self.gcui.comzup )
#
        self.root.bind( '<h>', self.gcui.gohome )
        self.root.bind( '<t>', self.gcui.sethome )
        self.root.bind( '<p>', self.gcui.pause )
        self.root.bind( '<g>', self.gcui.gcodestream )
#        self.lStatus.bind( '<q>', quit )
        self.root.bind( '<r>', self.gcui.resetg )
#        self.lStatus.bind( '<s>', self.gcui.status )
        self.root.bind( '<x>', self.gcui.stops )
        root.protocol( "WM_DELETE_WINDOW", self.exit )
        self.barconf.bind( '<<ComboboxSelected>>', self.serialConnec )


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
    #===========================================================================
    # a modifier
    #===========================================================================
    def serialConnec( self, event ):
        if self.protocole.serie.Connec.getPort() != None:
            if self.protocole.liaison_active: self.protocole.stop_liaison()
            if self.varcombo.get() != "Deconnexion":
                if self.protocole.serie.set_port( self.varcombo.get() ):
                    self.lStatusConnec.config( text="connected", fg="green" )
                    self.protocole.start_liaison( self.afficheText )
                else:
                    self.lStatusConnec.config( text="not connected", fg="red" )
            else:
                self.lStatusConnec.config( text="not connected", fg="red" )
        else:
            if self.varcombo.get() != "Deconnexion":
                if self.protocole.serie.set_port( self.varcombo.get() ):
                    self.lStatusConnec.config( text="connected", fg="green" )
                    self.protocole.start_liaison( self.afficheText )
                else:
                    self.lStatusConnec.config( text="not connected", fg="red" )
            else:
                self.lStatusConnec.config( text="not connected", fg="red" )

    #===========================================================================
    # def set_color_bg( self, colorbg ):
    #     self.lStatus.config( bg=colorbg )
    #===========================================================================

    def afficheText( self, text ):
        self.tAffiche.config( state=NORMAL )
        self.tAffiche.insert( END, text )
        self.tAffiche.config( state=DISABLED )
        self.tAffiche.yview( END )

    def help( self ):
        tkMessageBox.showinfo( 
            "Help",
            "1:            " + "set speed to 0.01 mm  per jog\n" +
            "2:            " + "set speed to 0.10 mm per jog\n" +
            "3:            " + "set speed to 1.00 mm per jog\n\n" +
            "arrow keys:   " + "jog in x-y plane\n" +
            "page up & page down:" + "jog in z axis\n\n" +
            "h:            " + "go home\n" +
            "t:            " + "set virtual home/disable\n" +
            "r:            " + "reset grbl\n" +
            "g:            " + "stream un     fichier g-code\n" +
            "p:            " + "met en pause le stream\n" +
            "x:            " + "stop streaming g-code (this is NOT immediate)\n" +
            "s:            " + "status de la machine"
        )

if __name__ == "__main__":
    testa = gcode_parser.gcode_parser()
    test = ui( testa )
    test.root.mainloop()
