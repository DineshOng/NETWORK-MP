##### NETWORK S19 Machine Project
#### Altea, Dagdag, Ong
### April 2, 2017
import socket
import threading
import time
from Tkinter import *
import random
import tkMessageBox

tlock = threading.Lock()
shutdown = False

score=-1
timeleft=60
word=""

add=[]
 
host = socket.gethostbyname(socket.gethostname())
add.append(host)
port = 0

def receving(name, sock):
    global word
    while not shutdown:
        try:
            tlock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                if str(data)[3] is '.' and str(data)[11] is ':' and "has disconnected" not in str(data):
                    if str(data)[0:11] not in add:
                        add.append(str(data)[0:11])
                    if str(data)[0:11] in add[1]:
                        player2.config(text="Player 2: "+str(data)[13:])
                    elif str(data)[0:11] in add[2]:
                        player3.config(text="Player 3: "+str(data)[13:])
                    elif str(data)[0:11] in add[3]:
                        player4.config(text="Player 4: "+str(data)[13:])
                elif str(data)[11] is ' ' and add[0] in str(data) :
                    word=str(data)[12:]
                elif "has disconnected" in str(data) :
                    if str(data)[0:11] in add[1]:
                        player2.config(text="Player 2: disconnected")
                    elif str(data)[0:11] in add[2]:
                        player3.config(text="Player 3: disconnected")
                    elif str(data)[0:11] in add[3]:
                        player4.config(text="Player 4: disconnected")
        except:
            pass
        finally:
            tlock.release()

server = ('192.168.1.2', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

def startGame(event):
    if timeleft == 60:
        countdown()
        
    nextWord()

def nextWord():
    global score
    global timeleft
    
    if timeleft > 0:

        e.focus_set()

        if e.get().lower() == word.lower():
            score += 1
            s.sendto(socket.gethostbyname(socket.gethostname())+": " + str(score), server)
            tlock.acquire()
            tlock.release()
            time.sleep(0.1)
            e.delete(0, END)
            
        label.config(text=word)
        scoreLabel.config(text="Your Score: " + str(score))
        
def countdown():
    global timeleft
    global score
    
    if timeleft > 0:

        timeleft -= 1
        timeLabel.config(text="Time left: " + str(timeleft))
        timeLabel.after(1000, countdown)

    else :
        tkMessageBox.showinfo("Game Over", "Your score: "+str(score))
        scoreLabel.config(text="Press enter to start again")
        score=0
        timeleft=60
        startGame
        
app = Tk()
app.title("Typing Maniac")
app.geometry("900x300")

instructions = Label(app, text="Typing Maniac!", font=('Helvetica', 36))
instructions.pack()

timeLabel = Label(app, text="Time left: " + str(timeleft), font=('Helvetica', 12))
timeLabel.pack()

label = Label(app, font=('Helvetica', 60))
label.pack()

e = Entry(app)
app.bind('<Return>', startGame)
e.pack()
e.focus_set()

scoreLabel = Label(app, text="Press enter to start", font=('Helvetica', 12))
scoreLabel.pack()

player2=Label(app, text="Player 2")
player2.pack()

player3=Label(app, text="Player 3")
player3.pack()

player4=Label(app, text="Player 4")
player4.pack()

app.mainloop()

s.sendto(socket.gethostbyname(socket.gethostname())+ " has disconnected", server)
shutdown = True
rT.join()
s.close()
