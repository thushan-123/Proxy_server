import socket
import signal
import threading

def main():
    PORT = 8080
    
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",PORT))
    server.listen()
    
    print(f"Proxy SERVER Listening on Port {PORT}")
    
    while True:
        client_socket, addr = server.accept()
        
        print(f"Client Accept Connection From {addr[0]} - {addr[1]}")
        
        
    
if __name__ == "__main__":
    main()
