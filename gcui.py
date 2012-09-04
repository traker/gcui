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
Connec.open()


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
        gcode = loadfile()
        if gcode != None:
            global streaming
            streaming = True
            thread.start_new_thread( stream, (gcode, ) )


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
    file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a file',filetypes=[('numeric command', '*.nc'), ('gcode', '*.gc')])
    if file != None:
        return file

def stream(data):
    if streaming == False: return
    global streaming
    Connec.write("\r\n\r\n")
    time.sleep(2)
    Connec.flushInput()
    f = data.readlines()
    for line in f :
        if streaming == False: 
            data.close()
            break
        i = 0
        while varpause:
            i = i + 1
        l = line.strip() # Strip all EOL characters for consistency
        lStatus.config(text=l)
        #print 'Sending: ' + l,
        Connec.write(l + '\n') # Send g-code block to grbl
        grbl_out = Connec.readline() # Wait for grbl response with carriage return
        lStatus.config(text=l + ': ' + grbl_out.strip() + ' ' )
    data.close()
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
root.resizable(width=False, height=False)

lTitre=Label(root,text="INSTRUCTIONS", fg="red")

lCommandes=Label(root, text="1: \n2: \n3: \n\narrow keys: \npage up & page down: \n\nh: \nt: \nr: \ng: \np: \nx: \ns: ", justify=RIGHT, fg="red")
lInstruc=Label(root,text="set speed to 0.01 mm  per jog\nset speed to 0.10 mm per jog\nset speed to 1.00 mm per jog\n\njog in x-y plane\njog in z axis\n\ngo home\nset virtual home/disable\nreset grbl\nstream un fichier g-code\nmet en pause le stream\nstop streaming g-code (this is NOT immediate)\nstatus de la machine", justify=LEFT)


lStatus=Label(root,text="coordonnees", fg="dark green", bg="yellow")
lJogSpeed=Label(root,text="current jog speed: " + str(speed) + " mm per step")
lPortname=Label(root, text="current serial port: " + portname)

lTitre.grid(row=0, columnspan=2)
lCommandes.grid(row=1, column=0)
lInstruc.grid(row=1, column=1)
lStatus.grid(row=2, columnspan=2)
lJogSpeed.grid(row=3, columnspan=2)
lPortname.grid(row=4, columnspan=2)

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

root.protocol("WM_DELETE_WINDOW", handler)
# or toplevel.protocol(...
thread.start_new_thread( status,())
root.mainloop()
 



