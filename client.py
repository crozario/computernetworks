from socket import *
import time
import struct
import sys

argv = sys.argv
server_ip = argv[1] 
server_port = int(argv[2]) 

total_requests = 10
client = socket(AF_INET, SOCK_DGRAM)   
client.settimeout(1)      

request_num = 1
seq_num = 0
num_packets_sent = 0
num_packets_recv = 0
all_rtt = []

print("Pinging Server IP: ", server_ip, ", Server Port: ", server_port)

while seq_num < total_requests:
	seq_num += 1
	msg = struct.pack("!II", seq_num, request_num)

	try:
		t1 = time.time()
		client.sendto(msg, (server_ip, server_port))
		num_packets_sent += 1
		recvData, address = client.recvfrom(len(msg))
		t2 = time.time()		
	except timeout:
		print("Sequence Num:", seq_num, "Message timed out")
	else:
		rtt = t2 - t1
		all_rtt.append(rtt)
		recvData = struct.unpack("!II", recvData)
		num_packets_recv += 1
		s_num = recvData[0]
		response_num = recvData[1]
		print("Sequence Num:", seq_num, "RTT: {0:.5f}".format(rtt))

loss = (1 - num_packets_recv/num_packets_sent) * 100
min_rtt = min(all_rtt)
max_rtt = max(all_rtt)
print(max_rtt)
print(min_rtt)
average_rtt = sum(all_rtt)/len(all_rtt)
print("Num of packets sent:", num_packets_sent, "Received:", num_packets_recv, "Loss rate: {0:.2f}%".format(loss))
print("Min RTT: {} Max RTT: {} Average RTT: {}".format(min_rtt, max_rtt, average_rtt))

client.close()

