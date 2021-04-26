import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)
exit = False

print('########################################################')
print('##                                                    ##')
print('##           COMMAND AND CONTROL PROGRAM              ##')
print('##   Yefim Shneyderman, Anthony Rinaldi, Brendon Ky   ##')
print('##                                                    ##')
print('########################################################')

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
        print("Sending data")

    elif choice == '4' or choice == 'q' or choice == 'exit' or choice == 'Exit' or choice == 'quit':
        exit = True
        print("Exiting the C2 instance")
        print("Implant is still running - connect to it again later")

    else:
        print("Unrecognized input")