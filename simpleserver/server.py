from socket import *
import random   
import struct         

server = socket(AF_INET, SOCK_DGRAM)      
server_ip = ''
server_port = 12000
datalen = 10000
server.bind((server_ip, server_port))     
print("The server is ready on port: ", server_port)
response_num = 2


while True:
	rand_num = random.randint(0, 10)
	data, address = server.recvfrom(datalen)
	data = struct.unpack('!II', data)
	seq_num = data[0]
	request_num = data[1] 
	if rand_num < 4:
		print("Message with sequence num:", seq_num, "dropped")
	else:
		msg = struct.pack("!II", seq_num, response_num)
		print("Responding to ping request with sequence num:", seq_num)
		server.sendto(msg, address) 

server.close()