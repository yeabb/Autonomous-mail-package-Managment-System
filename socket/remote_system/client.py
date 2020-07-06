import socket
import RPi.GPIO as GPIO
import time
import numpy as np
import lcddriver
import lcddriver

display = lcddriver.lcd()
GPIO.setmode(GPIO.BCM)
MATRIX=[[1,2,'A',3],
        [4,5,'B',6],
        [7,8,'C',9],
        ['*',0,'D','#']]
ROW=[26,19,13,6] 
COL=[5,0,7,1]



try:
    while True:
        for j in range(4):
            GPIO.setup(COL[j], GPIO.OUT)
            GPIO.output(COL[j],1)
            
        for i in range(4):
            GPIO.setup(ROW[i], GPIO.IN,pull_up_down=GPIO.PUD_UP)

        display.lcd_display_string("welcome",1)
        time.sleep(3)
        display.lcd_clear()
        display.lcd_display_string("enter your pin",1)
        #x=input("put your name here please:")
        
        x=""
        num=""
        while True:
            for j in range(4):
                GPIO.output(COL[j],0)
                for i in range(4):
                    if GPIO.input(ROW[i])==0:
                        num=MATRIX[i][j]
                        if(num=="A"):
                            break
                        x=x+str(num)
                        print(x)
                        display.lcd_clear()
                        display.lcd_display_string(x,1)
                        
                        while(GPIO.input(ROW[i])==0):
                            pass
                
                GPIO.output(COL[j],1)
            if(num=="A"):
                break        
                
        display.lcd_clear()
    
        
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("", 8000))
        s.send(bytes(x,"utf-8"))
        inst = s.recv(1024).decode("utf-8")
        while True:
            if(inst=="wrong"):
                
                display.lcd_display_string("Wrong!try again",1)
                
                time.sleep(2)
                display.lcd_clear()
                
                display.lcd_display_string("enter your pin",1)
                x=""
                num=""
                while True:
                    for j in range(4):
                        GPIO.output(COL[j],0)
                        for i in range(4):
                            if GPIO.input(ROW[i])==0:
                                num=MATRIX[i][j]
                                if(num=="A"):
                                    break
                                x=x+str(num)
                                print(x)
                                display.lcd_clear()
                                display.lcd_display_string(x,1)
                                
                                while(GPIO.input(ROW[i])==0):
                                    pass
                        
                        GPIO.output(COL[j],1)
                    if(num=="A"):
                        break        
                
                display.lcd_clear()
                s.send(bytes(x,"utf-8"))
                    
            elif(inst=="1"):

                GPIO.setmode(GPIO.BCM)

                GPIO.setup(11,GPIO.OUT)

                GPIO.output(11,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box one--0pened",1)
                print("box one is opened")
                time.sleep(2)
                GPIO.output(11,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box one--closed",1)
                print("box one is closed")
                time.sleep(2)
                s.send(bytes("Box-1 closed succesfully","utf-8"))
                display.lcd_clear()
                display.lcd_display_string("have a good one!",1)
                time.sleep(2)
                display.lcd_clear()
                break
            elif(inst=="2"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(25,GPIO.OUT)

                GPIO.output(25,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box two is opened",1)
                print("box two is opened")
                time.sleep(1)
                GPIO.output(25,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box two is closed",1)
                time.sleep(2)
                print("box two is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
                display.lcd_clear()
                display.lcd_display_string("have a good one!",1)
                time.sleep(2)
                display.lcd_clear()
                break
            elif(inst=="3"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(4,GPIO.OUT)

                GPIO.output(4,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box three is opened",1)
                print("box three is opened")
                time.sleep(1)
                GPIO.output(4,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box three is closed",1)
                print("box three is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
            elif(inst=="4"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(17,GPIO.OUT)

                GPIO.output(17,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box four is opened",1)
                print("box four is opened")
                time.sleep(1)
                GPIO.output(17,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box four is closed",1)
                print("box four  is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
            elif(inst=="5"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(27,GPIO.OUT)

                GPIO.output(27,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box five is opened",1)
                print("box five is opened")
                time.sleep(1)
                GPIO.output(27,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box five is closed",1)
                print("box five is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
            elif(inst=="6"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(22,GPIO.OUT)

                GPIO.output(22,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box six is opened",1)
                print("box six is opened")
                time.sleep(1)
                GPIO.output(22,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box six is closed",1)
                print("box six  is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
            
            elif(inst=="7"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(10,GPIO.OUT)

                GPIO.output(10,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box seven is opened",1)
                print("box seven is opened")
                time.sleep(1)
                GPIO.output(10,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box seven is closed",1)
                print("box seven is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
                
            elif(inst=="8"):
                GPIO.setmode(GPIO.BCM)

                GPIO.setup(9,GPIO.OUT)

                GPIO.output(9,GPIO.LOW)
                display.lcd_clear()
                display.lcd_display_string("box eight is opened",1)
                print("box eight is opened")
                time.sleep(1)
                GPIO.output(9,GPIO.HIGH)
                display.lcd_clear()
                display.lcd_display_string("box eight is closed",1)
                print("box eight is closed ")
                s.send(bytes("Box-1 closed succesfully","utf-8"))
            
            inst = s.recv(1024).decode("utf-8")
        
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    GPIO.cleanup()
        
        
    
