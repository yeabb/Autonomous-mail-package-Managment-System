import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8000))

while True:
    
    s.listen(5)
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    pre_cred= clientsocket.recv(1024).decode("utf-8")
    

    
    while True:
        if(pre_cred=="termiante connection"):
            clientsocket.close()
            break
        else:
            credentials=pre_cred.split(",")
            email=credentials[0]
            password=credentials[1]
            if(User.objects.filter(email=email).exists()):

                user=User.objects.filter(email=email).first()
            
            
                if(password==user.password):
                   
                    if(Parcel.objects.filter(email=email).exists()):
                        parcel=Parcel.objects.filter(email=email).first()
                        clientsocket.send(bytes(parcel.box_num,"utf-8"))
                        print(clientsocket.recv(1024).decode("utf-8"))
                        clientsocket.send(bytes("terminate","utf-8"))
                        clientsocket.close()
                        parcel.delete()
                        break
                    else:
                        clientsocket.send(bytes("parcel not present","utf-8"))
                        print(clientsocket.recv(1024).decode("utf-8"))
                        clientsocket.close()
                        break
                else:
                    clientsocket.send(bytes("password is wrong","utf-8"))
                    pre_cred= clientsocket.recv(1024).decode("utf-8")
                
            else:    
                clientsocket.send(bytes("email could not be found","utf-8"))
                pre_cred= clientsocket.recv(1024).decode("utf-8")
