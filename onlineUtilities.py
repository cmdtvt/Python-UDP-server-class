#### This file contains classes and functions for client / server for network connections. ####


import json

#### First implementation of packetMaker ####
class packetManager():
    def __init__(self,):
        self.commands = {}

    def addCommand(self,name,command):
        self.commands[name] = str(command)
        print("Command: "+name+" with data: "+str(command))

    def listAllCommands(self,):
        print("Listing all binded commands")
        for command in self.commands: 
            print(str(command)+" / "+str(self.commands[command]))

    def dictToString(self,):
        return (json.dumps(self.commands))



#### Newer version of packetManager ####
class packetMaker():
    def __init__(self,):
        self.list = []
        self.compiledpacket = ""

    def addToPacket(self,data):
        self.list.append(str(data))
        print("PacketMaker: "+str(data)+" was added to packet!")

    #### Make list into a string ####
    def compilePacket(self,):
        string = ""
        for i in range(len(self.list)):
            #### Check for that if is last item dont add ',' to the end. ####
            if not i == len(self.list)-1:
                string = string + self.list[i] + ","
            else:
                string = string + self.list[i]

        self.compiledpacket = string
        print("PacketMaker: Packet compiled: "+self.compiledpacket)

    #### Make string into a packet ####
    def loadPacket(self,string):
        itemlist = []
        print("PacketMaker: Loading packet!")
        itemlist = string.split (',')
        print("PacketMaker: Found "+str(len(itemlist))+" commands!")
        self.list = itemlist
        print("PacketMaker: Loading Done!")

    #### Return all packet information in string format. (For sending) ####
    def getPacket(self,):
        self.compilePacket()
        print("PacketMaker: "+str(self.compiledpacket)+" was given!")
        return str(self.compiledpacket);

    #### Return all packet information in list format ####
    def getPacketRaw(self,):
        return self.list;
