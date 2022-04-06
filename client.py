from pickle_data import get_event
from pickle_data import HEADERSIZE
from hashlib import sha1
from string import hexdigits
import pickle
import socket
import threading
import time

from crc_func import *
from Packet import *

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

#Subroutine for the thread which listen for any incoming socket connection
ack_recieved = False
def l_subroutine():
    try:
        sock_fd  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #Initialization a UDP socket
        print("[+] socket created")
    except socket.error as err:     # Catch any errors or exception thrown during initialization 
        print("[-] Error failed to create socket")
        raise

    sock_fd.bind(('0.0.0.0', m_port)) #Binding the socket to port m_port

    expected_seq_num = 0

    while True:

        package = sock_fd.recv(1024)
       
        G = "10011" #same G on both peers
        R = decoder(package, G)
        # temp = "0" * (len(G) - 1) #if the remainder is all zeros 
        # if R == temp:
        #     print("Remainder " + R + " no errors found")
        # else:
        #     print("Remainder= " + R + " errors detected")
        # print(R + " errors detected")

        rcv_packet = pickle.loads(package)
       # print(rcv_packet)
        if rcv_packet.type == 'has_data':
            if rcv_packet.check() and expected_seq_num == rcv_packet.seq_num:
                package = Packet_reciever('ACK', rcv_packet.seq_num)
                packet = pickle.dumps(package)

                sock_fd.sendto(packet, (rcv_packet.ip, int(rcv_packet.port)))
                
                print("[+] peer_msg: {}".format(rcv_packet.data))
        
        elif rcv_packet.type == 'has_ack':
            global ack_recieved
            ack_recieved = True
            print("     - Delivered")
            expected_seq_num = 1 - expected_seq_num


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


# sender's code

while True:
    msg = raw_input('[>] ')
    addr = raw_input('[*] Enter the address of peer :') #Taking peer_address as input from userv
    port = int(input('[*] Enter the port of peer : '))  #Takign peer_port as input from user

    sequence_number = 0
    ack_recieved = False
    num_of_tries = 0

    while not ack_recieved:

        if msg == "EVENT":
            pkl_data = get_event()
            package = Packet_sender(pkl_data, sequence_number, '127.0.0.1', m_port)
        else:   
            package = Packet_sender(msg, sequence_number, '127.0.0.1', m_port)
       
        bin_data  = pickle.dumps(package) #covert string to binary CRC
        G= "10011"                                           #four bit checker
        package = encoder(bin_data,G)     

        sock_fd.sendto(package, (addr, port))

        time.sleep(1)
        if(not ack_recieved):
            if num_of_tries>10:
                print("Many attempts unsuccessful, try again!")
                break
            else:
                num_of_tries+=1
                print("Retrying sending data packet...")
            
    sequence_number = 1 - sequence_number