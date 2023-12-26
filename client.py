# import required modules
import socket
import threading
import tkinter as tk
import datetime
import pickle
import os
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

messages_list = []
messages_have_keyword = []

def get_current_time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def add_message(message):
    current_time = get_current_time()
    formatted_message = f"[{current_time}] {message}"
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, formatted_message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():

    # try except block
    try:

        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        messages_list.append(message)
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")
        
def send_message():
    message = message_textbox.get()
    if message != '':
        messages_list.append(message)
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")
        
def search_strings(arr, small_string):
    results = []
    for string in arr:
        if small_string in string:
            results.append(string)
    return results

def enter_keyword():
    keyword = keyword_textbox.get()
    if keyword != '':
        search_keyword = search_strings(messages_list, keyword)
        keyword_box.config(state=tk.NORMAL)
        keyword_box.delete(1.0, tk.END)  # Clear previous results
        if search_keyword:
            for result in search_keyword:
                keyword_box.insert(tk.END, result + '\n')
        else:
            keyword_box.insert(tk.END, "No matching messages found.\n")
            keyword_box.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Empty keyword", "Keyword cannot be empty")

def send_search_request():
    threading.Thread(target=enter_keyword).start()


def save_messages_to_file():
    current_time = get_current_time().replace(" ", "_").replace(":", "-")
    filename = f"messages_{current_time}.dat"
    
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, filename)
    
    messagebox.showinfo("Save Messages", f"Messages saved to {full_path}")
  
    
        
   

# Sử dụng hàm search_keyword_in_messages khi cần tìm kiếm từ khoá
root = tk.Tk()
root.geometry("1000x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=6)


lefttop_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
lefttop_frame.grid(row=0, column=0, sticky=tk.NSEW)

leftmiddle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
leftmiddle_frame.grid(row=1, column=0, sticky=tk.NSEW)

leftbottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
leftbottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# Frame bên phải
righttop_frame = tk.Frame(root, width=400, height=100, bg=OCEAN_BLUE    )
righttop_frame.grid(row=0, column=0, sticky=tk.NSEW)

rightmiddle_frame= tk.Frame(root, width=400, height=400, bg=DARK_GREY)
rightmiddle_frame.grid(row=1, column=0,sticky=tk.NSEW)


rightbottom_frame= tk.Frame(root, width=400, height=100, bg=DARK_GREY)
rightbottom_frame.grid(row=2, column=0, sticky=tk.NSEW)


# Widget cho ô nhập tin nhắn và nút gửi
lefttop_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
lefttop_frame.grid(row=0, column=0, sticky=tk.NSEW)

leftmiddle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
leftmiddle_frame.grid(row=1, column=0, sticky=tk.NSEW)

leftbottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
leftbottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(lefttop_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT)

username_textbox = tk.Entry(lefttop_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(lefttop_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(leftbottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(leftbottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(leftmiddle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)

message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

save_button = tk.Button(leftbottom_frame, text="Save", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=save_messages_to_file)
save_button.pack(side=tk.LEFT, padx=10)


# Widget cho ô nhập từ khoá
righttop_frame = tk.Frame(root, width=400, height=100, bg=MEDIUM_GREY)
righttop_frame.grid(row=0, column=1, sticky=tk.NSEW)

rightmiddle_frame = tk.Frame(root, width=400, height=400, bg=DARK_GREY)
rightmiddle_frame.grid(row=1, column=1, sticky=tk.NSEW)

rightbottom_frame = tk.Frame(root, width=400, height=100, bg=MEDIUM_GREY)
rightbottom_frame.grid(row=2, column=1, sticky=tk.NSEW)

keyword_label = tk.Label(righttop_frame, text="Messages have keyword", font=FONT, bg=MEDIUM_GREY, fg=WHITE)
keyword_label.pack(padx=80, side=tk.LEFT)

username_label = tk.Label(rightbottom_frame, text="Keyword:", font=FONT, bg=MEDIUM_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT)

keyword_textbox = tk.Entry(rightbottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=15)
keyword_textbox.pack(side=tk.LEFT, padx=10)

keyword_button = tk.Button(rightbottom_frame, text="Search", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_search_request)
keyword_button.pack(side=tk.LEFT, padx=10)

keyword_box = scrolledtext.ScrolledText(rightmiddle_frame, font=SMALL_FONT, bg=DARK_GREY, fg=WHITE, width=67, height=26.5)
keyword_box.config(state=tk.DISABLED)
keyword_box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
 
            
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")


# main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
