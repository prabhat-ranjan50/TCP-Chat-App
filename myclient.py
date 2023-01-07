import socket       # importing socket library for socket interface
import threading    # import thereading for making use of multithreading as we're going to use different threads for diffrent clients

class client:       # client class definition


    def __init__(self) -> None:
            
        self.PORT = 5050        # server port number
        self.ADDRESS  = socket.gethostbyname(socket.gethostname())     # server ip address (here it's taken localhost since server is on the same machine as the client)
        self.ADDR = (self.ADDRESS, self.PORT)      # tuple of server ip address and port number for passing into the connect method of socket interface
        self.FORMAT = 'utf-8'  # encoding scheme for converting the string messages into the byte form 
        # self.currRecv = '<?>'

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # creating a TCP socket for client
        
        
    def receive(self):  # function for hadling incoming messages

        while self.connected:   # keep running the thraed untill the connection is not off.
            try:
                msg = self.client_sock.recv(1024).decode(self.FORMAT)       # receive the message then deconde it to make it into a string form by using the .decode() function
                print(msg)      # print the message
            except:                 
                print('Error')      # if thre is an error then print it and close the socket, and exit the program. 
                self.client_sock.close()
                self.connected = False
                break


    def sendMsg(self):      # function for sending messages

        while self.connected:   # keep runing while the connnect is up
            try:        
                msg = input()       # get message from the terminal
                self.client_sock.send(msg.encode(self.FORMAT))  # send it to the server through the socket 
            except:
                print("Error")      # if there is an error then print error, on the screen, close the circuit and terminate the program.
                self.client_sock.close()    # close the socket
                self.connected = False      # set the variable connected to false    
                break
    


    def start(self):                # a fucntion to initialize the socket for server connection
        try:
            self.client_sock.connect(self.ADDR)     # calling the connect method of socket interface to make connection to server
        except ConnectionRefusedError:              # handing exception if any occurs while connecting
            print('Server is not Receiving Requests!!!')       
            self.client_sock.close()        # if there is an error then close the socket and exit the program
            exit(1)
        self.connected = True           # global variable for tracking connection status 
        recv = self.client_sock.recv(1024).decode(self.FORMAT)     # calling the receive method because the server will ask for name of the client
        name = input(recv)      # give the client promt for typing their name in the commnad line
        self.client_sock.send(name.encode(self.FORMAT)) # then send the name of the client after enconding it into a byte stream

        senderThread = threading.Thread(target=self.sendMsg)    # start a thread for handling outgoing (sending) messages
        recverThread = threading.Thread(target=self.receive)    # start a thread for handling incoming messages
        senderThread.start()    # start the thread
        recverThread.start()

if __name__ == '__main__':  # run the current file only 
    myclient = client() # create an instance of the client class
    myclient.start()    # call the start function to connect to the server.


