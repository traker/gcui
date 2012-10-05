from Tkinter import *
import serial, tkFileDialog, time, thread, tkMessageBox

DEFAULT_BAUDRATE = 9600
speed = 0.10
portname = "COM4"
streaming = False
virtualhome = False
varpause = False
Connec = serial.Serial()
Connec.port = portname
Connec.baudrate = DEFAULT_BAUDRATE
zoom = 5.0    # niveau de zoom
mm = 5.03
_debug = 1     #active l'affichage des differentes variables
filegcode = ""
loadingfile = False

        

coord = {
    "tx": 135.0 * mm,
    "ty": 75.0 * mm,
    "oldcol": "red",
    "oldx": 0.0,
    "oldy": 0.0,
    "col": "red",
    "ox" : 0.0,
    "oy" : 0.0,
    "oz" : "up"
}



def G0com(xyz):
    global coord
    for f in xyz:
        if f[0] == "Z":
            if float(f[1:]) <= 0: 
                coord["col"] = "blue"
                if loadingfile == True: coord["col"] = "green"
                coord["oz"] = "down"
            else: 
                coord["col"] = "red"
                if loadingfile == True: coord["col"] = "yellow"
                coord["oz"] = "up"
        if f[0] == "X":
            coord["ox"] = f[1:]
        if f[0] == "Y":
            coord["oy"] = f[1:]
    x = float(coord["ox"])
    y = float(coord["oy"])
    if _debug :print 'x = {0},y = {1}, z = {2}, couleur = {3}, pos x actuel = {4}, pos y actuel = {5}'.format( x, y, coord["oz"], coord["col"], coord["oldx"],coord["oldy"], coord["oldcol"] )
    vuegc.create_line(float(coord["oldx"])*zoom,-float(coord["oldy"])*zoom, x*zoom, -y*zoom,fill=coord["col"])
    coord["oldcol"] = coord["col"]
    coord["oldx"] = coord["ox"]
    coord["oldy"] = coord["oy"]


    
    

def G1com(xyz):
    global coord
    for f in xyz:
        if f[0] == "Z":
            if float(f[1:]) <= 0: 
                coord["col"] = "blue"
                if loadingfile == True: coord["col"] = "green"
                coord["oz"] = "down"
            else: 
                coord["col"] = "red"
                if loadingfile == True: coord["col"] = "yellow"
                coord["oz"] = "up"
        if f[0] == "X":
            coord["ox"] = f[1:]
        if f[0] == "Y":
            coord["oy"] = f[1:]
    x = float(coord["ox"])
    y = float(coord["oy"])
    if _debug :print 'x = {0},y = {1}, z = {2}, couleur = {3}, pos x actuel = {4}, pos y actuel = {5}'.format( x, y, coord["oz"], coord["col"], coord["oldx"],coord["oldy"], coord["oldcol"] )
    vuegc.create_line(float(coord["oldx"])*zoom,-float(coord["oldy"])*zoom, x*zoom, -y*zoom,fill=coord["col"])
    coord["oldcol"] = coord["col"]
    coord["oldx"] = coord["ox"]
    coord["oldy"] = coord["oy"]


        
def G3com(xyz):
    global coord
    for f in xyz:
        if f[0] == "Z":
            if float(f[1:]) <= 0: 
                coord["col"] = "blue"
                if loadingfile == True: coord["col"] = "green"
                coord["oz"] = "down"
            else: 
                coord["col"] = "red"
                if loadingfile == True: coord["col"] = "yellow"
                coord["oz"] = "up"
        if f[0] == "X":
            coord["ox"] = f[1:]
        if f[0] == "Y":
            coord["oy"] = f[1:]
    x = float(coord["ox"])
    y = float(coord["oy"])
    if _debug :print 'x = {0},y = {1}, z = {2}, couleur = {3}, pos x actuel = {4}, pos y actuel = {5}'.format( x, y, coord["oz"], coord["col"], coord["oldx"],coord["oldy"], coord["oldcol"] )
    vuegc.create_line(float(coord["oldx"])*zoom,-float(coord["oldy"])*zoom, x*zoom, -y*zoom,fill=coord["col"])
    coord["oldcol"] = coord["col"]
    coord["oldx"] = coord["ox"]
    coord["oldy"] = coord["oy"]

def nullcomm(xyz):
    #print "commande non prise en charge"
    pass


gcode = {
            "G0"    :G0com ,    # Interpolation lineaire en vitesse rapide
            "G00"    :G0com ,
            "G1"    :G1com ,    # Interpolation lineaire en vitesse programmee
            "G01"    :G1com ,
#            "G2"    :"" ,            # Interpolation circulaire ("ou helicoidale") sens horaire
            "G3"    :G3com ,            # Interpolation circulaire ("ou helicoidale") sens antihoraire
            "G03"    :G3com ,
#            "G7"    :"" ,            #
#            "G10"    :"" ,            #
#            "G17"    :"" ,            # Plan de travail XY
#            "G18"    :"" ,            # Plan de travail XZ
#            "G19"    :"" ,            # Plan de travail YZ
#            "G20"    :"" ,            #
#            "G21"    :G21com ,    #
#            "G30"    :"" ,            #
#            "G33"    :"" ,            # Filetage avec broche synchronisee
#            "G38"    :"" ,            #
#            "G40"    :G40com ,    # Annulation de la compensation de rayon d'outil
#            "G41"    :"" ,            # Compensation de rayon d'outil, a gauche profil
#            "G42"    :"" ,            # Compensation de rayon d'outil, a droite du profil
#            "G43"    :"" ,            #
#            "G49"    :G49com ,    #
#            "G53"    :"" ,            #
#            "G54"    :"" ,            #
#            "G59"    :"" ,            #
#            "G61"    :"" ,            # Mode trajectoire exacte
#            "G64"    :"" ,            # Mode trajectoire continue avec tolerance optionnelle
#            "G73"    :"" ,            #
#            "G76"    :"" ,            #
#            "G80"    :"" ,            # Revocation des codes modaux
#            "G81"    :"" ,            # Cycle de percage
#            "G82"    :"" ,            #
#            "G89"    :"" ,            #
#            "G90"    :G90com ,    # Deplacements en coordonnees absolues (par rapport a l'origine piece)
#            "G91"    :"" ,            # Deplacements en coordonnees relatives (incrementales)
#            "G92"    :"" ,            #
#            "G93"    :"" ,            # Vitesse inverse du temps (vitesse/distance)
#            "G94"    :"" ,            # Vitesse en unites par minute 
#            "G95"    :"" ,            # Vitesse en unites par tour
#            "G96"    :"" ,            #
#            "G97"    :"" ,            #
#            "G98"    :"" ,            # Retrait au point initial
#            "G99"    :"" ,            # Retrait sur R
        }

def parse_xyz(s):
    g = s.split()
    return(g)

def setlabel():
    lJogSpeed.config(text="current jog speed: " + str(speed) + " mm per step")

def set_speed0(event):
    global speed
    speed = 0.01
    setlabel()

def set_speed1(event):
    global speed
    speed = 0.10
    setlabel()

def set_speed2(event):
    global speed
    speed = 1.00
    setlabel()

def comup(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X0.000 Y" + str(speed) + " Z0.000\n")
        Connec.flushInput()

def comdown(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X0.000 Y-" + str(speed) + " Z0.000\n")
        Connec.flushInput()

def coml(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X-" + str(speed) + " Y0.000 Z0.000\n")
        Connec.flushInput()

def comr(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X" + str(speed) + " Y0.000 Z0.000\n")
        Connec.flushInput()

def comzup(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X0.000 Y0.000 Z" + str(speed)+ "\n")
        Connec.flushInput()

def comzdown(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X0.000 Y0.000 Z-" + str(speed) + "\n")
        Connec.flushInput()

def gohome(event):
    if streaming == False:
        Connec.writelines("G90\nG21\nG00 Z2.000\nG00 X0.000 Y0.000\nG00 Z0.000\n")
        Connec.flushInput()

def sethome(event):
    global virtualhome
    if streaming == False:
        if virtualhome == False:
            Connec.writelines("G92 X0.000 Y0.000 Z0.000\n")
            Connec.flushInput()
            virtualhome = True
        else:
            Connec.writelines("G92.1\n")
            Connec.flushInput()
            virtualhome = False



def pause(event):
    global varpause
    if streaming == False: 
        varpause = False
        return
    if varpause == True:
        varpause = False
        return
    if varpause == False:
        varpause = True



def gcodestream(event):
    if streaming == False:
        if filegcode == "":
            loadfile()
        if filegcode != "":
            global streaming
            streaming = True
            thread.start_new_thread( stream, (filegcode, ) )


def stops(event):
    global streaming
    streaming = False

def quit(event):
    if streaming == False:
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            Connec.close()
            root.quit()

def resetg(event):
    if streaming == False:
        Connec.writelines("\030")


def handler():
    if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
        Connec.close()
        root.quit()

def loadfile():
    global filegcode, loadingfile
    vuegc.delete('all')
    file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetypes=[('numeric command', '*.nc'), ('gcode', '*.gc')])
    if file != None:
        filegcode = file.readlines()
        loadingfile = True
        for line in filegcode :
            l = line.strip()
            ref= parse_xyz(l)
            gcode.get(ref[0],nullcomm)(ref[1:])
        vuegc.create_line(coord["tx"]/2 - coord["tx"], 0,coord["tx"] / 2,0)
        vuegc.create_line(0.0, coord["ty"] / 2, 0.0, coord["ty"] / 2 - coord["ty"])
        file.close()
        loadingfile = False


def clear(event):
    if streaming == True: return
    vuegc.delete('all')

def dessine():
    global coord
    x = float(coord["ox"])
    y = float(coord["oy"])
    if _debug :print 'x = {0},y = {1}, z = {2}, couleur = {3}, pos x actuel = {4}, pos y actuel = {5}'.format( x, y, coord["oz"], coord["col"], coord["oldx"],coord["oldy"], coord["oldcol"] )
    vuegc.create_line(float(coord["oldx"])*zoom,float(coord["oldy"])*zoom, x*zoom, y*zoom,fill=coord["col"])
    coord["oldcol"] = coord["col"]
    coord["oldx"] = coord["ox"]
    coord["oldy"] = coord["oy"]


def stream(data):
    if streaming == False: return
    global streaming
    Connec.write("\r\n\r\n")
    time.sleep(2)
    Connec.flushInput()
    f = data
    for line in f :
        if streaming == False: 
            break
        i = 0
        if varpause == True :
            Connec.write('!')
            while True:
                if varpause == False :
                    Connec.write('~')
                    print('~')
                    break
        l = line.strip() # Strip all EOL characters for consistency    
        ref = parse_xyz(l)
        thread.start_new_thread(gcode.get(ref[0],nullcomm),(ref[1:],))
        #gcode.get(ref[0],nullcomm)(ref[1:])
        #thread.start_new_thread(dessine, ())
        lStatus.config(text=l)
        if l == "M30":
            streaming = False
            break
        Connec.write(l + '\n') # Send g-code block to grbl
        grbl_out = Connec.readline() # Wait for grbl response with carriage return
        lStatus.config(text=l + ': ' + grbl_out.strip() + ' ' )
    streaming = False



def status():
    while True:
        # if etatstat == False: break
        time.sleep(0.5)
        if streaming == False:
            Connec.flushInput()
            Connec.write('?') # Send g-code block to grbl
            grbl_out = Connec.readline() # Wait for grbl response with carriage return
            if "MPos" in grbl_out.strip():
                lStatus.config(text=grbl_out.strip())
        
        

root = Tk()
root.minsize(600,600)
#root.resizable(width=False, height=False)
root.title('CncGui')

lTitre=Label(root,text="INSTRUCTIONS", fg="red")

lCommandes=Label(root, text="1: \n2: \n3: \n\narrow keys: \npage up & page down: \n\nh: \nt: \nr: \ng: \np: \nx: \ns: ", justify=RIGHT, fg="red")
lInstruc=Label(root,text="set speed to 0.01 mm  per jog\nset speed to 0.10 mm per jog\nset speed to 1.00 mm per jog\n\njog in x-y plane\njog in z axis\n\ngo home\nset virtual home/disable\nreset grbl\nstream un     fichier g-code\nmet en pause le stream\nstop streaming g-code (this is NOT immediate)\nstatus de la machine", justify=LEFT)

lStatus=Label(root,text="coordonnees", fg="dark green", bg="yellow")
lJogSpeed=Label(root,text="current jog speed: " + str(speed) + " mm per step")
lPortname=Label(root, text="current serial port: " + portname)

vuegc = Canvas(root, bg ='white',scrollregion=(coord["tx"]/2 - coord["tx"],coord["ty"]/2 - coord["ty"],coord["tx"]/2,coord["ty"]), relief="raised")
hbar=Scrollbar(root,orient=HORIZONTAL)
hbar.config(command=vuegc.xview)
vbar=Scrollbar(root,orient=VERTICAL)
vbar.config(command=vuegc.yview)
vuegc.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)


menubar = Menu(root)


filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=loadfile)
filemenu.add_command(label="Save", command=handler)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

lTitre.grid(row=1, columnspan=2)
lCommandes.grid(row=2, column=0)
lInstruc.grid(row=2, column=1)
lStatus.grid(row=3, columnspan=2)
lJogSpeed.grid(row=4, columnspan=2)
lPortname.grid(row=5, columnspan=2)
vuegc.grid(row=0, column=3, rowspan=6,columnspan=4, sticky=E+W+S+N)
hbar.grid(row=6,column=3, columnspan=4, sticky=E+W)
vbar.grid(row=0,column=7, rowspan=4,sticky=N+S)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(3, weight=1)

root.bind_all('1',set_speed0)
root.bind_all('2', set_speed1)
root.bind_all('3', set_speed2)

root.bind_all('<Up>', comup)
root.bind_all('<Down>', comdown)
root.bind_all('<Left>', coml)
root.bind_all('<Right>', comr)
root.bind_all('<Next>', comzdown)
root.bind_all('<Prior>', comzup)

root.bind_all('<h>', gohome)
root.bind_all('<t>', sethome)
root.bind_all('<p>', pause)
root.bind_all('<g>', gcodestream)
root.bind_all('<q>', quit)
root.bind_all('<r>', resetg)
root.bind_all('<x>', stops)
root.bind_all('<c>', clear)
root.protocol("WM_DELETE_WINDOW", handler)
root.config(menu=menubar)

def main():
    Connec.open()
    thread.start_new_thread( status,())
    #thread.start_new_thread(dessine, ())
    root.mainloop()

if __name__ == "__main__":
    main()
