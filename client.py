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
my_text1.pack(side="top", padx=5)


my_text2 = Text(my_frame, width=38, height=1,  wrap="none")
my_text2.pack(side="bottom", padx=2)

def handler(e):
        message = '{}: {}'.format(nickname, my_text2.get("1.0",INSERT))
        CLIENT.send(message.encode('UTF-8'))
        my_text2.delete(1.0,END)
        my_text2.delete(1.0,END)

my_text2.bind('<Return>',handler)



nickname = input("Choose your nickname: ")
HOST = '192.168.43.124'
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
            else:
                my_text1.insert(END,message+'\n')
        except:
            # Close Connection When Error
            print("An error occured!")
            CLIENT.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()


root.mainloop()
