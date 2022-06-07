import socket
import threading

from tkinter import *
from tkinter.ttk import *

ws = Tk()
ws.title("Host Alma Ekranı")


HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
ADDR = (HOST, PORT)
print(HOST) # Alınan Host terminal ekranına kullanıcı için yazıldı.

# Label ile ekrana host değerinin verildiği uyarısı çıkar.
label1 = Label(ws, text = "Bağlanmak için Host adresiniz: ", font= ('Helvetica 16'), foreground="#1ba1e2")
label1.pack(pady= 20)

# Yazı giriş bölümünde Host değeri kullanıcıya verildi, kopyalayabilsin diye
entry1 = Entry(ws)
entry1.insert(END,HOST)
entry1.pack(expand = 1)

# Pencere çıkış Butonu
entry2 = Button(ws, text ="Çıkış", command=ws.destroy) # .destroy fonksiyonu pencereyi kapatır.
entry2.focus_set()
entry2.pack(pady = 5)


ws.mainloop()

# Server Başlatıyoruz...
# AF_INET IPv4 bağlantısı
# sock_stream tcp bağlantı tipi
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR) #Bağlama
SERVER.listen()

# Kullanıcılar ve onların Nickname leri için.
clients = []
nicknames = []


def broadcast(message, ip): # Çevrimici clientları her değişimde yenileyerek gösterilmesi için.
    nicknameStr = ""
    for nickname in nicknames:
        nicknameStr += nickname + " "
    for client in clients:
        client.send(message)
        client.send('NICKNAMES {}'.format(nicknameStr).encode('UTF-8'))


def handle(client): #
    while True:
        try:
            # Broadcasting Messages
            # recv, mesajın buffer size'ını ayarlar
            message = client.recv(1024)

            broadcast(message, client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast('{} left!'.format(nickname).encode('UTF-8'), client)
            break

# Mesajı alma / dinleme Fonksiyonu
def receive():
    while True:
        # Bağlantıyı kabul etme
        conn, addr = SERVER.accept()
        print(conn)
        print(addr)

        print("Connected with {}".format(str(addr)))
        print("here")

        # Request ve Store Nickname
        conn.send('NICK'.encode('UTF-8'))
        nickname = conn.recv(1024).decode('UTF-8')
        nicknames.append(nickname) # listeye yeni giriş yapan kişiyi nickname den çıkardı.
        clients.append(conn)

        # Print ve Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('UTF-8'), conn)
        conn.send('Connected to server!'.encode('UTF-8'))

        # Server ı dinlemeyi ve Server a yazmayı başlatma
        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()


receive()
