##### NETWORK S19 Machine Project
#### Altea, Dagdag, Ong
### April 2, 2017
import socket
import random

host = socket.gethostbyname(socket.gethostname())
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

quitting = False
print "Server Started."

words = []
lines = open('enable2k.txt').read().splitlines()
for x in range(50):
    myline=random.choice(lines)
    words.append(myline)

print words[0]
print words[1]

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
        print str(data)
        for client in clients:
              s.sendto(data, client)
              if "has disconnected" not in str(data):
                  s.sendto(data[0:11]+" "+words[int(str(data)[13:])], client)
    except:
        pass
    
s.close()
            

