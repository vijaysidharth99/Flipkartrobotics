import cv2

video = cv2.VideoCapture('http://172.16.244.52:4747/video')

# Check if the webcam is opened correctly
if not video.isOpened():
    raise IOError("Cannot open webcam")

# Read first frame
ok, frame = video.read()
cv2.imwrite('photo2.png', frame)

while True:
    ok, frame = video.read()
    cv2.imshow('photo', frame)
    k = cv2.waitKey(2) & 0xff
    if k == 27:
        cv2.imwrite('photo2.png', frame)
        print(k)
        break