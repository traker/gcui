from Tkinter import *
import serial, tkFileDialog, time, thread, tkMessageBox
import sys
sys.path.append('src/')
from fraiseuse import fraiseuse

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
_debug = 0     #active l'affichage des differentes variables
filegcode = ""
loadingfile = False



coord = {
    "tx": 135.0 * mm,
    "ty": 75.0 * mm,
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
    vuegc.create_line(test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], x*mm + test.get_posZeroVirtuel()[0], -y*mm + test.get_posZeroVirtuel()[1],fill=coord["col"], tags="uno")
    test.x_movetoa(float(y))
    test.y_movetoa(float(x))
    if coord["col"] == "blue" or coord["col"] == "red":
        vuegc.coords(vueBroche, test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], float(vuegc.cget("width")) / 2, 0)






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
    vuegc.create_line(test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], x*mm + test.get_posZeroVirtuel()[0], -y*mm + test.get_posZeroVirtuel()[1],fill=coord["col"], tags="uno")
    test.x_movetoa(float(y))
    test.y_movetoa(float(x))
    if coord["col"] == "blue" or coord["col"] == "red":
        vuegc.coords(vueBroche, test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], float(vuegc.cget("width")) / 2, 0)




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
    vuegc.create_line(test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], x*mm + test.get_posZeroVirtuel()[0], -y*mm + test.get_posZeroVirtuel()[1],fill=coord["col"], tags="uno")
    test.x_movetoa(float(y))
    test.y_movetoa(float(x))
    if coord["col"] == "blue" or coord["col"] == "red":
        vuegc.coords(vueBroche, test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], float(vuegc.cget("width")) / 2, 0)


def nullcomm(xyz):
    #print "commande non prise en charge"
    pass


gcode = {
            "G0"    :G0com ,    # Interpolation lineaire en vitesse rapide
            "G00"    :G0com ,
            "G1"    :G1com ,    # Interpolation lineaire en vitesse programmee
            "G01"    :G1com ,
            "G2"    :G3com ,            # Interpolation circulaire ("ou helicoidale") sens horaire
            "G02"    :G3com ,            # Interpolation circulaire ("ou helicoidale") sens horaire
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
        test.x_movetor(-speed)
        Connec.flushInput()
        dessine()


def comdown(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X0.000 Y-" + str(speed) + " Z0.000\n")
        test.x_movetor(speed)
        Connec.flushInput()
        dessine()

def coml(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X-" + str(speed) + " Y0.000 Z0.000\n")
        test.y_movetor(-speed)
        Connec.flushInput()
        dessine()

def comr(event):
    if streaming == False:
        Connec.writelines("G91\nG21\nG00 X" + str(speed) + " Y0.000 Z0.000\n")
        test.y_movetor(speed)
        Connec.flushInput()
        dessine()

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
        test.gohome()
        dessine()

def sethome(event):
    global virtualhome
    if streaming == False:
        if virtualhome == False:
            Connec.writelines("G92 X0.000 Y0.000 Z0.000\n")
            Connec.flushInput()
            test.set_home()
            virtualhome = True
            dessine()
            
        else:
            virtualhome = False
            Connec.writelines("G92.1\n")
            Connec.flushInput()
            test.homeReset()
            dessine()
            



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
    file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetypes=[('numeric command', '*.nc'), ('gcode', '*.gc')])
    if file != None:
        filegcode = file.readlines()
        loadingfile = True
        temp = [test.get_posBrocheMachine()[0], test.get_posBrocheMachine()[1], test.get_posBrocheMachine()[2]]
        dessine()
        test.set_BrocheMachine(temp)
        file.close()
        loadingfile = False


def clear(event):
    if streaming == True:
        vuegc.delete("uno")

def cleari():
    vuegc.delete("uno")



def middleaxe(taille):
    if taille == "x":
        return int(vuegc.cget("width")) /2
    else:
        return int(vuegc.cget("height")) /2

def zerox():
    return vuegc.coords(vueAxe_Y)[0]

def zeroy():
    return vuegc.coords(vueAxe_X)[1]

def OnvuegcClick(event):
    global  virtualhome
    if streaming == False:
        virtualhome = True
        test.set_axe([event.x, event.y])
        Connec.writelines("G92 X"+str(test.afficheZeroVirtuel()[0] - test.afficheBrocheMachine()[0])+" Y"+str(test.afficheZeroVirtuel()[1] - test.afficheBrocheMachine()[1])+" Z0.000\n")
        #print "G92 X"+str(test.afficheZeroVirtuel()[0]) +" -"+str(test.afficheBrocheMachine()[0])+" Y"+str(test.afficheZeroVirtuel()[1])+" - "+str(test.afficheBrocheMachine()[1])+" Z0.000\n"
        #gohome(None)
        temp = [test.get_posBrocheMachine()[0], test.get_posBrocheMachine()[1], test.get_posBrocheMachine()[2]]
        dessine()
        test.set_BrocheMachine(temp)


def MousePos(event):
    vuegc.itemconfigure(text_X, text="X: "+str((event.x - test.get_posZeroVirtuel()[0]) / mm))
    vuegc.itemconfigure(text_Y, text="Y: "+str((test.get_posZeroVirtuel()[1] - event.y) / mm))


def dessinetable():
    print "axe x:"+str(test.get_vue_axe0X())
    print "axe z:"+str(test.get_vue_axe0Y())
    print "pos broche:"+str(test.get_posBrocheMachine())
    print "zero virtuel:"+str(test.get_posZeroVirtuel())
    print "zero machine:"+str(test.get_zeroMachine())
    vuegc.coords(table_XY, test.get_table()[0],test.get_table()[1], test.get_table()[2], test.get_table()[3])
    vuegc.coords(vueAxe_X, test.get_vue_axe0X()[0], test.get_vue_axe0X()[1], test.get_vue_axe0X()[2], test.get_vue_axe0X()[3])
    vuegc.coords(vueAxe_Y, test.get_vue_axe0Y()[0], test.get_vue_axe0Y()[1], test.get_vue_axe0Y()[2], test.get_vue_axe0Y()[3])
    vuegc.coords(vueBroche, test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], float(vuegc.cget("width")) / 2, 0)



def dessine():
    global loadingfile
    dessinetable()
    if filegcode != None :
        loadingfile = True
        cleari()
        for line in filegcode :
            l = line.strip()
            ref= parse_xyz(l)
            gcode.get(ref[0],nullcomm)(ref[1:])
        loadingfile = False

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
        #lStatus.config(text=l)
        if l == "M30":
            streaming = False
            break
        Connec.write(l + '\n') # Send g-code block to grbl
        grbl_out = Connec.readline() # Wait for grbl response with carriage return
        lStatus.config(text=l + ': ' + grbl_out.strip() + ' ' )
    streaming = False


def status():
    while True:
        time.sleep(0.5)
        if streaming == False:
            Connec.flushInput()
            Connec.write('?') # Send g-code block to grbl
            grbl_out = Connec.readline() # Wait for grbl response with carriage return
            if "MPos" in grbl_out.strip():
                lStatus.config(text=grbl_out.strip())




root = Tk()
root.resizable(width=False, height=False)
root.title('CncGui')

lTitre=Label(root,text="INSTRUCTIONS", fg="red")

lCommandes=Label(root, text="1: \n2: \n3: \n\narrow keys: \npage up & page down: \n\nh: \nt: \nr: \ng: \np: \nx: \ns: ", justify=RIGHT, fg="red")
lInstruc=Label(root,text="set speed to 0.01 mm  per jog\nset speed to 0.10 mm per jog\nset speed to 1.00 mm per jog\n\njog in x-y plane\njog in z axis\n\ngo home\nset virtual home/disable\nreset grbl\nstream un     fichier g-code\nmet en pause le stream\nstop streaming g-code (this is NOT immediate)\nstatus de la machine", justify=LEFT)

lStatus=Label(root,text="coordonnees", fg="dark green", bg="yellow")
lJogSpeed=Label(root,text="current jog speed: " + str(speed) + " mm per step")
lPortname=Label(root, text="current serial port: " + portname)

vuegc = Canvas(root, bg ='white', relief="raised",height=int(coord["ty"])+200,width=int(coord["tx"])+100)
hbar=Scrollbar(root,orient=HORIZONTAL)
hbar.config(command=vuegc.xview)
vbar=Scrollbar(root,orient=VERTICAL)
vbar.config(command=vuegc.yview)
vuegc.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

var = [(float(middleaxe("x")) - (coord["tx"])/2),\
                                       (float(middleaxe("y")) - (coord["ty"]) / 2),\
                                       (float(middleaxe("x"))) + (coord["tx"]/2 ),\
                                       (float(middleaxe("y"))) + ( coord["ty"] / 2 )]

test = fraiseuse(var,[vuegc.cget("height"), vuegc.cget("width")])
table_XY = vuegc.create_rectangle(test.get_table(),fill = "gray")
vueAxe_X = vuegc.create_line(test.get_vue_axe0X())
vueAxe_Y = vuegc.create_line(test.get_vue_axe0Y())
vueBroche = vuegc.create_line(test.get_posBrocheMachine()[0],test.get_posBrocheMachine()[1], float(vuegc.cget("width")) / 2, 0, fill="red")
text_X = vuegc.create_text(int(vuegc.cget("width")) / 3, int(vuegc.cget("height")) - 20)
text_Y = vuegc.create_text((int(vuegc.cget("width")) / 3)*2, int(vuegc.cget("height")) - 20)

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
vuegc.bind('<Motion>', MousePos)
vuegc.bind('<Button-1>',OnvuegcClick)

root.config(menu=menubar)

def main():
    Connec.open()
    Connec.flushInput()
    thread.start_new_thread( status,())
    root.mainloop()

if __name__ == "__main__":
    main()
