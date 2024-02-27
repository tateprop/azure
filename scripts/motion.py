import cv2
import json
import numpy as np

with open("../configuration.json", "r") as f:
    configure = json.loads(f.read())


def applyEffects(frame):
    # scale down frame to make motion detection faster
    newHeight = int(frame.shape[0] * configure["scale"])
    newWidth = int(frame.shape[1] * configure["scale"])
    frame = cv2.resize(frame, (newWidth, newHeight))

    mask = np.zeros_like(frame)
    points = [list(map(lambda x: int(x*configure["scale"]), d.values()))
              for d in configure["points"]]
    pts = np.array(points)
    mask = cv2.fillPoly(mask, pts=[pts], color=(255, 255, 255))

    frame = cv2.bitwise_and(frame, mask)
    return frame


def detectMotion(frame1, frame2):
    frame1, frame2 = applyEffects(frame1), applyEffects(frame2)

    diff = cv2.absdiff(frame1, frame2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 900:  # Test this field
            continue
        return True
    return False
