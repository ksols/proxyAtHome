import socket
import sys
from _thread import *


listening_port = 3000
max_connection = 5
buffer_size = 8192 # Seems to be default size

def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', listening_port))
        sock.listen(max_connection)
        print(f"--------- Server started successfully on port: {listening_port} ---------")
    except Exception:
        print("Unable to Initialize Socket")
        print("Exception: ", Exception)
        sys.exit(2)

    while True:
        try:
            conn, addr = sock.accept() #no need for addr when conn is esablished
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn,data))
        except KeyboardInterrupt:
            sock.close()
            print("\n Stopping...")
            sys.exit(1)

def conn_string(conn, data): # creates the parameters webserver and port and runs proxy_server with them
    try:
        first_line = data.split(b'\n')[0]
        url = first_line.split()[1]
        http_pos = url.find(b'://')
        if(http_pos==-1):
            temp=url
        else:
            temp = url[(http_pos+3):]
        
        port_pos = temp.find(b':')
        
        webserver_pos = temp.find(b'/')
        
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]
        proxy_server(webserver, port, conn, data)
    except Exception:
        pass

def proxy_server(webserver, port, conn, data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((webserver, port))
        print(f"Connected to server: {webserver}:{(port)} \n From {conn}")
        sock.send(data)
        print("Forward: ", data)
        while 1:
            reply = sock.recv(buffer_size)
            if(len(reply)>0):
                conn.send(reply)
            else:
                break

        sock.close()

        conn.close()
    except socket.error:
        sock.close()
        conn.close()
        print("-------------------- sock.error: --------------------")
        print(sock.error)
        print("------------------------------------------------------------")
        sys.exit(1)

if __name__== "__main__":
    start()