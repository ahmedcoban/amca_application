import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (HOST, PORT)
print(HOST)

# Starting Server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

def broadcast(message,ip):
    for client in clients:
        if client == ip :
            pass
        else:
            client.send(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message,client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('UTF-8'),client)
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        conn, addr = SERVER.accept()
        print(conn)
        print(addr)

        
        print("Connected with {}".format(str(addr)))
        print("here")
        

        # Request And Store Nickname
        conn.send('NICK'.encode('UTF-8'))
        nickname = conn.recv(1024).decode('UTF-8')
        nicknames.append(nickname)
        clients.append(conn)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('UTF-8'),conn)
        conn.send('Connected to server!'.encode('UTF-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()


receive()