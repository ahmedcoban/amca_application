import tkinter as tk
from tkinter import *

master=tk.Tk()
master.title("Amca")
tk.Canvas(master, height=600, width=1000, bg="#2f4f4f").pack()
sol_frame=tk.Frame(bg="black")
sol_frame.place(x=0, y=0, width=800, height=600)
sag_frame=tk.Frame(bg="red")
sag_frame.place(x=800, y=0, width=200, height=600)
mesaj=tk.Entry(sol_frame)
mesaj.place(x=0, y=0, width=800, height=350)
mesaj2=tk.Entry(sol_frame, state=DISABLED)
mesaj2.place(x=0, y=355, width=800, height=245)

def handler(e):
    mesaj2.config(state=NORMAL)
    mesaj2.delete(0, END)
    mesaj2.insert(0, str(mesaj.get()))
    mesaj2.config(state=DISABLED)

mesaj.bind('<Return>',handler)
master.mainloop()

#amro
