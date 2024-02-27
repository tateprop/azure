from motion import detectMotion
import cv2
import time


class Detector:
    def __init__(self, bufferSize=100):
        self.buffer = []
        self.bufferSize = bufferSize
        self.globalTime = 0

    def debugWrapper(func):

        def inner(*args):
            self = args[0]
            start = time.time()
            if self.globalTime:
                print(start-self.globalTime)
            func(*args)
            print(f"{func.__name__} took {time.time() - start}")
            if self.globalTime:
                print((start-self.globalTime) + (time.time() - start))
            self.globalTime = time.time()

        return inner

    def addBuffer(self, frame):
        self.buffer.append(frame)
        if len(self.buffer) >= self.bufferSize:
            self.buffer.pop(0)

    def detectCars(self, frame):
        pass

    @debugWrapper
    def compute(self, frame1, frame2):
        # self.addBuffer(frame1)
        # if detectMotion(frame1, frame2):
        #     #self.detectCars(frame1)
        pass


# Dectector
# Functions
# 1 - detect motion
# 2 - hold buffer
# 3 - detect cars
# 4 - in box?
# 5 - work out state
