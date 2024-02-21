import cv2 as cv
import numpy as np
import json

## IF IMAGE IS TOO BIG TO FIT ON SCREEN CHANGE SCALE OPTION TO SOMETHING <1
SCALE = 0.5

class Configure:
    def __init__(self):
        video = cv.VideoCapture("vid.mp4")
        cv.namedWindow('Configure points')
        cv.setMouseCallback('Configure points', self.click_event)

        _, frame = video.read()
        height, width, _ = frame.shape
        sHeight, sWidth = int(height*SCALE), int(width*SCALE)
        self.frame = cv.resize(frame, (sWidth, sHeight)) 

        self.pointList = []
        self.cache = []
        self.completed = False

    def click_event(self, event, x, y, _, __):
        if event == cv.EVENT_LBUTTONDOWN:
            if self.completed == False:
                self.pointList.append((x,y))
                self.cache.append(self.frame.copy())
                cv.circle(self.frame, (x, y), 5, (0, 0, 255), -1)
                if len(self.pointList) >= 2:
                    cv.line(self.frame, self.pointList[-2], self.pointList[-1], (0, 0, 255), 2) 
            else:
                print("You've already completed the selection exit or hit backspace to redo")
    
    def backspace(self):
        try:
            self.frame = self.cache.copy()[-1]
            self.cache.pop()
            self.pointList.pop()
            self.completed = False
        except IndexError:
            print("You've reached the end of the cache")
    
    def saveData(self):
        with open("../configuration.json", "w+") as f:
            keys = ["x", "y"]
            data = [{keys[i]:val*SCALE for i,val in enumerate(data)} for data in self.pointList]
            jsonData = {"scale" : SCALE, "points" : data}
            f.write(json.dumps(jsonData))
    
    def finish(self):
        if len(self.pointList) >= 3 and self.completed == False:
            x,y = self.pointList[0]
            self.pointList.append((x,y))
            self.cache.append(self.frame.copy())
            cv.circle(self.frame, (x, y), 5, (0, 0, 255), -1)  
            cv.line(self.frame, self.pointList[-2], self.pointList[-1], (0, 0, 255), 2)
            
            contours = np.array(self.pointList)
            overlay = self.frame.copy() 
            cv.fillPoly(overlay, pts = [contours], color =(0,255,0))
            alpha = 0.3
            self.frame = cv.addWeighted(overlay, alpha, self.frame, 1 - alpha, 0) 
            self.saveData()
            self.completed = True
        
        else:
            if self.completed:
                print("Selection has been made please close the window or hit backspace to redo")
            else:
                print("Please draw a polygon around the entire area that needs monitoring")

    def start(self):
        while True:
            cv.imshow('Configure points', self.frame)
            k = cv.waitKey(1) & 0xFF                
            if k == 13:
                self.finish()
            if k == 8:
                self.backspace() 
            if k == 27 or k == ord("q"):
                break
            if cv.getWindowProperty('Configure points', cv.WND_PROP_VISIBLE) <1:
                break
            
if __name__ == "__main__":
    config = Configure()
    config.start()
