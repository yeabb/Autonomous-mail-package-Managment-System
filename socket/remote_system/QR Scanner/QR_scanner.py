import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

while True:
    x=eval(input("put 1 here: "))
    if(x==1):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(3,640)
        cap.set(4,480)
     
        num=0
        myData=0
        tempo=None
        track=0
        while True:
            
            success, img = cap.read()
            for barcode in decode(img):
                if(num>=2):
                    tempo=myData
                myData= barcode.data.decode('utf-8')
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(255,0,255),5)
                pts2 = barcode.rect
                cv2.putText(img,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,(255,0,255),2)

                cv2.imshow('Result',img)
                cv2.waitKey(1)
                if(num>=2):
                    if(myData==tempo):
                        track=-1
                        break
            if(track==-1):
                break
            num=num+1
        print(myData)
        time.sleep(2)
        cap.release()
        cv2.destroyAllWindows()