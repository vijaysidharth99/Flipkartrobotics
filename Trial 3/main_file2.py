import cv2
import time
import track_object2
import multiprocessing as mp  # Parallelizing using Pool.apply()
import socket

HEADER = 64
PORT = 80
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.16.244.168"
ADDR = (SERVER, PORT)

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

#def send(msg):
#    message = msg.encode(FORMAT)
#     client.send(message)

def worker(arg):
    trckr, hsv_frame, curr_time = arg
    trckr.track_n_update(hsv_frame, curr_time)


if __name__ == '__main__':

    no_trackers = 1  # number of trackers

    pool = mp.Pool(no_trackers)  # initialize multiprocessing

    # initialize the trackers
    Trackers = []
    # Trackers.append(track_object.TrackObject('pink'))
    Trackers.append(track_object2.TrackObject('green2'))

    fps = []

    # video = cv2.VideoCapture(2)
    video = cv2.VideoCapture('http://172.16.244.52:4747/mjpegfeed?960x720')#mjpegfeed')#52

    # Check if the webcam is opened correctly
    if not video.isOpened():
        raise IOError("Cannot open webcam")

    # Read first framee
    time.sleep(1)
    ok, frame = video.read()
    cv2.imwrite('savedImage.png', frame)
    new_frame_time = 0
    prev_frame_time = 0
    frameCount = 0
    startFrame = time.time()
    while True:
        # start timer for fps
        #timer = cv2.getTickCount()
        # Read the next frame
        ok, nframe = video.read()
        # new1_frame_time = time.time()
        # print("time:" , new1_frame_time-new_frame_time)
        # Exit if ok is not initialized
        if not ok:
            print("....ending...")
            time.sleep(2)
            break


        frameCount = frameCount + 1
        # blur the image using blur
        imgblur = cv2.blur(nframe, (10, 10))

        # convert blur image to hsv
        hsv = cv2.cvtColor(imgblur, cv2.COLOR_BGR2HSV)

        # Update location using multiprocessing
        # pool.map(worker, ((trckr, hsv, time.time()) for trckr in Trackers))
        #pool.apply(worker, args=(row, 4, 8)) for row in data

        for trckr in Trackers:
            # trckr.track_n_update(hsv, time.time())
            trckr.track_n_update(hsv, nframe, time.time())

        for trckr in Trackers:
            # print("Values are: ", trckr.x, trckr.y)
            if trckr.x == 0 and trckr.y == 0:
                cv2.putText(nframe, "Failed detection ", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            elif not trckr.x:
                print('......ERRORRRR!!!.......')
            else:
                cv2.rectangle(nframe, (trckr.x, trckr.y), (trckr.x + trckr.w, trckr.y + trckr.h), trckr.color, 5)
                cv2.circle(nframe, (int(trckr.x + trckr.w / 2), int(trckr.y + trckr.h / 2)), 5, trckr.color, 2)
                cv2.arrowedLine(nframe, (int(trckr.x + trckr.w / 2), int(trckr.y + trckr.h / 2)),
                                (trckr.end_x, trckr.end_y), [255, 255, 0], 5, tipLength=5)
                cv2.putText(nframe, "x = " + str(trckr.x + trckr.w / 2) + "Y = " + str(trckr.y + trckr.h / 2),
                                (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                # if (trckr.x > 300):
                #     send('f')
                # else:
                #     send('s')
                for index, item in enumerate(trckr.info):
                    if index == len(trckr.info) - 1:
                        break
                    # cv2.line(nframe, item[:2], trckr.info[index][:2], trckr.color, 5)

        # Display tracker type on frame
        # cv2.putText(imgContour, "Shape detection ", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Calculate fps
        # time.sleep()
        #fps.append(cv2.getTickFrequency() / (cv2.getTickCount() - timer))


        # draw grid lines
        nrows = 5
        ncols = 7
        for i in range(1, nrows):
            cv2.line(nframe, (0, int(nframe.shape[0] * i / nrows)), (nframe.shape[1], int(nframe.shape[0] * i / nrows)),
                     (0, 0, 0), 2, 1)
        for i in range(1, ncols):
            cv2.line(nframe, (int(nframe.shape[1] * i / ncols), 0), (int(nframe.shape[1] * i / ncols), nframe.shape[0]),
                     (0, 0, 0), 2, 1)

        # Display FPS
        #fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        #cv2.putText(nframe, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50),2)

        # Display the frame
        cv2.imshow("Tracking", nframe)
        # time.sleep(0.002)

        # Exit if ESC is pressed
        k = cv2.waitKey(2) & 0xff
        if k == 27:
            print(k)
            break
    EndFrame = time.time()
    print((EndFrame-startFrame)/frameCount)
    print(frameCount)
    #print("Average FPS: ", int(sum(fps)/len(fps)))
    #print("Min FPS: ", int(min(fps)))
    #pool.close()
    #pool.join()