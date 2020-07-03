import cv2
import numpy as np
import urllib2
import cookielib
from getpass import getpass
import sys
import os
from stat import *
import time

message = "GAS LEAK!!!!!"                                   # message to be sent
number = raw_input("Enter number: ")                        #emergency contact


if __name__ == "__main__":    
    username = "Add username"
    passwd = "Add pswd"

    message = "+".join(message.split(' '))


 #logging into the sms site
    url ='http://site24.way2sms.com/Login1.action?'
    data = 'username='+username+'&password='+passwd+'&Submit=Sign+in'

 #For cookies

    cj= cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #u=opener.open(url1)
 #Adding header details
    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120')]
    try:
	usock =opener.open(url, data)
    except IOError:
        print "error"
        #return()


cap = cv2.VideoCapture(0)
arrOpen=np.ones((5,5))                          # Array of 1s
arrClose=np.ones((20,20))

while True:
    flag = False
    ret, frame = cap.read()

    if ret: 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    else:
        print("Unsuccesful Camera Read")

    lower_red = np.array([0,100,100])
    upper_red = np.array([5,255,255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,arrOpen)          # This removes the noise in the image
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,arrClose)

    maskFinal=maskClose
    contours, h = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)       # Contours are curves joining all the continuous points, having same color or intensity
    
    cv2.drawContours(frame,contours,-1,(255,0,0),3)
    for i in range(len(contours)):
        x,y,w,h=cv2.boundingRect(contours[i])
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)  # Uncomment this if you want rectangle around object
        
        area = cv2.contourArea(contours[i])        
        if area > 1000:                                    # Set this as per your object dimensions
            flag = True

     
    if flag: 
        print ("ALERT!!!!Gas Leakage!!!!!!")
        jession_id =str(cj).split('~')[1].split(' ')[0]
    	send_sms_url = 'http://site24.way2sms.com/smstoss.action?'
    	send_sms_data = 'ssaction=ss&Token='+jession_id+'&mobile='+number+'&message='+message+'&msgLen=136'
    	opener.addheaders=[('Referer', 'http://site25.way2sms.com/sendSMS?Token='+jession_id)]
    	try:
        	sms_sent_page = opener.open(send_sms_url,send_sms_data)
    	except IOError:
        	print "error"
       		 #return()

    	print "success" 
	#time.sleep(10)                                    #Uncomment to send message after 10 seconds
   	 #return ()

       
    cv2.imshow("maskClose",maskClose)                       # Camera in black and white...detecting only red color
    cv2.imshow("cam",frame)
    
    k = cv2.waitKey(10)                                    # Set this as per your requirement
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()