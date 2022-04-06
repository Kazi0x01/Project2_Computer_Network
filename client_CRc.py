import pickle
import socket
import threading
from pickle_data import get_event
from pickle_data import HEADERSIZE


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


# addr = raw_input('[*] Enter the address of peer :') #Taking peer_address as input from userv
# port = int(input('[*] Enter the port of peer : '))  #Takign peer_port as input from user


# msg = sock_fd.recv(1024).decode()   #Receiving UDP packet from any address send to m_port 


# print('[+] Peer msg {}'.format(msg))

# sock_fd.sendto(b'\n[+] Hi from peer2', (addr, port))





# print("[+] Connected to peer")
# print("[*] Address : {}".format(addr))
# print("[*] Port : {}".format(port))

def xor(x, y):
    res = []
    for i in range(1, len(y)): 
        if x[i] == y[i]: #flip bits when nesscary
            res.append('0')
        else:
            res.append('1')
    return ''.join(res)




def crc(data, G):

    msb = len(G) # get lenght of the divisor so we can segement the data  
    seg = data[0 : msb] # segment data
 
    while msb  < len(G): #start divission algorithim 
 
        if seg[0] == '1': #if divided in  xor to get next segment of focus
            seg= xor(G, seg) + data[msb] #carry down next bit
 
        else:  #if does not divide in the xor with 0 
            seg = xor('0'*msb, seg) + data[msb] #carry down next bit
 
        seg  += 1 #increment to mover across data
 
    if seg[0] == '1': #last loop of the algorithm 
        seg = xor(data, seg)
    else:
        seg = xor('0'*msb, seg)
 
    R = msb
    return R

def encoder(data, G):

    lenght_G = len(G)   
    data_crc = data + '0'*(lenght_G-1)  # add extra zeros for crc
    remainder =crc(data_crc, G) #find the reminder of the crc
    encodeddata = data + str(remainder) #add this remainder onto the end
    return encodeddata    


def decoder(data, G):
    lenght_G = len(G)   
    data_crc = data + '0'*(lenght_G-1)  # add extra zeros for crc
    remainder =crc(data_crc, G) #find the reminder of the crc

    return str(remainder)
  

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
        # print("[+]peer_msg: {}".format(pickle.loads(msg)))

        
        G = "1001" #same G on both peers

        R = decoder(msg, G)
    
        temp = "0" * (len(G) - 1) #if the remainder is all zeros 
        if R == temp:
            print("Remainder= "+ R + "no errors found")
        else:
            print("Remainder= "+ R + "errors detected")

            print("[+]peer_msg: {}".format(pickle.loads(msg)))


    


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

 


    


while True:
    input = raw_input('> ')

    bin_data  = pickle.dumps(input) #covert string to binary
    G= "1001"                                           #four bit checker
    msg = encoder(bin_data,G)

    addr = raw_input('[*] Enter the address of peer :') #Taking peer_address as input from userv
    port = int(raw_input('[*] Enter the port of peer : '))  #Takign peer_port as input from user


    if msg == "EVENT":
        pkl_data = get_event()
        sock_fd.sendto(pkl_data, (addr, port))
    else:
        # msg = pickle.dumps(msg)  #check if this works 
       
        sock_fd.sendto(msg, (addr, port))



 







