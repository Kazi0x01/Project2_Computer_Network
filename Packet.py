import pickle 
from hashlib import sha1
from string import hexdigits

from matplotlib.colors import hexColorPattern
# from termcolor import colored



class Packet:
    def __init__(self, status, data, ack, seq_num): 
        self.status = status
        self.data = data
        self.seq_num = seq_num
        self.ack = ack
        self.checksum = sha1(data).hexdigest()
    
              
    
    def dumps(self):
        return pickle.dumps(self)


    def check(self):
        return self.checksum == sha1(self.data).hexdigest()
    

    def get(self, field):
        if field == 'seq_num':
            return str(self.seq_num)
        elif field == 'data':
            return self.data
        elif field == 'status':
            return self.status
        elif field == 'ack':
            return self.ack
        elif field == 'checksum':
            return self.checksum

    # def printf(self):
    #     if self.pkt.ack == 'ACK':
    #         print(colored('Positive Ack ' + self.pkt.seq_num, color= 'green'))
    #     elif self.pkt.ack == 'NAK':
    #         print(colored('Negative Ack ' + self.pkt.seq_num, color='red'))
    #     elif self.pkt.status == 'found':
    #         print(colored('File if found, recieving', color = 'green'))
    #     elif self.pkt.status == 'not_found':
    #         print(colored('File is not found', color = 'red'))
    #     else:
    #         print(colored('Recieved Packet ' + self.pkt.seq_num, color = 'yellow'))


if __name__ == '__main__':
    msg = "Helloo I am data"
    msg = msg.encode('utf-8')

    pk = Packet("found", msg, 'ACK', 1)
    print("Status : {}".format(pk.status))
    print("Ack : {}".format(pk.ack))
    print("seq_num : {}".format(pk.seq_num))
    print("data : {}".format(pk.data))
    print("checksum : {}".format(pk.checksum))
    print("******CHECK SUM ******")
    cal_checksum = pk.check()
    print("Claculated sum : {}".format(sha1(pk.data.decode('utf-8')).hexdigest()))

    if cal_checksum:
        print("data not corrupted")
    else:
        print("corrupted !!")

    
