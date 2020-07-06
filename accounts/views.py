from django.shortcuts import render, redirect
from django.contrib import messages
import socket
import qrcode
import smtplib
import ssl
import os
import imghdr
import random
from email.message import EmailMessage

code=None
# Create your views here.
def signup(request):
    return render(request,"signup.html")

def access(request):
    return render(request,"access.html")

def register(request):
    if (request.method=="POST"):
        firstName=request.POST["FirstName"]
        lastName=request.POST["LastName"]
        email=request.POST["Email"]
        tel=request.POST["Phone_Number"]


        
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

        code=random.randint(1,1000000)


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
                <h1 style="color:SlateGray;">Confirm your email address</h1>
                <p>
                    There’s a quick step you need to complete before creating your account. Please confirm this is the right address to use for your new account.
                </p>
                <br/>
                <p>
                    Please enter this verification code to get started on our plateform: <h1 style="color:SlateGray;">{code}</h1>
                </p>
                <p>
                    After you verify your email please take a screenshot of the QRCode attached below(you will need it)
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
        print("File Removed!")
        return render(request, "email_verification.html")
    else:
        return render(request, "signup.html")



def verify_email(request):
    if (request.method=="POST"):
        veri_code=request.POST["code"]
        if(veri_code==code):
            return render(request, "after_signup.html")
        else:
            messages.info(request,"Code didn't match, please try again")
            return render(request, "email_verification.html")


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