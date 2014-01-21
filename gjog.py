from Tkinter import *
import ttk
import serial, tkFileDialog, time, thread, tkMessageBox, os
from serial.tools.list_ports_windows import *
import sys
sys.path.append( 'src/' )


DEFAULT_BAUDRATE = 9600
speed = 0.10
streaming = False
virtualhome = False
varpause = False
Connec = serial.Serial()
Connec.port = None
Connec.baudrate = DEFAULT_BAUDRATE
_debug = 0     #active l'affichage des differentes variables
filegcode = ""
loadingfile = False

def afficheText( text ):
    tAffiche.config( state=NORMAL )
    tAffiche.insert( END, text )
    tAffiche.config( state=DISABLED )
    tAffiche.yview( END )

def getSerial( lis ):
    for l in lis:
        tempbuffer = l
        l = l + "\n"
        afficheText( tempbuffer )

def parse_xyz( s ):
    g = s.split()
    return( g )

def setlabel():
    lJogSpeed.config( text="current jog speed: " + str( speed ) + " mm per step" )

def set_speed0( event ):
    global speed
    speed = 0.01
    setlabel()

def set_speed1( event ):
    global speed
    speed = 0.10
    setlabel()

def set_speed2( event ):
    global speed
    speed = 1.00
    setlabel()

def status():
    while True:
        time.sleep( 0.5 )
        if Connec.isOpen():
            if streaming == False:
                Connec.flushInput()
                Connec.write( '?' ) # Send g-code block to grbl
                grbl_out = Connec.readline() # Wait for grbl response with carriage return
                if "MPos" in grbl_out.strip():
                    lStatus.config( text=grbl_out.strip() )




def comup( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 Y" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 Y" + str( speed ) + "\n" )
        #status( event )


def comdown( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 Y-" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 Y-" + str( speed ) + "\n" )
        #status( event )

def coml( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 X-" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 X-" + str( speed ) + "\n" )
        #status( event )

def comr( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 X" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 X" + str( speed ) + "\n" )
        #status( event )

def comzup( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 Z" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 Z" + str( speed ) + "\n" )
        #status( event )

def comzdown( event ):
    if streaming == False:
        Connec.writelines( "G91\nG21\nG00 Z-" + str( speed ) + "\n" )
        Connec.flushInput()
        afficheText( "G91\nG21\nG00 Z-" + str( speed ) + "\n" )
        #status( event )

def gohome( event ):
    if streaming == False:
        Connec.writelines( "G90\nG21\nG00 Z2.000\nG00 X0.000 Y0.000\nG00 Z0.000\n" )
        Connec.flushInput()
        afficheText( "G90\nG21\nG00 Z2.000\nG00 X0.000 Y0.000\nG00 Z0.000" + "\n" )
        #status( event )

def sethome( event ):
    global virtualhome
    if streaming == False:
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
    #status( event )

def pause( event ):
    global varpause
    if streaming == False:
        varpause = False
        afficheText( "rien a mettre en pause" + "\n" )
        return
    if varpause == True:
        varpause = False
        afficheText( "PAUSE" + "\n" )
        return
    if varpause == False:
        varpause = True
        afficheText( "GO" + "\n" )



def gcodestream( event ):
    if streaming == False:
        if filegcode == "":
            loadfile()
        if filegcode != "":
            global streaming
            streaming = True
            thread.start_new_thread( stream, ( filegcode, ) )


def stops( event ):
    global streaming
    streaming = False

def quit( event ):
    if streaming == False:
        if tkMessageBox.askokcancel( "Quit?", "Are you sure you want to quit?" ):
            Connec.close()
            root.quit()

def resetg( event ):
    if streaming == False:
        Connec.writelines( "\030" )


def handler():
    if tkMessageBox.askokcancel( "Quit?", "Are you sure you want to quit?" ):
        Connec.close()
        root.quit()

def loadfile():
    global filegcode, loadingfile
    file = tkFileDialog.askopenfile( parent=root, mode='rb', title='Choose a file', filetypes=[( 'numeric command', '*.nc' ), ( 'gcode', '*.gc' )] )
    if file != None:
        filegcode = file.readlines()
        loadingfile = True
        file.close()
        loadingfile = False

def cValide():
    temp = tCommand.get()
    temp = temp + "\n"
    tCommand.delete( 0 , 255 )
    lStatus.focus_set()
    if streaming == False:
        Connec.writelines( temp )
        Connec.flushInput()
        afficheText( temp )
        #status( event )
        #getSerial()
        grbl_out = Connec.readlines() # Wait for grbl response with carriage return
        getSerial( grbl_out )

def cAnnule():
    lStatus.focus_set()
    tCommand.delete( 0 , 255 )

def stream( data ):
    if streaming == False: return
    global streaming
    tCommand.config( state=DISABLED )
    bValide.config( state=DISABLED )
    Connec.write( "\r\n\r\n" )
    time.sleep( 2 )
    Connec.flushInput()
    f = data
    for line in f :
        if streaming == False:
            break
        i = 0
        if varpause == True :
            Connec.write( '!' )
            while True:
                if varpause == False :
                    Connec.write( '~' )
                    #print( '~' )
                    break
        l = line.strip() # Strip all EOL characters for consistency
        #ref = parse_xyz( l )
        #lStatus.config(text=l)
        afficheText( l )
        if l == "M30":
            streaming = False
            break
        Connec.write( l + '\n' ) # Send g-code block to grbl
        grbl_out = Connec.readline() # Wait for grbl response with carriage return
        afficheText( grbl_out )
        #lStatus.config( text=l + ': ' + grbl_out.strip() + ' ' )
    streaming = False
    tCommand.config( state=NORMAL )
    bValide.config( state=NORMAL )




def scan():
   # scan for available ports. return a list of tuples (num, name)
   available = []
   for port, desc, hwid in sorted( comports() ):
        if "USB" in desc:
            available.append( port )
   return available

def serialConnec( event ):
    global Connec
    lStatus.focus_set()
    if Connec.getPort() != None:
        Connec.close()
        if varcombo.get() != "":
            Connec.setPort( varcombo.get() )
            Connec.open()
            Connec.flushInput()

            if Connec.isOpen():
                lStatusConnec.config( text="connected", fg="green" )
                #tAffiche.
            else:
                lStatusConnec.config( text="not connected", fg="red" )

    else:
        if varcombo.get() != "":
            Connec.setPort( varcombo.get() )
            Connec.open()
            Connec.flushInput()
            if Connec.isOpen():
                lStatusConnec.config( text="connected", fg="green" )
            else:
                lStatusConnec.config( text="not connected", fg="red" )
#GUI

root = Tk()
root.resizable( width=False, height=False )
root.title( 'CncGui' )

lTitre = Label( root, text="INSTRUCTIONS", fg="red" )

lCommandes = Label( root, text="1: \n2: \n3: \n\narrow keys: \npage up & page down: \n\nh: \nt: \nr: \ng: \np: \nx: \ns: ", justify=RIGHT, fg="red" )
lInstruc = Label( root, text="set speed to 0.01 mm  per jog\nset speed to 0.10 mm per jog\nset speed to 1.00 mm per jog\n\njog in x-y plane\njog in z axis\n\ngo home\nset virtual home/disable\nreset grbl\nstream un     fichier g-code\nmet en pause le stream\nstop streaming g-code (this is NOT immediate)\nstatus de la machine", justify=LEFT )

lStatus = Label( root, text="coordonnees", fg="dark green", bg="yellow" )
lJogSpeed = Label( root, text="current jog speed: " + str( speed ) + " mm per step" )
lPortname = Label( root, text="" )



menubar = Menu( root )

filemenu = Menu( menubar, tearoff=0 )
filemenu.add_command( label="Open", command=loadfile )
filemenu.add_separator()
filemenu.add_command( label="Exit", command=handler )
menubar.add_cascade( label="File", menu=filemenu )

CadreBar = Frame( root )
cadreCom = Frame( root )
cadreAffich = Frame( root )


scrollAffiche = Scrollbar( cadreAffich )
tAffiche = Text( cadreAffich, width=80, height=10, yscrollcommand=scrollAffiche.set )
tAffiche.insert( INSERT, "cncgui v0.1 \n" )
tAffiche.config( state=DISABLED )
varcombo = StringVar()

barconf = ttk.Combobox( CadreBar, state='readonly', textvariable=varcombo )

barconf["value"] = scan()
lStatusConnec = Label( CadreBar, text="Not Connected", fg="red" )

tCommand = ttk.Entry( cadreCom, width=48 )
bValide = Button( cadreCom, text="envoi", command=cValide )
bAnnule = Button( cadreCom, text="annule", command=cAnnule )

lTitre.grid( row=1, columnspan=2 )
lCommandes.grid( row=2, column=0 )
lInstruc.grid( row=2, column=1 )
lStatus.grid( row=3, columnspan=2 )
lJogSpeed.grid( row=4, columnspan=2 )
cadreCom.grid( row=5, columnspan=4 )
cadreAffich.grid( row=6, columnspan=4 )
lPortname.grid( row=8, columnspan=1 )
CadreBar.grid( row=9, columnspan=4 )

tCommand.pack( side=LEFT )
bValide.pack( side=LEFT )
bAnnule.pack( side=LEFT )

tAffiche.pack( side=LEFT, fill=BOTH )
scrollAffiche.pack( side=RIGHT, fill=Y )
scrollAffiche.config( command=tAffiche.yview )

barconf.pack( side=LEFT )
lStatusConnec.pack( side=LEFT )
lStatus.focus_set()

root.grid_rowconfigure( 0, weight=1 )
root.grid_columnconfigure( 3, weight=1 )

lStatus.bind( '1', set_speed0 )
lStatus.bind( '2', set_speed1 )
lStatus.bind( '3', set_speed2 )

lStatus.bind( '<Up>', comup )
lStatus.bind( '<Down>', comdown )
lStatus.bind( '<Left>', coml )
lStatus.bind( '<Right>', comr )
lStatus.bind( '<Next>', comzdown )
lStatus.bind( '<Prior>', comzup )

lStatus.bind( '<h>', gohome )
lStatus.bind( '<t>', sethome )
lStatus.bind( '<p>', pause )
lStatus.bind( '<g>', gcodestream )
lStatus.bind( '<q>', quit )
lStatus.bind( '<r>', resetg )
#root.bind_all( '<s>', status )
lStatus.bind( '<x>', stops )

root.protocol( "WM_DELETE_WINDOW", handler )

barconf.bind( '<<ComboboxSelected>>', serialConnec )

root.config( menu=menubar )

def main():
    thread.start_new_thread( status, () )
    root.mainloop()


if __name__ == "__main__":
    main()
