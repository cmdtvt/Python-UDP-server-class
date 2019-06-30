import socket
from threading import Thread
from time import sleep
from onlineUtilities import *


        


SERVER_IP = "192.168.10.60"
SERVER_PORT = 5000

CLIENT_IP = "192.168.10.60"
CLIENT_PORT = int(input()) #### The port where client waits for connections.


manager = packetMaker()
manager.addToPacket("FIRSTCONNECT")
manager.addToPacket(CLIENT_PORT)

DATA = manager.getPacket()


#DATA = "FIRSTCONNECT"+","+str(CLIENT_PORT)

HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
print("My Address Is: "+str(IPADDRESS))

DATA = str.encode(str(DATA))
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
send_sock.sendto(DATA, (SERVER_IP, SERVER_PORT))




recieve_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
recieve_sock.bind((CLIENT_IP, CLIENT_PORT))

print("Waiting server for client id...")
run = True
while run == True:
    data,address = recieve_sock.recvfrom(1024)
    print(data)
    data = data.decode()
    
    manager = packetMaker()
    manager.loadPacket(data)
    data = manager.getPacketRaw()

    if data[0] == "FIRSTCONNECT":
        print("Recieved Client id: "+str(data[1])+"\n\n")
    if data[0] == "MESSAGE":
        print("Message from server: "+str(data[1])+"\n")
