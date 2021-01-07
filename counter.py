#camera.py
# import the necessary packages
import cv2
import numpy as np
import sys

# defining face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')



class VideoCamera(object):

    def __init__(self):

        self.count =0
        self.count1 =0 
        self.count2 =0
       
        #capturing video
        self.video = cv2.VideoCapture(0)

        #detetcting faces
        self.ok, self.frame = self.video.read()

        if not self.ok:
            print ('Cannot read video file')
            sys.exit()

        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.faces = face_cascade.detectMultiScale(self.gray, 1.3, 5)
        if len(self.faces):
            for (x,y,w,h) in self.faces:
                self.bbox = (x,y,w,h)
        else:
            self.bbox = (10,0,10,10)

        #self.bbox = cv2.selectROI("Tracking",self.frame, False)

        #init tracker
        self.tracker = cv2.TrackerCSRT_create()
        print(self.bbox)

        # Initialize tracker with first frame and bounding box
        self.ok = self.tracker.init(self.frame, self.bbox)
      
        
    def __del__(self):
        #releasing camera
        self.video.release()

    def get_frame(self,idx):
    #extracting frames
        ok,frame = self.video.read()
        ok, self.bbox = self.tracker.update(frame)
        if ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            cv2.line(frame, (0,int(frame.shape[0]/2)),(int(frame.shape[1]),int(frame.shape[0]/2)), (0,255,0),2)
            cv2.line(frame, (int(frame.shape[1]/2),0),(int(frame.shape[1]/2),int(frame.shape[0])), (0,255,0),2)
        
            if idx==0:
                if p1[1] >= int(frame.shape[0]/2):
                    self.count = self.count +1
                if p1[1] <= int(frame.shape[0]/2) and self.count >0:
                    self.count1 = self.count1 +1
                if self.count >0 and self.ount1>0:
                    self.count2=self.count2+1
                    self.count1 = 0
                    self.count = 0

            if idx == 1:
                if p2[1] >= int(frame.shape[0]/2):
                    self.count = self.count +1
                if p2[1] <= int(frame.shape[0]/2) and self.count >0:
                    self.count1 = self.count1 +1
                if self.count >0 and self.count1>0:
                    self.count2=self.count2+1
                    self.count1 = 0
                    self.count = 0
            

            if idx == 2:    
                if int((p2[0]+p1[0])/2) >= int(frame.shape[1]/2):
                    self.count = self.count +1
                if int((p2[0]+p1[0])/2) <= int(frame.shape[0]/2) and self.count >0:
                    self.count1 = self.count1 +1
                if self.count >0 and self.count1>0:
                    self.count2=self.count2+1
                    self.count1 = 0
                    self.count = 0
               
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    

        cv2.putText(frame, "Count : " + str(int(self.count2)), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)

        ok, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_count(self):
        return (self.count2)