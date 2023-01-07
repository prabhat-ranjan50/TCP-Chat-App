import socket       # importing socket library for socket interface
import threading    # import thereading for making use of multithreading as we're going to use different threads for diffrent clients

class myServer:         # server class

    def __init__(self) -> None:     # sever class constructor
            
        self.PORT = 5050        # port on which the server will run
        self.ADDRESS  = socket.gethostbyname(socket.gethostname())      # ip address for the server.
        self.ADDR = (self.ADDRESS, self.PORT)       # tuple for server ip address and port address for the bind function
        self.FORMAT = 'utf-8'   # encoding scheme
        self.clients = []   # list for keeping connect clients  
        self.names = []     # list for keeping names of connected clients


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # creating the sever socket of type TCP
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # setting the server PORT address reusable by the server so that we dont have to wait if we dissconected the sever and tried reconnecting
        self.server.bind(self.ADDR)     # binding the server to the ip address and port address defined above.
        self.start()    # call the start function for socket starting the connection


    def start(self):

        print('Starting server')    # echo that the server is starting
        self.server.listen()    # start listening for client request
        print(f'Server is listening on {self.ADDR}')    # ehco the that server is listening on the server ip address
        while True: # keeping looping untill we close the server.
            client, addr = self.server.accept() # accept any client connection that are incoming 
            self.startThread(client, addr)      # make and start a thread for the current new client
            print(len(self.clients))


    
    def sendMsg(self, client, msg, name):    # function for sending messages to clinets 
        if name:    # check if there is a valid name , if so then set the formatted message of the form (name : message)
            message = f'{name.strip()}: {msg.decode(self.FORMAT)}'.encode(self.FORMAT)  # formatting 
        else:
            message = msg       # if name is not valid then just keep the message unformatted

        client.send(message)        # the the final message to the specified client.


    
    def broadcast(self, msg, name):     # function for broadcasting the message to all the connected clients

        for client in self.clients:     # loop through the clients list for every client.
            self.sendMsg(client, msg, name)     # send the msg to the client in current iteration


    def startThread(self, client, addr):        # a helper function for craeting and starrting a new thread for a client.
        print(f'Connection established with {addr}')    # print the ip of the newly connected client.
        client.send('Name?: '.encode(self.FORMAT))      # send a msg for asking the name of the client.
        try:
            name = client.recv(1024).decode(self.FORMAT)    # receive the name responce of the client.
        except UnicodeDecodeError:      # check for any errors while decoding the responce
            client.send('closing your connection'.encode(self.FORMAT))  # send msg to client that connection is unsuccessful
            client.close()  # close the socket
            return  # exit the function
        
        self.clients.append(client)     # if connection is good then add the client address to the clients list
        self.names.append(name) # add the name of the client to list of names 
        print(name)             # print the name of the client
        self.broadcast(f'{name.strip()} has joined the chat!\n'.encode(self.FORMAT), None)      # broadcast the message to all the clients
        thread = threading.Thread(target=self.handle_client, args=(client, addr))       # make a new thread for handling the client
        thread.start()  # start the thread 


    def handle_client(self, client, addr):      # fucntion for handling the client

        # while the connection of the client is active keep recving
        while True: 
            i = self.clients.index(client)      # get the index of the client
            name = self.names[i]                # get the name from the names list
            try:
                msg = client.recv(1024)         # receiving msgs from the client
                self.broadcast(msg, name)       # broadcast it to all other clients
            except:
                self.clients.remove(client)     # if connection is broken then remove client from clients list
                self.names.remove(name)         # also remove the name of client from names list
                self.broadcast(f'{name.strip()} has left the chat!'.encode(self.FORMAT), None)      # broadcast that this client has left the chat
                client.close()                  # close the socket 
                break                           # break out of the loop


if __name__ == '__main__':
    server = myServer()                         # make an instance of the server class
    server.start()                              # start the server 
            



            







