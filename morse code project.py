import tkinter as tk
from pyfirmata import Arduino,OUTPUT,INPUT,util
import time
#==========================================================================for arduino board
board=Arduino('COM11')
led=12
ldr=0
board.digital[led].mode=OUTPUT
board.analog[ldr].mode=INPUT
it=util.Iterator(board)
it.start()
board.analog[ldr].enable_reporting()
#==========================================================================morse code dictionary
morsecode={ 'A':'.-', 'B':'-...', 
	    'C':'-.-.', 'D':'-..', 'E':'.', 
            'F':'..-.', 'G':'--.', 'H':'....', 
	    'I':'..', 'J':'.---', 'K':'-.-', 
	    'L':'.-..', 'M':'--', 'N':'-.', 
	    'O':'---', 'P':'.--.', 'Q':'--.-', 
	    'R':'.-.', 'S':'...', 'T':'-', 
	    'U':'..-', 'V':'...-', 'W':'.--', 
	    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
	    '1':'.----', '2':'..---', '3':'...--', 
	    '4':'....-', '5':'.....', '6':'-....', 
	    '7':'--...', '8':'---..', '9':'----.', 
	    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
	    '?':'..--..', '/':'-..-.', '-':'-....-', 
	    '(':'-.--.', ')':'-.--.-',' ':'*'}
#==========================================================================functions for gui windows open and close
def closetc():
    transceiver_window.destroy()
def menu1():
    transmitter_window.update()
    transmitter_window.withdraw()
    transceiver_window.deiconify()
def menu2():
    receiver_window.update()
    receiver_window.withdraw()
    transceiver_window.deiconify()
def tr():
    transceiver_window.withdraw()
    open_transmitter()
def re():
    transceiver_window.withdraw()
    open_receiver()

#========================================================================== transmitter function
def trans():
    string=transmitter_window.message.get('1.0','end-1c')
    transmit_code=''
    for letter in string.upper():
            for key in morsecode.keys():
                    if key==letter:
                            transmit_code=transmit_code+morsecode[key]+' '
    for value in transmit_code:
            if value=='.':
                    board.digital[led].write(1)
                    time.sleep(.2)
                    board.digital[led].write(0)
                    time.sleep(.2)                           
            elif value=='-':
                    board.digital[led].write(1)
                    time.sleep(.6)
                    board.digital[led].write(0)
                    time.sleep(.2)
            elif value==' ':
                    time.sleep(.4)
            elif value=='*':
                    time.sleep(.4)
    time.sleep(6)
    transmitter_window.message.delete('1.0','end-1c')

#======================================================================receiver function    
def recei():
    receiver_window.Text1.delete('1.0','end-1c')
    received_code=''
    light_on_count=0
    ldr_test_count=0
    light_off_count=0
    ldr_max_value=0
    message=[]
    total=0
    
#find the average light intesity    
    while ldr_test_count<100:
        ldr_test_count+=1
        val=board.analog[ldr].read()
        total=total+val
    ldr_max_value=total/100+0.04
    
    while True:
        val=board.analog[ldr].read()
        print('',end='')
        if val>ldr_max_value:
            light_on_count=0
            light_off_count=0
#find -,. from led signel            
            while True:
                val=board.analog[ldr].read()
                if val>ldr_max_value:
                    light_on_count+=1
                    time.sleep(.1)
                else:
                    break
            if 3>=light_on_count>=1:
                received_code=received_code+"."
            elif 7>=light_on_count>4:
                received_code=received_code+"-"
#find ' ','  ' from led signel                 
            while True:
                val=board.analog[ldr].read()
                if val<ldr_max_value:
                    light_off_count+=1
                    if light_off_count>=16:
                        break
                    time.sleep(.1)
                else:
                    break
            if 6>=light_off_count>=3:
                received_code=received_code+" "
            elif 14>=light_off_count>=7:
                received_code=received_code+" * "
            elif light_off_count>=16:
                for i in range(len(received_code.split(' '))):
                    for letter,key in morsecode.items():
                        if key==received_code.split(' ')[i]:
                            message.append(letter)
#print the received morse cose as text                            
                output=''   
                for i in message:
                    output+=i
                receiver_window.Text1.insert('1.0',output)
                if light_off_count>=16:
                    message=[]
                    received_code=''
                    break
        if light_off_count>=16:
            break
#==============================================================function for transceiver window open
        
def open_transceiver():
    global transceiver_window
    transceiver_window=tk.Tk()
    transceiver_window.geometry("600x273+300+100")
    transceiver_window.minsize(120, 1)
    transceiver_window.maxsize(1370, 749)
    transceiver_window.resizable(0, 0)
    transceiver_window.title("TRANCIVER")
    transceiver_window.configure(background="#cbc9e9")
    transceiver_window.configure(highlightbackground="#d9d9d9")
    transceiver_window.configure(highlightcolor="black")

    transceiver_window.tr = tk.Button(transceiver_window)
    transceiver_window.tr.place(relx=0.067, rely=0.476, height=44, width=227)
    transceiver_window.tr.configure(activebackground="#00ff40")
    transceiver_window.tr.configure(activeforeground="#000000")
    transceiver_window.tr.configure(background="#d9d9d9")
    transceiver_window.tr.configure(command=tr)
    transceiver_window.tr.configure(disabledforeground="#a3a3a3")
    transceiver_window.tr.configure(foreground="#000000")
    transceiver_window.tr.configure(highlightbackground="#d9d9d9")
    transceiver_window.tr.configure(highlightcolor="black")
    transceiver_window.tr.configure(pady="0")
    transceiver_window.tr.configure(text='''TRANSMITTER''')

    transceiver_window.closetc = tk.Button(transceiver_window)
    transceiver_window.closetc.place(relx=0.317, rely=0.769, height=44, width=227)
    transceiver_window.closetc.configure(activebackground="#ff0000")
    transceiver_window.closetc.configure(activeforeground="white")
    transceiver_window.closetc.configure(activeforeground="#000000")
    transceiver_window.closetc.configure(background="#d9d9d9")
    transceiver_window.closetc.configure(command=closetc)
    transceiver_window.closetc.configure(disabledforeground="#a3a3a3")
    transceiver_window.closetc.configure(foreground="#000000")
    transceiver_window.closetc.configure(highlightbackground="#d9d9d9")
    transceiver_window.closetc.configure(highlightcolor="black")
    transceiver_window.closetc.configure(pady="0")
    transceiver_window.closetc.configure(text='''CLOSE''')

    transceiver_window.re = tk.Button(transceiver_window)
    transceiver_window.re.place(relx=0.533, rely=0.476, height=44, width=227)
    transceiver_window.re.configure(activebackground="#00ff00")
    transceiver_window.re.configure(activeforeground="#000000")
    transceiver_window.re.configure(background="#d9d9d9")
    transceiver_window.re.configure(command=re)
    transceiver_window.re.configure(disabledforeground="#a3a3a3")
    transceiver_window.re.configure(foreground="#000000")
    transceiver_window.re.configure(highlightbackground="#d9d9d9")
    transceiver_window.re.configure(highlightcolor="black")
    transceiver_window.re.configure(pady="0")
    transceiver_window.re.configure(text='''RECEIVER''')

    transceiver_window.Frame1 = tk.Frame(transceiver_window)
    transceiver_window.Frame1.place(relx=0.183, rely=0.073, relheight=0.275
                    , relwidth=0.642)
    transceiver_window.Frame1.configure(relief='groove')
    transceiver_window.Frame1.configure(borderwidth="2")
    transceiver_window.Frame1.configure(relief="groove")
    transceiver_window.Frame1.configure(background="#b8ebfa")
    transceiver_window.Frame1.configure(highlightbackground="#d9d9d9")
    transceiver_window.Frame1.configure(highlightcolor="black")

    transceiver_window.Label1 = tk.Label(transceiver_window.Frame1)
    transceiver_window.Label1.place(relx=0.208, rely=0.267, height=41, width=184)
    transceiver_window.Label1.configure(activebackground="#f5fafc")
    transceiver_window.Label1.configure(activeforeground="#000000")
    transceiver_window.Label1.configure(background="#c1f0f0")
    transceiver_window.Label1.configure(disabledforeground="#a3a3a3")
    
    transceiver_window.Label1.configure(foreground="#0000ff")
    transceiver_window.Label1.configure(highlightbackground="#d9d9d9")
    transceiver_window.Label1.configure(highlightcolor="black")
    transceiver_window.Label1.configure(text='''TRANSCIVER''')

#==========================================================================function for transmitter window open
def open_transmitter():
    global transmitter_window
    transmitter_window=tk.Tk()
    transmitter_window.geometry("600x273+300+100")
    transmitter_window.minsize(120, 1)
    transmitter_window.maxsize(1370, 749)
    transmitter_window.resizable(0, 0)
    transmitter_window.title("TRANSMITTER")
    transmitter_window.configure(background="#c8e8ea")

    transmitter_window.Label1 = tk.Label(transmitter_window)
    transmitter_window.Label1.place(relx=0.267, rely=0.11, height=51, width=264)
    transmitter_window.Label1.configure(activebackground="#ebf2f5")
    transmitter_window.Label1.configure(background="#c8e7ea")
    transmitter_window.Label1.configure(disabledforeground="#a3a3a3")

    transmitter_window.Label1.configure(foreground="#000000")
    transmitter_window.Label1.configure(text='''TRANSMITTER''')

    transmitter_window.Label2 = tk.Label(transmitter_window)
    transmitter_window.Label2.place(relx=0.067, rely=0.368, height=31, width=174)
    transmitter_window.Label2.configure(background="#d9d9d9")
    transmitter_window.Label2.configure(disabledforeground="#a3a3a3")
    transmitter_window.Label2.configure(foreground="#000000")
    transmitter_window.Label2.configure(text='''MESSAGE''')
    
    transmitter_window.message = tk.Text(transmitter_window)
    transmitter_window.message.place(relx=0.383, rely=0.368, relheight=0.125
                    , relwidth=0.59)
    transmitter_window.message.configure(background="white")

    transmitter_window.message.configure(foreground="black")
    transmitter_window.message.configure(highlightbackground="#00ff00")
    transmitter_window.message.configure(highlightcolor="black")
    transmitter_window.message.configure(insertbackground="black")
    transmitter_window.message.configure(selectbackground="#c4c4c4")
    transmitter_window.message.configure(selectforeground="black")
    
    

    transmitter_window.transmit = tk.Button(transmitter_window)
    transmitter_window.transmit.place(relx=0.133, rely=0.699, height=44, width=177)
    transmitter_window.transmit.configure(activebackground="#ececec")
    transmitter_window.transmit.configure(activeforeground="#000000")
    transmitter_window.transmit.configure(background="#d9d9d9")
    transmitter_window.transmit.configure(command=trans)
    transmitter_window.transmit.configure(disabledforeground="#a3a3a3")
    transmitter_window.transmit.configure(foreground="#000000")
    transmitter_window.transmit.configure(highlightbackground="#d9d9d9")
    transmitter_window.transmit.configure(highlightcolor="black")
    transmitter_window.transmit.configure(pady="0")
    transmitter_window.transmit.configure(text='''TRANSMIT''')

    transmitter_window.menu = tk.Button(transmitter_window)
    transmitter_window.menu.place(relx=0.533, rely=0.699, height=44, width=177)
    transmitter_window.menu.configure(activebackground="#ececec")
    transmitter_window.menu.configure(activeforeground="#000000")
    transmitter_window.menu.configure(background="#d9d9d9")
    transmitter_window.menu.configure(command=menu1)
    transmitter_window.menu.configure(disabledforeground="#a3a3a3")
    transmitter_window.menu.configure(foreground="#000000")
    transmitter_window.menu.configure(highlightbackground="#d9d9d9")
    transmitter_window.menu.configure(highlightcolor="black")
    transmitter_window.menu.configure(pady="0")
    transmitter_window.menu.configure(text='''MENU''')
#==========================================================================function for receiver window open
def open_receiver():
    global receiver_window
    receiver_window=tk.Tk()
    receiver_window.geometry("600x273+300+100")
    receiver_window.minsize(120, 1)
    receiver_window.maxsize(1370, 749)
    receiver_window.resizable(0, 0)
    receiver_window.title("RECEIVER")
    receiver_window.configure(background="#c6e8ec")

    receiver_window.Label1 = tk.Label(receiver_window)
    receiver_window.Label1.place(relx=0.25, rely=0.035, height=61, width=274)
    receiver_window.Label1.configure(background="#c7ebeb")
    receiver_window.Label1.configure(disabledforeground="#a3a3a3")
    receiver_window.Label1.configure(foreground="#000000")
    receiver_window.Label1.configure(text='''RECEIVER''')

    receiver_window.receive = tk.Button(receiver_window)
    receiver_window.receive.place(relx=0.3, rely=0.315, height=54, width=217)
    receiver_window.receive.configure(activebackground="#ececec")
    receiver_window.receive.configure(activeforeground="#000000")
    receiver_window.receive.configure(background="#d9d9d9")
    receiver_window.receive.configure(command=recei)
    receiver_window.receive.configure(disabledforeground="#a3a3a3")
    receiver_window.receive.configure(foreground="#000000")
    receiver_window.receive.configure(highlightbackground="#d9d9d9")
    receiver_window.receive.configure(highlightcolor="black")
    receiver_window.receive.configure(pady="0")
    receiver_window.receive.configure(text='''RECEIVE''')

    receiver_window.Label2 = tk.Label(receiver_window)
    receiver_window.Label2.place(relx=0.05, rely=0.559, height=31, width=184)
    receiver_window.Label2.configure(background="#d9d9d9")
    receiver_window.Label2.configure(disabledforeground="#a3a3a3")
    receiver_window.Label2.configure(foreground="#000000")
    receiver_window.Label2.configure(text='''MESSAGE''')

    receiver_window.Text1 = tk.Text(receiver_window)
    receiver_window.Text1.place(relx=0.383, rely=0.559, relheight=0.119, relwidth=0.59)
    receiver_window.Text1.configure(background="white")

    receiver_window.Text1.configure(foreground="black")
    receiver_window.Text1.configure(highlightbackground="#d9d9d9")
    receiver_window.Text1.configure(highlightcolor="black")
    receiver_window.Text1.configure(insertbackground="black")
    receiver_window.Text1.configure(selectbackground="#c4c4c4")
    receiver_window.Text1.configure(selectforeground="black")
    receiver_window.Text1.configure(wrap="word")

    receiver_window.Button1 = tk.Button(receiver_window)
    receiver_window.Button1.place(relx=0.367, rely=0.804, height=44, width=137)
    receiver_window.Button1.configure(activebackground="#ececec")
    receiver_window.Button1.configure(activeforeground="#000000")
    receiver_window.Button1.configure(background="#d9d9d9")
    receiver_window.Button1.configure(command=menu2)
    receiver_window.Button1.configure(disabledforeground="#a3a3a3")
    receiver_window.Button1.configure(foreground="#000000")
    receiver_window.Button1.configure(highlightbackground="#d9d9d9")
    receiver_window.Button1.configure(highlightcolor="black")
    receiver_window.Button1.configure(pady="0")
    receiver_window.Button1.configure(text='''MENU''')    

#==========================================================================
open_transceiver()
transceiver_window.mainloop()
transmitter_window.mainloop()
receiver_window.mainloop()




