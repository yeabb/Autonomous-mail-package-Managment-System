import qrcode
import os

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


os.remove("qr.png") 	#to remove the QR image after it has been send through email
print("File Removed!")