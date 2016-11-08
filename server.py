import argparse
import time
import socket
import threading

max_threads = 10
HOST = "10.62.0.145"
BUFFER = 1024
UTF = "utf-8"
RESPONSE_PACKET_ONE = 1
RESPONSE_PACKET_TWO = 2
STUDENT_ID = "13319349"
allThreadsWorking = []
waiting_conns = []

def sendResponse(clientSocket, address, port):
        print ("Thread doing work....")
        data = (clientSocket.recv(BUFFER)).decode(UTF)
        whichPacket = handleInput(data)
        if whichPacket == RESPONSE_PACKET_ONE:
                response = "HELO BASE_TEST\nIP:%s\nPort:%d\nStudentID:[%s]" % (HOST, port, STUDENT_ID)
                clientSocket.sendall(response.encode())
                clientSocket.close()
        elif whichPacket == RESPONSE_PACKET_TWO:
                clientSocket.close()
        print ("Thread finished!\nClosed connection!")
	

def handleInput(data):
	if ("HELO" in data):
		return RESPONSE_PACKET_ONE
	elif ("KILL_SERVICE" in data):
		return RESPONSE_PACKET_TWO

def main():
	parser = argparse.ArgumentParser(description='Start server on port entered')
	parser.add_argument("-start", help="port number on which to start server")
	args = parser.parse_args()

	if (args.start):
		PORT = int(args.start)
	else:
		PORT = 8000
		
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)

	while 1:
		print ("Waiting for client connections...")
		#accept connections from outside
		(clientsocket, address) = serversocket.accept()
		waiting_conns.append((clientsocket, address))
		print ("Current amount of queued connections: %d" % (len(waiting_conns)))

		for t in allThreadsWorking:
				if (not t.isAlive()):
					allThreadsWorking.remove(t)
					print ("Removed an unworking thread from the pool.")

		if (len(allThreadsWorking) <= max_threads): #can create a new thread
			connTuple = waiting_conns.pop()
			clsocket = connTuple[0]
			address = connTuple[1]
			thread = threading.Thread(target=sendResponse, args = (clsocket, address, PORT))
			allThreadsWorking.append(thread)
			thread.start()
			print ("Current working threads: " + str(len(allThreadsWorking)))
		print ("Still Current amount of queued connections: %d" % (len(waiting_conns)))

main()
