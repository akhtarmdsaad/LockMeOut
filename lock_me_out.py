from tkinter import *
import time,datetime, os
root=Tk()
root.geometry('620x500')
st = time.time()
SHUTDOWN_ST = None
timings=[]

# Shutdown the pc after timeout expires from block state of pc
TIMEOUT = 10


def add_time(name,st:tuple,et:tuple,description,date=None):
    if date:
        if isinstance(date,datetime.date):
            timings.append((name,*st,*et,description,date))
        else:
            print("date should be instance of datetime.date")
            return False
    else:
        timings.append((name,*st,*et,description))
    return  True

add_time("Sleep",(20,0),(23,30),"Sleep")

l = Label(root,text='Transfer',font=('Times new roman',40),fg='Black',bg="white")
name = Label(root,text="Use The Pc :)",font=('Times new roman',50),fg="green",bg="black")

title_block = "Use The Pc :)"

def runme(*args):   
    global SHUTDOWN_ST
    l.after(1000,runme) 
    l.config(text=time.strftime("%I:%M:%S %p"))
    
    now = datetime.datetime.now()
    block_pc = False
    warn_user = False
    for i in timings:
        if len(i) == 7:
            if datetime.date.today() != i[6]:
                continue
        if now.hour >= i[1] and now.minute >= i[2]-5 and now.hour  <= i[3]:
            if now.hour == i[3] and now.minute > i[4]:
                warn_user = False
            else:
                warn_user = True 
                title_block = i[0]
                break
                
    for i in timings:
        # verify length 
        if len(i) == 7:
            if datetime.date.today() != i[6]:
                continue
        if now.hour >= i[1] and now.minute >= i[2] and now.hour  <= i[3]:
            if now.hour == i[3] and now.minute > i[4]:
                block_pc = False
            else:
                warn_user = False
                block_pc = True
                if not SHUTDOWN_ST:
                    SHUTDOWN_ST = time.time()
                title_block = i[0]
                break
    if warn_user:
        name.config(text=title_block,fg = "yellow",bg="white")
        root.deiconify()
    elif block_pc:
        if time.time() - SHUTDOWN_ST > TIMEOUT:
            os.system("shutdown /s")
            title_block = "SHUTTING DOWN"
        name.config(text=title_block,fg = "red",bg="white")
        root.attributes("-topmost",True)
        root.state("zoomed")
        
    else:
        name.config(text="Enjoy !!",fg="green",bg="white")

# Dont allow the close button
def disable_event():
    pass
root.protocol("WM_DELETE_WINDOW",disable_event)

name.pack()
l.pack(pady=20)


runme()
root.mainloop()