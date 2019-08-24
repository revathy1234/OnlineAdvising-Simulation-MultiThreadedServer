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

#client gui
def gui():
    win = Tk()
    win.geometry('200x400')
    print("Advisor GUI started")
    global b
    global vLabel
    global headerLabel										#variables to store values to be diaplayed on the gui label
    global srLabel
    srLabel = StringVar()
    srLabel.set("Advisor GUI")
    headerLabel = Label(win, textvariable=srLabel, fg="blue", font=("Helvetica", 16))
    headerLabel.pack()
    vLabel = StringVar()
    b = Label(win, textvariable=vLabel, fg="blue", font=("Helvetica", 16)) #Label to display message
    b.pack()
    button = Button(win, text='close', width=30, command=win.quit())	 #To close the connection
    button.pack()
    win.mainloop()



#function that connects advisor socket to MQS
def advisor_process():
	try:
		host = '127.0.0.1'
		port = 5000
		global client
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Client socket creation
		client.connect((host,port))      #Connection
		print("connected")
		s_name = "advisor"
		sc_name=s_name
		client.send(s_name.encode('utf8'))		#Sending username - Registration
		try:
			while (1):
				data=client.recv(1024).decode('utf-8')		#getting response from MQS
				if(data == "NO messages"):
					print("NO messages")
				else:
					vLabel.set(data)
					print("Decision printed successfully")		#printing to the gui
		except select.error:
				print("error")
				client.close()
	except select.error:	#error handling
		print("error")
		client.close()

#main function that starts advisor process thread and advisor gui thread
if __name__ == '__main__':
	threading.Thread(target=gui).start()
	time.sleep(2)
	threading.Thread(target=advisor_process).start() #Starting thread

	