import cv2
import numpy as np

## video path to receive video path inside the '.mp4'
video_path = 'redv.mp4'
## Saving the video inside cap; capture
cap = cv2.VideoCapture(video_path)


# Output size for the ROI Setting
output_size = (300, 500) #(width, height)

# initialize writing video; saved format
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

if not cap.isOpened():
exit()

# Resetting the CSRT Tracker
# Terminal:opencv-contrib-python
tracker = cv2.TrackerCSRT_create()

## Bring the first ROI(Region of Interest)
ret, img = cap.read()

cv2.namedWindow('Select Window')
cv2.imshow('Select Window', img)

##Setting ROI(Region of Interest)
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

#Initialize Tracker setting with ROI
tracker.init(img, rect)


# Receiving video per frame through the while statement
while True:
ret, img = cap.read()

if not ret:
exit()
## Sucessfully updating the object tracking constantly
## This follows the assigned object to constantly track the object
success, box = tracker.update(img)

left, top, w, h = [int(v) for v in box]

center_x = left + w / 2
center_y = top + h / 2

result_top = int(center_y - output_size[1] / 2)
result_bottom = int(center_y + output_size[1] / 2)
result_left = int(center_x - output_size[0] / 2)
result_right = int(center_x + output_size[0] / 2)

## Eliminates the white box from the cropped output
result_img = img[result_top:result_bottom, result_left:result_right]
## Saves the cropped output
out.write(result_img)

cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)

# Represents the video and quits by the key('q')
cv2.imshow('result_img', result_img)
cv2.imshow('img', img)
if cv2.waitKey(1) == ord('q'):
break
