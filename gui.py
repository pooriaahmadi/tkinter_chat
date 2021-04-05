import tkinter as tk
import tkinter.font as tkFont
import socket
import pickle
from threading import Thread

SERVER_HOST = '87.107.172.12'
SERVER_PORT = 15013
HEADER_SIZE = 10

def decode(data, format='utf-8'):
    return data.decode(format)

def encode(data, format='utf-8'):
    return data.encode(format)

def create_header(data, decode=False):
    data = f"{len(data):<{HEADER_SIZE}}"
    if decode:
        data = decode(data)
    return data

def get_length(message_header):
    return int(message_header)

class App:
    def __init__(self, root):
        #setting title
        root.title("Developers Chat")
        #setting window size
        width=600
        height=500

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        scrollbar = tk.Scrollbar(root)

        GLabel_595=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        GLabel_595["font"] = ft
        GLabel_595["fg"] = "#333333"
        GLabel_595["justify"] = "center"
        GLabel_595["text"] = "Developers Chat"
        GLabel_595.place(x=0,y=0,width=599,height=51)

        GLineEdit_371=tk.Entry(root)
        GLineEdit_371["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_371["font"] = ft
        GLineEdit_371["fg"] = "#333333"
        GLineEdit_371["justify"] = "center"
        GLineEdit_371["text"] = "Entry"
        GLineEdit_371.place(x=10,y=450,width=511,height=43)
        self.entry = GLineEdit_371

        GButton_779=tk.Button(root)
        GButton_779["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_779["font"] = ft
        GButton_779["fg"] = "#000000"
        GButton_779["justify"] = "center"
        GButton_779["text"] = "Send"
        GButton_779.place(x=530,y=450,width=60,height=44)
        GButton_779["command"] = self.GButton_779_command

        GMessage_2=tk.Text(root, yscrollcommand=scrollbar.set)
        GMessage_2["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GMessage_2['background'] = "white"
        GMessage_2["font"] = ft
        GMessage_2["fg"] = "#333333"
        GMessage_2.insert("end",f"Connected to server!")
        GMessage_2.place(x=10,y=40,width=560,height=380)
        GMessage_2.config(state='disabled')
        self.GMessage_2 = GMessage_2

        scrollbar.config(command=GMessage_2.yview)
        scrollbar.place(x=575, y=40, width=20, height=380)
    def GButton_779_command(self):
        message = self.entry.get()
        client_socket.send(encode(f"{create_header(message)}{message}"))

def incomming_messages(app):
    while True:
        message_header = client_socket.recv(HEADER_SIZE)
        if len(message_header):
            message = client_socket.recv(get_length(decode(message_header)))
            user = pickle.loads(message)
            app.GMessage_2.config(state='normal')
            app.GMessage_2.insert("end",f"\n{user['username']} > {user['message']}")
            app.GMessage_2.see("end")
            app.GMessage_2.config(state='disabled')


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    username = input('Please enter your username: ')
    client_socket.send(encode(f"{create_header(username)}{username}"))
    root = tk.Tk()
    app = App(root)
    Thread(target=incomming_messages, args=(app,)).start()
    root.mainloop()
