import cv2
import numpy as np
import time
import math


class TrackObject:
    def __init__(self, color):
        self.info = []                                              # stores the (x,y,time,contour) throughout
        self.start_time = time.time()
        self.contour = self.x = self.y = self.h = self.w = []       # stores the data at each time interval
        self.count = 0
        if color == 'pink':
            # for pink color
            self.color = (203, 192, 255)
            self.hsv_lb = np.array([60, 30, 30])
            self.hsv_ub = np.array([165, 255, 255])

        elif color == 'green':
            # for green color
            self.color = (100, 255, 0)
            self.hsv_lb = np.array([30, 40, 0])
            self.hsv_ub = np.array([115, 90, 255])

        elif color == 'green2':
            # for green color
            self.color = (100, 255, 0)
            self.hsv_lb = np.array([26, 26, 130])
            self.hsv_ub = np.array([100, 255, 200])

        elif color == 'blue':
            # for green color
            self.color = (100, 255, 0)
            self.hsv_lb = np.array([0, 0, 0])
            self.hsv_ub = np.array([255, 255, 248])

    def track_n_update(self, hsv_frame, frame, curr_time):
        mask = cv2.inRange(hsv_frame, self.hsv_lb, self.hsv_ub)

        # canny convert
        imgCanny = cv2.Canny(mask, 0, 0)

        # dilation function
        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

        self.x, self.y, self.h, self.w, self.contour, self.end_x, self.end_y= self.getContours(imgDil, frame)
        self.info.append([int(self.x + self.w/2), int(self.y + self.h/2), int(curr_time - self.start_time), self.contour])
        # print(self.x, self.y)

    def getContours1(self, img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                # cv2.drawContours((imgContour), contours, -1, (255, 0, 255), 7)
                perimeter = cv2.arcLength(cnt, True)                        # True means contour is closed
                approx = cv2.approxPolyDP(cnt, 0.098*perimeter, True)
                x, y, h, w = cv2.boundingRect(approx)
                # cv2.rectangle(imgContour, (x, y), (x + w, y + h), [0, 255, 0], 5)
                # cv2.circle(imgContour, (int(x + w/2), int(y + h/2)), 5, [0, 255, 0], -1)
                return x, y, h, w, cnt
        return 0, 0, 0, 0, []

    def getContours(self, img, img_og):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                perimeter = cv2.arcLength(cnt, True)  # True means contour is closed
                approx = cv2.approxPolyDP(cnt, 0.09 * perimeter, True)
                x, y, h, w = cv2.boundingRect(approx)  # create a bounding box around bot
                # h = 60
                # w = 60
                # x = x - 10
                # y = y - 10
                print(len(approx))
                if len(approx) == 4:  # if four end points are detected
                    # cx1 = (approx[0][0][0] + approx[1][0][0] + approx[2][0][0])/3
                    # cy1 = (approx[0][0][1] + approx[1][0][1] + approx[2][0][1])/3
                    # cx2 = (approx[0][0][0] + approx[3][0][0] + approx[2][0][0])/3
                    # cy2 = (approx[0][0][1] + approx[3][0][1] + approx[2][0][1])/3
                    circle1_x = int(x + h / 2)  # int((cx1+cx2)/2)
                    circle1_y = int(y + w / 2)  # int((cy1+cy2)/2)
                    cropped_img = img_og[y: y + h, x: x + w]
                    # for pink color
                    lower_range3 = np.array([90, 30, 30])
                    upper_range3 = np.array([165, 255, 255])
                    hsv1 = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
                    mask1 = cv2.inRange(hsv1, lower_range3, upper_range3)
                    imgCanny = cv2.Canny(mask1, 0, 0)

                    # dilation function
                    kernel = np.ones((5, 5))
                    imgDil2 = cv2.dilate(imgCanny, kernel, iterations=1)
                    contours, hierarchy = cv2.findContours(imgDil2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        print(area)
                        if area > 300 :
                            print(area)
                            perimeter2 = cv2.arcLength(cnt, True)  # True means contour is closed
                            approx2 = cv2.approxPolyDP(cnt, 0.09 * perimeter2, True)
                            x2, y2, h2, w2 = cv2.boundingRect(approx2)
                            # cv2.drawContours((img), contours, -1, (255, 0, 255), 7)
                            # cv2.imshow('sdfgsdf', img)
                            # cv2.waitKey(0)
                            print(len(approx2))
                            if len(approx2) == 4:
                                circle2_x = int(x2 + h2 / 2 + x)  # int((cx1+cx2)/2)
                                circle2_y = int(y2 + w2 / 2 + y)  # int((cy1+cy2)/2)
                                angle = math.radians(20)
                                A = [[math.cos(angle), -math.sin(angle)],
                                     [math.sin(angle), math.cos(angle)]]
                                B = [[circle2_x - circle1_x],
                                     [circle2_y - circle1_y]]
                                end_point = np.dot(A, B)
                                end_point_x = int(end_point[0] + circle1_x)
                                end_point_y = int(end_point[1] + circle1_y)
                                return x, y, h, w, cnt, end_point_x, end_point_y
                    # cv2.drawContours(img_og, [approx], -1, (255, 0, 255), 4)
                # cv2.imshow("osdfsdk", img_og)
                # cv2.waitKey(0)
                # cv2.rectangle(imgContour, (x, y), (x + w, y + h), [0, 255, 0], 5)
                # cv2.circle(imgContour, (int(x + w/2), int(y + h/2)), 5, [0, 255, 0], -1)
                return x, y, h, w, cnt, 0, 0
        return 0, 0, 0, 0, [], 0, 0
