#Revathy Ramamoorthy
#https://realpython.com/python-sockets/
#https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
#https://www.geeksforgeeks.org/socket-programming-python/
#https://stackabuse.com/basic-socket-programming-in-python/
#https://www.youtube.com/watch?v=SepyXsvWVfo
#https://stackoverflow.com/questions/2905965/creating-threads-in-python
#https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
#https://www.tutorialspoint.com/python/python_gui_programming.htm
#http://effbot.org/tkinterbook/label.htm
import socket
import threading
from tkinter import *
import select
import time



#function that connects student socket to MQS
def student_process():
    try:
        host = '127.0.0.1'
        port = 5000
        global client
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Client socket creation
        client.connect((host,port))      #Connection
        print("connected")
        s_name = "student"
        sc_name=s_name
        client.send(s_name.encode('utf8'))		#Sending username - Registration
        while (1):
                print("Please input the following details :")
                message0 = input("Enter your name")	 #Getting student name and course name to send to MQS
                message1=input("Enter course name")
                message2=message0 +"\n" + message1
                client.send(message2.encode('utf-8'))	#Sending message
                print("\nDetails added to queue successfully")
    except select.error:	#error handling
        print("error")
        client.close()

#student gui
def studentgui():
    win = Tk()
    win.geometry('200x400')
    print("Student GUI started")
    global b
    global vLabel												#variables to store values to be diaplayed on the gui label
    global headerLabel
    global srLabel
    srLabel = StringVar()
    srLabel.set("Student GUI")
    headerLabel = Label(win, textvariable=srLabel, fg="blue", font=("Helvetica", 16))
    headerLabel.pack()
    vLabel = StringVar()
    b = Label(win, textvariable=vLabel, fg="blue", font=("Helvetica", 16)) #Label to display message
    b.pack()
    button = Button(win, text='close', width=30, command=win.quit())	 #To close the connection
    button.pack()
    win.mainloop()

#main function that starts student process thread and student gui thread
if __name__ == '__main__':
    threading.Thread(target=studentgui).start()
    time.sleep(2)
    threading.Thread(target=student_process).start() #Starting thread
