from cProfile import label
from tkinter import *
import socket
import threading

root = Tk()
root.title('amca chat app')
root.resizable(0,0)
root.geometry("320x568")        

# Yview Function
def multiple_yview(*args):
	my_text1.yview(*args)


# Frame
my_frame = Frame(root)
my_frame.place(x=0, y=0)

# Create our Scrollbar
text_scroll = Scrollbar(my_frame, command=multiple_yview)
# text_scroll.pack(side=LEFT, fill=Y)

# Create Two Text Boxes
my_text1 = Text(my_frame, width=25, height=20, font=("Helvetica", 16), yscrollcommand=text_scroll.set, wrap="none")
my_text1.pack(fill=BOTH, expand=True)


my_text2 = Text(my_frame, width=38, height=1,  wrap="none")
my_text2.pack(fill=BOTH, expand=True)

my_text3 = Text(my_frame, width=25, height=20, font=("Helvetica", 16), yscrollcommand=text_scroll.set, wrap="none")
my_text3.pack(fill=BOTH, expand=True)

def handler(e):
        message = '{}: {}'.format(nickname, my_text2.get("0.0",INSERT))
        CLIENT.send(message.encode('UTF-8'))
        my_text2.delete(0.0,END)
        my_text2.delete(0.0,END)

my_text2.bind('<Return>',handler)



nickname = input("Choose your nickname: ")
HOST = '10.123.13.57'
PORT = 8080
ADDR = (HOST, PORT)

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(ADDR)

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = CLIENT.recv(1024).decode('UTF-8')
            if message == 'NICK':
                CLIENT.send(nickname.encode('UTF-8'))
            elif 'NICKNAMES' in message:
                my_text3.delete(0.0,END)
                for word in message.replace("Connected to server!", "").replace("NICKNAMES", "").split(" "):
                    my_text3.insert(END, word + ", ")
            else:
                my_text1.insert(END,'\n' + message)
            my_text2.delete(1.0,END)
        except Exception as e:
            # Close Connection When Error
            print("An error occured!" + e)
            CLIENT.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()


root.mainloop()
