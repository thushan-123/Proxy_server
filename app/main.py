import socket
import signal
import threading

def handle_client_request(client_socket):
    print("Recived request:\n")
    
    request = b""
    client_socket.setblocking(False)
    
    while True:
        try:
            # recive data from webserver
            data = client_socket.recv(1024)
            
            request = request + data
            
            
            print(f"{data.decode("utf-8")}")
        except:
            break
        
    # get the webserver host and port
    host, port = extract_host_port_from_request(request)
    
    # create socket connection destination server
    
    destination_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    destination_socket.connect((host,port))  # connect to destination server
    
    destination_socket.sendall(request)
    
    print("Recived Response \n")
    
    while True:
        
        data = destination_socket.recv(1024)
        print(f"{data.decode("utf-8")}")
        
        # no data to send
        if len(data) > 0:
            client_socket.sendall(data)
        else: 
            break
    
    destination_socket.close()
    client_socket.close()
    
        
    
def extract_host_port_from_request(request):
    host_name_start = request.find(b"Host: ") + len(b"Host: ")
    host_name_end = request.find(b"\r\n", host_name_start)
    
    host = request[host_name_start:host_name_end].decode("utf-8")
    
    webserver_position = host.find("/")
    
    if webserver_position == -1:
        webserver_position = len(host)
        
    port_position = host.find(":")     # check if there is specific port
    
    if port_position == -1 or webserver_position < port_position:    # not given specific port set default 80
        
        port = 80
    
        host_ = host[:webserver_position]
    else:
        # get the specific port from the string
        port = int((host[(port_position+1):])[:webserver_position - port_position -1])
        host_ = host[:port_position]
    return host_, port
    
    


def main():
    PORT = 8080
    
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",PORT))
    server.listen()
    
    print(f"Proxy SERVER Listening on Port {PORT}")
    
    while True:
        client_socket, addr = server.accept()
        
        print(f"Client Accept Connection From {addr[0]} - {addr[1]}")
        

        client_handle = threading.Thread(target=handle_client_request,  args=(client_socket,))
        client_handle.start()
        
        
    
if __name__ == "__main__":
    main()
