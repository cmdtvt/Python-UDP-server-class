import socket
import json
from threading import Thread
from tkinter import *
from time import sleep
from onlineUtilities import *

class main_loop(Thread):
    def __init__(self,):
        print("Loop Thread has been started!")
        self.run = True
        self.tickspeed = 1 #How many seconds mainloop waits until its ran again.

            
    def shutdown(self,):
        self.run = False





class Client():
    def __init__(self,ip,port,clientid):

        #### ip of the client ####
        self.ip = ip
        #### Port wich client is expecting connection ####
        self.port = port
        self.id = clientid
        
    def setID(self,clientid):
        self.id = clientid
        print("Client id set to: "+str(self.id))

    def getID(self,):
        return self.id

    def getClientInfo(self,):
        return [self.ip,self.port,self.id]







        
class Server():
    def __init__(self,serverip,serverport):
        self.debug = True
        self.clients = []
        self.clientid = 0
        self.SERVER_IP = serverip
        self.SERVER_PORT = serverport
        self.recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP

        print("____ SERVER CLASS HAS STARTED ____")

    def PrintAsServer(self,message):
        if self.debug == True:
            print("## SERVER: ## "+str(message))

    #### Check if client has id and is registered. ####
    def checkClientIsRegistred(self,userid):
       
        for i in self.clients:
            if i.id == userid:
                return True;
        return False;
        #### if i in [x.id for x in list] ####

    #### Return all client info ####
    def getClientInfo(self,userid):
        if not self.checkClientIsRegistred(userid) == True:
            self.PrintAsServer("Client not found...")
        else:
            clientinfo = []
            for i in self.clients:
                if i.id == userid:
                    clientinfo = i.getClientInfo()
            return clientinfo;
            
    #### Register client as new and send back client id. ####
    def registerClient(ip,port,clientid):
        try:
            newclient = Client(ip,port,clientid)
            self.clients.append(newclient)
            self.PrintAsServer("New Client has been registerd!")
            return True;
        
        except:
            self.printAsServer("Could not register new Client!")
            return False;

    #### Wait for connections and deal with them ####
    def Update(self,):
        localsocket = self.recieve_socket
        localsocket.bind((self.SERVER_IP, self.SERVER_PORT))
        while True:

            #### Recieve data and turn it into readable format ####
            #### Data is recieved data and address is IP address and PORT where connection came from ####
            data,address = localsocket.recvfrom(1024)
            self.PrintAsServer("Incoming connection!")
            data = data.decode()
            manager = packetMaker()
            manager.loadPacket(data)
            data = manager.getPacketRaw()
            #print(address)
            print("DATA: "+str(data))

            if data[0] == "FIRSTCONNECT":




                
                self.PrintAsServer("New connection request! Registering as new client!")
                #### Register new client with IP port and clientid ####
                newclient = Client(address[0],data[1],self.clientid)
                self.clients.append(newclient)



                


                #### Create Packet with clientid ####
                manager = packetMaker()
                manager.addToPacket("FIRSTCONNECT")
                manager.addToPacket(self.clientid)
                DATA = manager.getPacket()



                

                #### Send packet to client with id ####
                if self.sendTo(self.clientid,DATA) == True:
                    self.PrintAsServer("Clientid sent!")
                else:
                    self.PrintAsServer("Error in sending client id!")

                
                self.clientid += 1
                self.PrintAsServer("Client has been registered!")
                print(self.clients)

                manager = packetMaker()
                manager.addToPacket("MESSAGE")
                manager.addToPacket("New client has connected!")

                self.sendToAll(manager.getPacket())

            
            
    #### Send data to user with id ####
    #### Unfinished
    def sendTo(self,userid,DATA):
        print("sendto userid : "+str(userid))
        info = self.getClientInfo(userid)
        print(info)

        DATA = str.encode(str(DATA))
        #### DATA , IP, PORT ####
        localsocket = self.send_socket
        localsocket.sendto(DATA, (info[0], int(info[1])))

    def sendToAll(self,DATA):
        for i in self.clients:
            self.sendTo(i.id,DATA)

    


#server = Server("192.168.10.60",5000)
#server.Update()




    
