from django.shortcuts import render, redirect
from django.contrib import messages
import socket

# Create your views here.
def signup(request):
    return render(request,"signup.html")

def access(request):
    return render(request,"access.html")

def open_box(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        pin=request.POST["pin"]
        
        if(email=="ybiru@conncoll.edu"):

            

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.1.252", 8000))
            s.send(bytes("wassup","utf-8"))

            msg = s.recv(1024).decode("utf-8")


            return render(request, "after_access.html",{"msg":msg})
        else:
            messages.info(request,"invalid credentials")
            return render(request, "access.html")
    else:
        return render(request, "access.html")