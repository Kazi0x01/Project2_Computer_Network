import pickle
import socket
import threading
from pickle_data import get_event
from pickle_data import HEADERSIZE

SND_PT = 3434

try:
    sock_fd  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Initialization a UDP socket
    print("[+] socket created")
except socket.error as err:     # Catch any errors or exception thrown during initialization 
    print("[-] Error failed to create socket")
    raise

m_port = int(input("[*] Enter the port for socket :"))  # Input port number for socket  

# Exceptional handling 
try:
    sock_fd.bind(('0.0.0.0', m_port))   #Binding the socket to the user defined port
    print("[+] socket binded")
except socket.error as err:          #Catching any error or exception thrown during binding process
    print("[-] Error failed to bind the socket")
    raise


addr = raw_input('[*] Enter the address of peer :') #Taking peer_address as input from userv
port = int(input('[*] Enter the port of peer : '))  #Takign peer_port as input from user


msg = sock_fd.recv(1024).decode()   #Receiving UDP packet from any address send to m_port 


print('[+] Peer msg {}'.format(msg))

sock_fd.sendto(b'\n[+] Hi from peer2', (addr, port))





print("[+] Connected to peer")
print("[*] Address : {}".format(addr))
print("[*] Port : {}".format(port))

#Subroutine for the thread which listen for any incoming socket connection 
def l_subroutine():
    try:
        sock_fd  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #Initialization a UDP socket
        print("[+] socket created")
    except socket.error as err:     # Catch any errors or exception thrown during initialization 
        print("[-] Error failed to create socket")
        raise

    try:
        sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Setting socket option to reuse the addresss
        try:
            sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)   #Setting socket option to reuse the port
        except AttributeError:
            print("[-] Error setting option")
            raise
    except socket.error as err:
        print("[-] Error setting option") 
        raise

    sock_fd.bind(('0.0.0.0', m_port)) #Binding the socket to port m_port
    while True:
        msg = sock_fd.recv(1024).decode()
        # print(pickle.loads(msg[HEADERSIZE:]))
        print("[+]peer_msg: {}".format(msg))

    


s_thread = threading.Thread(target=l_subroutine)    #Creating a thread for listening on the port
s_thread.daemon = True  # Making the thread low priority daemon in order to use it as backgorund process
sock_fd.close() #closing any open sockets
s_thread.start()

try:
    sock_fd  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #Initialization a UDP socket
    print("[+] socket created")
except socket.error as err:     # Catch any errors or exception thrown during initialization 
    print("[-] Error failed to create socket")
    raise

try:
    sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Setting socket option to reuse the addresss
    try:
        sock_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)   #Setting socket option to reuse the port
    except AttributeError:
        print("[-] Error setting option")
        raise
except socket.error as err:
    print("[-] Error setting option")    
    raise

sock_fd.bind(('0.0.0.0',SND_PT))
while True:
    msg = raw_input('> ')


    if msg == "EVENT":
        pkl_data = get_event()
        sock_fd.sendto(pkl_data, (addr, port))
    else:
        msg = pickle.dumps(msg)
        msg = bytes("{}".format(len(msg) < HEADERSIZE).encode('utf-8'))+msg
        sock_fd.sendto(msg.encode(), (addr, port))


