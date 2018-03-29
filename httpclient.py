from socket import *
import sys
import re 


def getHostAndFilename(url):
	http = "http://"
	https = "https://"
	regex = r'/[A-Za-z1-9]+.*'
	if http in url:
		newurl = url.replace(http, '')
		filename = re.search(regex, newurl).group(0)
		hostname = url.replace(filename, '')
		return [ hostname, filename ]
	elif https in url:
		newurl = url.replace(https, '')
		filename = re.search(regex, newurl).group(0)
		hostname = url.replace(filename, '')
		return [ hostname, filename ]
	else:
		filename = re.search(regex, url).group(0)
		hostname = url.replace(filename, '')
		return [ hostname, filename ]


def getRequest(hostname, filename):
	endtag = "\r\n"
	httpver = "HTTP/1.1"
	getstr = "GET" + "\t" + filename + "\t" + httpver + endtag + "Host:" + hostname + endtag + endtag 
 	
	return getstr

def conditionalGetRequest(hostname, filename, lastmodified):
	endtag = "\r\n"
	httpver = "HTTP/1.1"
	ifmodifiedsince = "If-Modified-Since: " + lastmodified 
	getstr = "GET" + "\t" + filename + "\t" + httpver + endtag + "Host:" + "\t" + hostname + endtag + ifmodifiedsince + endtag + endtag 
 	
	return getstr

def checkLastModified(data):
	return "Thu, 29 Mar 2018 03:06:32 UTC"

def main():
	argv = sys.argv
	url = argv[1] 
	client = socket(AF_INET, SOCK_STREAM)      

	hostname, filename = getHostAndFilename(url)
	client_host = "127.0.0.1"
	client_port = int(hostname.split(":")[1])

	client.connect((client_host, client_port))
	print("Connecting to " + client_host + ", " + str(client_port)) 

	
	# print("hostname:", hostname)
	# print("filename:", filename)
	data = getRequest(hostname, filename)

	client.send(data.encode('ascii'))
	print("***SENT GET REQUEST MESSAGE***")
	print(data)
	dataEcho = client.recv(1000)
	
	print("***RECEIVED GET RESPONSE MESSAGE***")
	print(dataEcho.decode('ascii'))


	lastmodified = checkLastModified(dataEcho)
	data = conditionalGetRequest(hostname, filename, lastmodified)

	client.send(data.encode('ascii'))
	print("***SENT CONDDITIONAL GET REQUEST MESSAGE***")
	print(data)
	dataEcho = client.recv(1000)
	
	print("***RECEIVED CONDITIONAL GET RESPONSE MESSAGE***")
	print(dataEcho.decode('ascii'))

	data = getRequest(hostname, "/hello.html")

	client.send(data.encode('ascii'))
	print("***SENT GET REQUEST MESSAGE***")
	print(data)
	dataEcho = client.recv(1000)
	
	print("***RECEIVED GET RESPONSE MESSAGE***")
	print(dataEcho.decode('ascii'))

	client.close()

if __name__ == '__main__':
	main()







	




