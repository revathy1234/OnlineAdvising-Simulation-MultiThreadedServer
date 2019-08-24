#Revathy Ramamoorthy
#https://www.geeksforgeeks.org/writing-files-background-python/
#https://pymotw.com/2/socket/tcp.html
#https://www.youtube.com/watch?v=SepyXsvWVfo
#http://effbot.org/tkinterbook/label.htm
#https://docs.python.org/3/library/threading.html#event-objects
import socket
import select
import threading
import queue
import time
import random

from tkinter import *

global q
q = queue.Queue(maxsize=100)
client_num = {}		#Dictionary to store connected clients and their socket details
message=''
a={}			#list to display connected clients
data = ""
b = ""

n = queue.Queue(maxsize=100)
#function to write messages from MQS to textfile for persistent storage
class AsyncWrite(threading.Thread):
    def __init__(self, text, out):              #https://www.geeksforgeeks.org/writing-files-background-python/
        threading.Thread.__init__(self)
        self.text = text
        self.out = out
    def run(self):
        f = open(self.out, "a")                 #opening a txt file out.txt
        f.write(self.text + '\n')                           #writing data to txt file
        f.close()
        time.sleep(2)


def servergui():
    win = Tk()
    win.geometry('400x300')
    print("Server GUI started")
    global b
    global vLabel
    global headerLabel
    global srLabel
    srLabel = StringVar()                   #variables to store values to be diaplayed on the gui label
    global xLabel
    xLabel = StringVar()
    global wLabel
    wLabel = StringVar()
    srLabel.set("Server GUI")
    headerLabel = Label(win, textvariable=srLabel, fg="blue", font=("Helvetica", 16))
    headerLabel.pack()
    vLabel = StringVar()
    b = Label(win, textvariable=vLabel, fg="blue", font=("Helvetica", 16)) #Label to display message
    b.pack()
    c = Label(win, textvariable=wLabel, fg="blue", font=("Helvetica", 16))  # Label to display message
    c.pack()
    d = Label(win, textvariable=xLabel, fg="blue", font=("Helvetica", 16))  # Label to display message
    d.pack()
    button = Button(win, text='close', width=30, command=win.quit())     #To close the connection
    button.pack()
    win.mainloop()


#function to perform connection with the clients
def server_connection():
    try:
        while (1):
            connection, client_address=server.accept()      #Accepting the client
            print(client_address[1])                        #Displaying client port number
            data1 = connection.recv(1024).decode('utf8')    #Registration with username
            source_client = str(data1)
            print('Source_client:'+source_client)           
            client_num[source_client] = connection          #Storing client details
            a[source_client]=client_address[1]
            print(client_num)
            print(a)
            if(source_client=="student"):
                vLabel.set("Student connected")
                threading.Thread(target=student, args=(connection, address)).start()
            elif(source_client=="notification"):
                xLabel.set("Notification connected")
                threading.Thread(target=notification, args=(connection, address)).start()  #thread to handle receiving and sending messages
            else:
                wLabel.set("Advisor connected")
                threading.Thread(target=advisor, args=(connection, address)).start()

    except select.error:  #error handling
        print("error")
        server.close()


#function that handles notification to students
def notification(connection,address):
        try:
            while True:
                if(n.empty()):              #polling MQS
                    msg=''
                    msg="NO messages"
                    for sock in client_num:                         #sending the queue is empty notification to the notification GUI
                            if sock=="notification":
                                client_num[sock].send(msg.encode('utf-8'))
                    time.sleep(7)               #sleeping for 7 seconds when queue is empty
                else:
                    notify=n.get()          #pulling data from MQS
                    for sock in client_num:
                            if sock=="notification":
                                client_num[sock].send(notify.encode('utf-8'))
        except select.error:                #error handling
            xLabel.set("Notification process disconnected")
            print("error")
            server.close()



#function that generates decisions for student requests
def advisor(connection,address):
        try:
            while True:
                if(q.empty()):                          #polling MQS
                    msg=''
                    msg="NO messages"
                    for sock in client_num:             #sending the queue is empty notification to the advisor GUI
                            if sock=="advisor":
                                client_num[sock].send(msg.encode('utf-8'))
                    time.sleep(3)       #sleeping for 3 seconds when queue is empty
                else:
                    x=q.get()           #pulling data from MQS
                    z=advisor_decision(x)       #function call for advisor decision
                    y=x+","+z
                    for sock in client_num:                                       #sending advisor decision to its GUI
                            if sock=="advisor":
                                client_num[sock].send(y.encode('utf-8'))
                    n.put(y)                 #adding student message to the queue                      
                    background = AsyncWrite(y, 'out.txt')
                    background.start()
        except select.error:  #error handling
            wLabel.set("Advisor process disconnected")
            print("error")
            server.close()    


#function that gives decision based on random probability
def advisor_decision(x):
    decision=''
    random_num=random.randint(0,1)
    if(random_num==0):
        decision="Approved"
    else:
        decision="Disproved"
    return decision 


            
#function to push student request in the queue
def student(connection, address):
    try:
        while True:
            student_input = connection.recv(1024).decode('utf-8')
            global data
            data = str(student_input)                       #getting students input
            m  = data
            print(m)
            q.put(m)                                    #adding student message to the queue
            background = AsyncWrite(m, 'out.txt')           #writing to txt file
            background.start()
    except socket.error:                 # https://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/
        vLabel.set("Student process disconnected")
        print("conn error")
        server.close()



#main function with threading to handle multiple concurrent client connection
if __name__ == '__main__':
    serverIP = '127.0.0.1'
    port = 5000
    address = (serverIP, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(3)
    print("listening")
    threading.Thread(target=server_connection).start()
    servergui()
