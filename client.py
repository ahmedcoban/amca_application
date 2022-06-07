
from cProfile import label
from tkinter import *
import socket
import threading

ws = Tk()
ws.title("Host Giriş")

# global HOST
# HOST = '10.0.5.55'

label1 = Label(ws, text = "Bağlanmak için Host'u giriniz: ", font= ('Helvetica 16'), foreground="#1ba1e2")
label1.pack(pady= 20)

# Yazı giriş bölümünde Host değeri kullanıcıya verildi, kopyalayabilsin diye
entry1 = Entry(ws)
entry1.pack(expand = 1)

def butons():
    global HOST # Buradakini aldığımız yeni host değeriyle değiştirmeliyiz.
    HOST = (str)(entry1.get())
    ws.destroy()

# Pencere çıkış Butonu
button = Button(ws, text ="girdim", command=butons) # .destroy fonksiyonu pencereyi kapatır.
button.focus_set()
button.pack(pady = 5)



ws.mainloop()
print("Girdiğiniz Host: "+ HOST)




ws2 = Tk()
ws2.title("İsim alma")

label10 = Label(ws2, text = "    İsim Giriniz:    ", font= ('Helvetica 16'), foreground="#1ba1e2")
label10.pack(pady= 20)

entry10 = Entry(ws2)
entry10.pack(expand = 1)

def butons2():
    global nickname # İsim
    nickname = (str)(entry10.get())
    ws2.destroy()

# Pencere çıkış Butonu
button10 = Button(ws2, text ="girdim", command=butons2) # .destroy fonksiyonu pencereyi kapatır.
button10.focus_set()
button10.pack(pady = 5)


ws2.mainloop()
print("Girdiğiniz isim: "+ nickname)



root = Tk() # pencereyi tkinter kullanarak oluşturma
root.title('amca chat app') # pencerenin adı
root.resizable(0,0) # kullanıcının pencereyi yeniden boyutlandırmasını engellemek için yükseklik ve genişlik 0,0 verildi.
root.geometry("320x568") # pencerenin ebatları

# Yview için fonksiyon
def multiple_yview(*args): # kaydırma çubuğuna 2 widgeti de birden bağlamak için yazılan bir fonksiyon.
    my_text1.yview(*args) # burada sadece text1 bunun için ayarlanmış. (xview de olabilir).

count = 0

# Frame oluşturduk.
my_frame = Frame(root)
my_frame.place(x=0, y=0)

# Scrollbar oluşturduk.
text_scroll = Scrollbar(my_frame, command=multiple_yview) # tek bir kaydırma çubuğu ile iki widgetı da kaydırmak için.
text_scroll.pack(side=RIGHT, fill=Y,  expand=True)

# Create Two Text Boxes
my_text1 = Text(my_frame, width=25, height=20, font=("Helvetica", 16), bg="#a4c400", yscrollcommand=text_scroll.set, wrap="none")
my_text1.pack(fill=BOTH, expand=True) # Yazışmanın bulunduğu text

my_text2 = Text(my_frame, width=38, height=1,  wrap="none")
my_text2.pack(fill=BOTH, expand=True) # Gönderilecek iletinin pencerede girildiği text yeri

my_text3 = Text(my_frame, width=25, height=20, font=("Helvetica", 16), bg="#1ba1e2", yscrollcommand=text_scroll.set, wrap="none")
my_text3.pack(fill=BOTH, expand=True) # Aktif kullanıcıların bulunduğu yer

def handler(e):
        # Text 2 deki iletilecek ifade ileten kişinin nick adıyla iletilir.
        message = '{}: {}'.format(nickname, my_text2.get("0.0",INSERT))
        CLIENT.send(message.encode('UTF-8'))
        my_text2.delete(0.0,END) # Yazı gittikten sonra text in içi boşaltılır.
        my_text2.delete(0.0,END)

my_text2.bind('<Return>',handler) # Text 2 yerinden gönderim için işlemi Enter tuşuna bağlamak için.



# nickname = input("Choose your nickname: ")

PORT = 8080
ADDR = (HOST, PORT)

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(ADDR)

# Server ı dinleme ve nickname gönderme
def receive():
    while True:
        try:
            # Server dan mesaj almak
            # Eğer mesaj NICK ise
            message = CLIENT.recv(1024).decode('UTF-8')
            if message == 'NICK':
                CLIENT.send(nickname.encode('UTF-8'))
            # Eğer mesajda nicknames var ise
            elif 'NICKNAMES' in message:
                my_text3.config(state=NORMAL)
                my_text3.delete(0.0, END)
                # Çevrimici kullanıcıları gösterir
                for word in message.replace("Connected to server!", "").replace("NICKNAMES", "").split(" "):
                    my_text3.insert(END, word + " ")
                my_text3.config(state=DISABLED)
                # my_text3.insert(END, " joined, ")
            else:
                my_text1.insert(END,'\n' + message)
            my_text2.delete(1.0,END)
        except Exception as e:
            # Hata verdiğinde bağlantı sonlandırılır
            print("An error occured!" + e)
            CLIENT.close()
            break

# Server ı dinlemeyi ve Server a yazmayı başlatma
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Uygulama başlatılır.
root.mainloop()
