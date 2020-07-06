import qrcode
import smtplib
import ssl
import os
import imghdr
from email.message import EmailMessage

qr = qrcode.QRCode(
	version=1,
	box_size=15,
	border=5
)

data = 'yeabkal'
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save('qr.png')


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

#contacts = ['YourAddress@gmail.com', 'test@example.com']

msg = EmailMessage()
msg['Subject'] = "Verification code"
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'mekonnentadesse999@gmail.com'

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:SlateGray;">This is an HTML Email!</h1>
    </body>
</html>
""", subtype='html')


with open("qr.png", "rb") as f:
	file_data= f.read()
	file_name=f.name
	file_type=imghdr.what(file_name)
	

msg.add_attachment(file_data, maintype="image", subtype="file_type", filename=file_name)




with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)








os.remove("qr.png") 	#to remove the QR image after it has been send through email
print("File Removed!")