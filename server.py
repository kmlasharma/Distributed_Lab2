import _thread
import time
import socket
import threading

PORT = 8000
HOST = "localhost"
BUFFER = 1024
UTF = "utf-8"
RESPONSE_PACKET_ONE = 1
STUDENT_ID = "13319349"
pool = []

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
	while True:
		serversocket.listen(5)
		print ("Waiting for client connections...")
		#accept connections from outside
		(clientsocket, address) = serversocket.accept()
		thread = threading.Thread(target=print_add, args = (clientsocket, address))
		# client socket = <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 58745)>
		# address = ('127.0.0.1', 58745)
		thread.start()
		# ct = client_thread(clientsocket)
		# ct.run()

main()