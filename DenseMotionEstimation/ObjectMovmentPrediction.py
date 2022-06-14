
import time
import cv2
import numpy as np


class ObjectMovmentDetection:
    # see the following github https://github.com/niconielsen32/ComputerVision/blob/master/opticalFlow/denseOpticalFlow.py
    # and this is the video for explaination https://www.youtube.com/watch?v=WrlH5hHv0gE
    # https://www.geeksforgeeks.org/python-opencv-dense-optical-flow/?ref=gcse
    def __init__(self):
        pass

    def draw_flow(self, img, flow, step=16):  # omran
        h, w = img.shape[:2]
        y, x = np.mgrid[step/2:h:step, step /
                        2:w:step].reshape(2, -1).astype(int)
        fx, fy = flow[y, x].T

        lines = np.vstack([x, y, x-fx, y-fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)

        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.polylines(img_bgr, lines, 0, (0, 255, 0))

        for (x1, y1), (_x2, _y2) in lines:
            cv2.circle(img_bgr, (x1, y1), 1, (0, 255, 0), -1)

        return img_bgr

    def draw_hsv(self, flow):  # fsfs
        h, w = flow.shape[:2]
        fx, fy = flow[:, :, 0], flow[:, :, 1]

        ang = np.arctan2(fy, fx) + np.pi
        v = np.sqrt(fx*fx+fy*fy)

        hsv = np.zeros((h, w, 3), np.uint8)
        hsv[..., 0] = ang*(180/np.pi/2)
        hsv[..., 1] = 255
        hsv[..., 2] = np.minimum(v*4, 255)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return bgr
    # output_file_path

    def video_motion_estimation(self, video_file_path):  # mhm
        cap = cv2.VideoCapture(video_file_path)

        ret, first_frame = cap.read()
        prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

        while(cap.isOpened()):
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
                                                None,
                                                0.5, 3, 15, 3, 5, 1.2, 0)

            cv2.imshow("optical flow", self.draw_flow(gray, flow))
            cv2.imshow("dense optical flow", self.draw_hsv(flow))

            prev_gray = gray
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # The following frees up resources and
        # closes all windows
        cap.release()
        cv2.destroyAllWindows()

    def real_time(self):
        cap = cv2.VideoCapture(0)

        suc, prev = cap.read()
        prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

        while True:

            suc, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # start time to calculate FPS
            start = time.time()

            flow = cv2.calcOpticalFlowFarneback(
                prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

            prevgray = gray

            # End time
            end = time.time()
            # calculate the FPS for current frame detection
            fps = 1 / (end-start)

            print(f"{fps:.2f} FPS")

            cv2.imshow('flow', self.draw_flow(gray, flow))
            cv2.imshow('flow HSV', self.draw_hsv(flow))

            key = cv2.waitKey(5)
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
