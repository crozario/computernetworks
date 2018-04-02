from socket import *  
import datetime, time
import os

def getFileLastMod(filename):
	secs = os.path.getmtime(filename)
	t = time.gmtime(secs)
	lastmod = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t)
	return lastmod

def getCurrDate():
	secs = time.time()
	t = time.gmtime(secs)
	currdate = time.strftime("%a, %d %b %Y %H:%M:%S %Z", t)
	return currdate

def getResponse(data):
	endtag = "\r\n"
	httpver = "HTTP/1.1"
	arr = data.split('\t')
	filename = arr[1]
	filename = filename[1:]
	body = ""
	status = ""
	date = "Date: " + getCurrDate()
	# print("---", arr)


	if "If-Modified-Since" in data:
		indexstart = data.find("If-Modified-Since")
		indexend = data.find("UTC")
		lastmod = data[indexstart + 19 : indexend + 3]
		lastmod = time.strptime(lastmod, "%a, %d %b %Y %H:%M:%S %Z")
		lastmod = time.mktime(lastmod)
		currmod = getFileLastMod(filename)
		currmod = time.strptime(currmod, "%a, %d %b %Y %H:%M:%S %Z")
		currmod = time.mktime(currmod)

		# print("---", currmod)
		# print("---", lastmod)
		# print(currmod == lastmod)
		if currmod != lastmod:

			status = httpver + " 304 Not Modified"
			responsestr = status + endtag + date + endtag + endtag
			return responsestr

	if arr[0] == "GET":
		try:
			file = open(filename, "r")
			body = file.read()
			# success status
			status = httpver + " 200 OK"
			file.close()

		except FileNotFoundError:
			# file not found status
			status = httpver + " 404 Not Found"


		if "200 OK" in status:
			contentbytelen = os.path.getsize(filename)
			contentlength = "Content-Length: " + str(contentbytelen)
			lastmodified = "Last-Modified: " + getFileLastMod(filename)
			contenttype = "Content-Type: text/html; charset=UTF-8"
			responsestr = status + endtag + date + endtag + lastmodified + endtag + contentlength + endtag + contenttype + endtag + endtag + body

		elif "404 Not Found" in status:
			responsestr = status + endtag + date + endtag + endtag


		return responsestr

	else:
		return "NOT A GET REQUEST"



def main():
	server = socket(AF_INET, SOCK_STREAM)      
	server_ip = ''
	server_port = 12000
	data_len = 10000
	server.bind((server_ip, server_port))     

	server.listen(1)
	print("The server is ready on port: ", server_port)
	
	
	while True:
		conn, addr = server.accept()
		print("Socket created for client " + addr[0] + ", " + str(addr[1]))

		while True:
			data = conn.recv(data_len).decode('ascii')
			print("***REQUEST RECEIVED***")
			if not data:
				conn.close()
				break
			response = getResponse(data)
			conn.send(response.encode('ascii'))
			print("***RESPONSE SENT***")
		
	server.close()
	

if __name__ == '__main__':
	main()