from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import socket
import qrcode
import smtplib
import ssl
import os
import imghdr
import random
from email.message import EmailMessage
from .models import *
from .presence import Presence
# Create your views here.
  


def signupForm(request):
    return render(request,"signupForm.html")




def contact_email(request):
    if (request.method=="POST"):
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        


        
        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=5
        )

        data = str(email)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        imgName=str(email)+".jpg"
        img.save(imgName)

        
        
        code=random.randint(0,1000000)
        


        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


        msg = EmailMessage()
        msg['Subject'] = "Verification code"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = str(email)

        #msg.set_content('your code is'+" "+str(code))

        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body style="display:block">
                <h1 style="color:SlateGray;">Confirm your email address and screenshot the QRCode</h1>
                <p>
                    There’s a quick step you need to complete before creating your account. Please confirm this is the right address to use for your new account.
                </p>
                <br/>
                <p>
                    Please enter this verification code to get started and take a screenshot of the QRCode attached below(you will need it):
                     <h1 style="color:SlateGray;">{code}</h1>
                    
                </p>
                
            </body>
        </html>
        """.format(**locals()), subtype='html')

        with open(imgName, "rb") as f:
            file_data= f.read()
            file_name=f.name
            file_type=imghdr.what(file_name)
        

        msg.add_attachment(file_data, maintype="image", subtype="file_type", filename=file_name)


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        #save the name,email and code into tempo data base


        os.remove(imgName) 	#to remove the QR image after it has been send through email
        print("File Removed!")
        return render(request, "email_verification.html",{"email":email})
    else:
        return render(request, "signup.html")



def verify_email(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        veri_code=request.POST["veri_code"]
       
        #open the tempo data base and access email and code
        
        # if(veri_code==code):
        return render(request, "finishup_registration.html",{"email":email})
        # else:
        #     messages.info(request,"Code didn't match, please try again")
        #     return render(request, "email_verification.html")




def email_reprompt(request):
    if (request.method=="POST"):
        email=request.POST["email_val"]
        return render(request, "email_reprompt.html",{"email":email})





def sendEmailAgain(request):
    if (request.method=="POST"):
        email=request.POST["confirm_email"]
    
        qr=qrcode.QRCode(
                version=1,
                box_size=15,
                border=5
        )

        
        data = str(email)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        imgName=str(email)+".jpg"
        img.save(imgName)

        
        
        code=random.randint(0,1000000)
        


        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


        msg = EmailMessage()
        msg['Subject'] = "Verification code"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = str(email)

        #msg.set_content('your code is'+" "+str(code))

        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body style="display:block">
                <h1 style="color:SlateGray;">Confirm your email address and screenshot the QRCode</h1>
                <p>
                    There’s a quick step you need to complete before creating your account. Please confirm this is the right address to use for your new account.
                </p>
                <br/>
                <p>
                    Please enter this verification code to get started and take a screenshot of the QRCode attached below(you will need it):
                        <h1 style="color:SlateGray;">{code}</h1>
                    
                </p>
                
            </body>
        </html>
        """.format(**locals()), subtype='html')

        with open(imgName, "rb") as f:
            file_data= f.read()
            file_name=f.name
            file_type=imghdr.what(file_name)
        

        msg.add_attachment(file_data, maintype="image", subtype="file_type", filename=file_name)


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        os.remove(imgName) 	#to remove the QR image after it has been send through email
        return render(request, "email_verification.html",{"email":email})






def finishup_registration(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        #agree_term=request.POST["agree_term"]


        #access the tempo database and fetch the first and lastname 

        #save each of the user info to the main user table




def login(request):
    return render(request,"login.html")





def personalAccount(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        password=request.POST["password"]
        if (email=="mekonnentadesse999@gmail.com"):
            presence=Presence()
            presence.val=True
            return render(request,"after_login.html",{"presence":presence})




def open_box(request):
    if (request.method=="POST"):
        email=request.POST["Email"]
        pin=request.POST["pin"]
        
        if(email=="ybiru@conncoll.edu"):

            

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.1.252", 8000))
            s.send(bytes("wassup","utf-8"))

            msg = s.recv(1024).decode("utf-8")


            return render(request, "after_access.html",{"msg":msg})
        else:
            messages.info(request,"invalid credentials! Please double-check and try again.")
            return render(request, "access.html")
    else:
        return render(request, "access.html")






    






