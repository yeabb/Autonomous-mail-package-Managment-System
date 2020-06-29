import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8000))

while True:
    
    s.listen(5)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    inst= clientsocket.recv(1024).decode("utf-8")
    
    while True:
        if(inst=="1234"):
            clientsocket.send(bytes("1","utf-8"))
            print(clientsocket.recv(1024).decode("utf-8"))
            clientsocket.send(bytes("terminate","utf-8"))
            clientsocket.close()
            break
        if (inst=="7896"):
            clientsocket.send(bytes("2","utf-8"))
            print(clientsocket.recv(1024).decode("utf-8"))
            clientsocket.close()
            break
        else:
            clientsocket.send(bytes("wrong","utf-8"))
            inst= clientsocket.recv(1024).decode("utf-8")
            
            
        
