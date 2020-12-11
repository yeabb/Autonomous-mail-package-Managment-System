from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
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
import datetime 
import pytz
# Create your views here.
  


def signupForm(request):
    return render(request,"signupForm.html")




def contact_email(request):
    if (request.method=="POST"):
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        username=request.POST["username"]
        decide=Presence()
        
        if(User.objects.filter(email=email).exists()):
            # parcel=Parcel.objects.filter(email=email).first()
            # parcel.delete()
            # for i in range(1,9):
            # box=BoxList.objects.filter(available=False).first()
            # box.associated_customer=None
            # box.available=True
            # box.save()

            # for i in range(1,9):
            #     # initiation_time=datetime.datetime.now(tz=pytz.UTC)
            #     box=BoxList(box_num=i)
            #     box.save()
            
            # x=False
            # box=BoxList.objects.filter(box_num=1).first()
            # box.delete()

            decide.dec=True
            messages.info(request,"email already taken! Please try again!")
            return render(request, "signupForm2.html",{"username":username, "first_name":first_name, "last_name":last_name,"decide":decide})
        elif(User.objects.filter(username=username).exists()):
            decide.dec=False
            messages.info(request,"username already taken! Please try again!")
            return render(request, "signupForm2.html",{"email":email, "username":username, "first_name":first_name, "last_name":last_name, "decide":decide})
        else:
            code=random.randint(0,1000000)
            if(BeforeEmailVerification.objects.filter(email=email).exists()):
                tempo_db=BeforeEmailVerification.objects.filter(email=email).first()
                initiation_time=datetime.datetime.now(tz=pytz.UTC)
                tdelta=datetime.timedelta(hours=2)
                expire_time=initiation_time+tdelta
                
                tempo_db.first_name=first_name
                tempo_db.last_name=last_name
                tempo_db.username=username
                tempo_db.code=code
                tempo_db.initiation_time=initiation_time
                tempo_db.expire_time=expire_time
                tempo_db.save() #save the code, initiation_time and expire-time into tempo data base
            else:
                initiation_time=datetime.datetime.now(tz=pytz.UTC)
                tdelta=datetime.timedelta(hours=2)
                expire_time=initiation_time+tdelta
                tempo_db=BeforeEmailVerification(first_name=first_name, last_name=last_name, username=username, email=email, code=code, initiation_time=initiation_time, expire_time=expire_time)
                tempo_db.save() #save the name, email, code, initiation_time and expire-time into tempo data base
            
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
            print("File Removed!")
            return render(request, "email_verification.html",{"email":email})
    else:
        return render(request, "signupForm.html")



def verify_email(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        veri_code=int(request.POST["veri_code"])
       
        #open the tempo data base and access email and code
        tempo_db=BeforeEmailVerification.objects.filter(email=email).first()
        code=int(tempo_db.code)
        
        
        expire_time=tempo_db.expire_time
        current_time=datetime.datetime.now(tz=pytz.UTC)
        
        
        if(veri_code==code):
            if(current_time<=expire_time):
                return render(request, "finishup_registration.html",{"email":email})
            elif(current_time>expire_time):
                tempo_db.delete()   #delete the user from here
                messages.info(request,"Code has expired! please start again from here! ")
                return render(request, "signupForm.html")
        
        else:
            messages.info(request,"Code didn't match, please try again")
            return render(request, "email_verification.html",{"email":email})
        
        
def email_reprompt(request):
    if (request.method=="POST"):
        email=request.POST["email_val"]
        return render(request, "email_reprompt.html",{"email":email})





def sendEmailAgain(request):
    if (request.method=="POST"):
        email=request.POST["confirm_email"]
        email_prev=request.POST["email_prev"]

        
        
        if(User.objects.filter(email=email).exists()):
            messages.info(request,"email adress already taken!")
            return render(request, "email_reprompt.html")

        else:
            code=random.randint(0,1000000)
            if (email_prev==email):
                if(BeforeEmailVerification.objects.filter(email=email).exists()):
                    tempo_db=BeforeEmailVerification.objects.filter(email=email).first()
                    initiation_time=datetime.datetime.now(tz=pytz.UTC)
                    tdelta=datetime.timedelta(hours=2)
                    expire_time=initiation_time+tdelta
                    
                    
                    tempo_db.code=code
                    tempo_db.initiation_time=initiation_time
                    tempo_db.expire_time=expire_time
                    tempo_db.save() #save the code, initiation_time and expire-time into tempo data base
                else:
                    initiation_time=datetime.datetime.now(tz=pytz.UTC)
                    tdelta=datetime.timedelta(hours=2)
                    expire_time=initiation_time+tdelta
                    tempo_db=BeforeEmailVerification(first_name=first_name, last_name=last_name, email=email, code=code, initiation_time=initiation_time, expire_time=expire_time)
                    tempo_db.save() #save the name, email, code, initiation_time and expire-time into tempo data base
            else:
                tempo_db=BeforeEmailVerification.objects.filter(email=email_prev).first()
                initiation_time=datetime.datetime.now(tz=pytz.UTC)
                tdelta=datetime.timedelta(hours=2)
                expire_time=initiation_time+tdelta
                
                tempo_db.email=email
                tempo_db.code=code
                tempo_db.initiation_time=initiation_time
                tempo_db.expire_time=expire_time
                tempo_db.save() #save the code, initiation_time and expire-time into tempo data base
        
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
    else:
        return render(request,"signupForm.html")





def finishup_registration(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        
        checked=request.POST.get("agree_term", False)


        
        if(password1==password2):
            if(checked):
                #access the tempo database and fetch the first and lastname
                tempo_db=BeforeEmailVerification.objects.filter(email=email).first()
                first_name=tempo_db.first_name
                last_name=tempo_db.last_name
                username=tempo_db.username
                user=User.objects.create_user(first_name=first_name, username=username, last_name=last_name, email=email, password=password1)
                user.save()
                tempo_db.delete()
                
                return render(request,"login.html")
            else:
                messages.info(request,"You need to check box if you wish to proceed")
                return render(request, "finishup_registration.html",{"email":email})
        else:
            messages.info(request,"Password didn't match")
            return render(request, "finishup_registration.html",{"email":email})
        
       
        
        


def login(request):
    return render(request,"login.html")





def personalAccount(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        password=request.POST["password"]
        if (User.objects.filter(email=email).exists()):
            customer=User.objects.filter(email=email).first()
            username=customer.username
            user=auth.authenticate(username=username,password=password)
            presence=Presence()
            if user is not None:
                if(customer.is_staff):
                    auth.login(request, user)
                    if(Parcel.objects.filter(email=email).exists()):
                        presence.val=True
                    else:
                        presence.val=False
                    return render(request,"after_login_staff.html",{"presence":presence, "email":email})
                else:
                    auth.login(request, user)
                    if(Parcel.objects.filter(email=email).exists()):
                        presence.val=True
                    else:
                        presence.val=False
                    return render(request,"after_login.html",{"presence":presence, "email":email})
            else:
                messages.info(request,"Wrong Password! Please try again")   
                return render(request,"login.html")
            
            
        else:
            messages.info(request,"User could not be found! Please try again") 
            return render(request,"login.html")


def addPackage(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        client_email=request.POST["client_email"]
        pres=request.POST["presence"]
        presence=Presence()
        presence.val=pres
        if(User.objects.filter(email=client_email).exists()):
            if(Parcel.objects.filter(email=client_email).exists()):
                parcel=Parcel.objects.filter(email=client_email).first()
                if(BoxList.objects.filter(available=True).exists()):
                    boxList=BoxList.objects.filter(available=True).first()
                    boxNum=boxList.box_num    #get the first box number that is free
                    
                    #open the box to enter the package and wait untill it's closed 
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("136.244.194.178", 8000))
                    s.send(bytes(str(boxNum),"utf-8"))
                    msg = s.recv(1024).decode("utf-8")
                                                                         
                    #192.168.1.194
                    totalBoxNum=parcel.box_num+","+str(boxNum)
                    parcel.box_num=totalBoxNum      #add the new box number into the parcel table
                    parcel.save()       #save the newly added box number

                    initiation_time=datetime.datetime.now(tz=pytz.UTC)

                    boxList.available=False
                    boxList.associated_customer=client_email
                    boxList.filledTime=initiation_time
                    boxList.save()          #save the newly updated BoxList object
                    
                    
                    ##email the client
                    data = str(client_email)

                    
                    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
                    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


                    msg = EmailMessage()
                    msg['Subject'] = "Verification code"
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = str(client_email)


                    msg.add_alternative("""\
                    <!DOCTYPE html>
                    <html>
                        <body style="display:block">
                            <h1 style="color:SlateGray;">You have new package in your box</h1>
                            <p>
                                your new package have arrived safely and we have placed it into you box, you can come and fetch it at anytime that works for you.
                            </p>
                            <br/>
                            <p>
                                please note that you already have another package in one of our boxes and you dont need a new access code to retrieve this new package. as soon as you enter the previous access code you will gain access to all of your packages at the same time.
                            </p>
                            
                        </body>
                    </html>
                    """.format(**locals()), subtype='html')

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)



                    messages.info(request,"package was succesfully placed to"+" "+str(client_email))
                    return render(request, "after_login_staff.html",{"email":email, "presence":presence})
                else:
                    messages.info(request,"All of the boxes are taken at the moment. Please try again!"+" "+str(client_email))
                    return render(request, "after_login_staff.html",{"email":email, "presence":presence})
            else:
                if(BoxList.objects.filter(available=True).exists()):
                    boxList=BoxList.objects.filter(available=True).first()
                    boxNum=boxList.box_num    #get the box number that is free
                    
                    #open the box to enter the package and wait untill it's closed 
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("136.244.194.178", 8000))
                    s.send(bytes(str(boxNum),"utf-8"))
                    msg = s.recv(1024).decode("utf-8")

                    #create a new row in the parcel table

                    access_code=random.randint(0,1000000)
                    initiation_time=datetime.datetime.now(tz=pytz.UTC)
                    parcel=Parcel(email=client_email, box_num=boxNum, access_code=access_code, entrance_time=initiation_time)  #create a new row in the parcel table
                    parcel.save()

                    boxList.available=False
                    boxList.associated_customer=client_email
                    boxList.filledTime=initiation_time
                    boxList.save()
                    
                    ##email the client and provide access code
                    data = str(client_email)

                    
                    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
                    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


                    msg = EmailMessage()
                    msg['Subject'] = "Verification code"
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = str(client_email)


                    msg.add_alternative("""\
                    <!DOCTYPE html>
                    <html>
                        <body style="display:block">
                            <h1 style="color:SlateGray;">You have new package in your box</h1>
                            <p>
                                Your new package have arrived safely and we have placed it into your box, you can come and fetch it at anytime that works for you.
                            </p>
                            <br/>
                            <p>
                                Please enter this Access code to gain acess to your package:
                                    <h1 style="color:SlateGray;">{access_code}</h1>
                               
                            </p>
                            
                        </body>
                    </html>
                    """.format(**locals()), subtype='html')


                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)


                    
                    messages.info(request,"package succesfully placed to"+" "+str(client_email))
                    return render(request, "after_login_staff.html",{"presence":presence})
                else:
                    messages.info(request,"All of the boxes are taken at the moment. Please try again!"+" "+str(client_email))
                    return render(request, "after_login_staff.html",{"email":email, "presence":presence})
       
        else:
            messages.info(request,str(client_email)+" "+"could not be found")
            return render(request, "after_login_staff.html",{"presence":presence})




def staffBoxAccess(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        pres=request.POST["presence"]
        presence=Presence()
        presence.val=pres
        return render(request,"after_login.html",{"email":email, "presence":presence})


def open_box(request):
    if (request.method=="POST"):
        email=request.POST["email"]
        pin=request.POST["pin"]
        
        parcel=Parcel.objects.filter(email=email).first()
        if(int(parcel.access_code)==int(pin)):
            box_num=parcel.box_num

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("136.244.194.178", 8000))
            s.send(bytes(box_num,"utf-8"))

            
            num = s.recv(1024).decode("utf-8")
            box_num_list=num.split(",")
            
           

            for i in(0,len(box_num_list)-2):
                boxList=BoxList.objects.filter(box_num=int(box_num_list[i])).first()
                boxList.available=True
                boxList.associated_customer=None
                boxList.filledTime=None
                boxList.save()

            parcel.delete()
            
            messages.info(request,"Box was succesfully opened.")
            return render(request, "after_access.html",{"num":num})

        else:
            messages.info(request,"invalid credentials! Please enw-check and try again.")
            return render(request, "after_login.html",{"email":email})
    else:
        return render(request, "after_login.html",{"email":email})




    






