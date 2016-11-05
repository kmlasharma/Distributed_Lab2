
import time
import socket
import threading

MINIMAL_AMOUNT = 0
MAX_AMOUNT = 3
PORT = 8000
HOST = "localhost"
BUFFER = 1024
UTF = "utf-8"
RESPONSE_PACKET_ONE = 1
STUDENT_ID = "13319349"
allThreadsWorking = []
waiting_conns = []

def print_add(clientSocket, address):
	print ("Received connection!")
	data = (clientSocket.recv(BUFFER)).decode(UTF)
	whichPacket = handleInput(data)
	if whichPacket == RESPONSE_PACKET_ONE:
		response = "HELO text\nIP:[%s]\nPort:[%d]\nStudentID:[%s]\n" % (HOST, PORT, STUDENT_ID)
		clientSocket.sendall(response.encode())
	clientSocket.close()
	print ("Closed connection!")
	


def handleInput(data):
	if ("HELO text" in data):
		return RESPONSE_PACKET_ONE



def main():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((HOST, PORT))
	serversocket.listen(5)

	while 1:
		print ("Waiting for client connections...")
		#accept connections from outside
		print ("Current amount of working threads: %d" % (len(allThreadsWorking)))
		print ("Current amount of queued connections: %d" % (len(waiting_conns)))
		(clientsocket, address) = serversocket.accept()
		waiting_conns.append((clientsocket, address))

		

		if (len(allThreadsWorking) < MAX_AMOUNT): #can create a new thread
			connTuple = waiting_conns.pop()
			clsocket = connTuple[0]
			address = connTuple[1]

			thread = threading.Thread(target=print_add, args = (clsocket, address))
			allThreadsWorking.append(thread)
			print ("Current amount of working threads: %d" % (len(allThreadsWorking)))
			print ("Current amount of queued connections: %d" % (len(waiting_conns)))
			thread.start()
			allThreadsWorking.remove(thread)
			thread.join()
			
			print ("Current amount of working threads: %d" % (len(allThreadsWorking)))
			print ("Current amount of queued connections: %d" % (len(waiting_conns)))
		# ct = client_thread(clientsocket)
		# ct.run()

main()