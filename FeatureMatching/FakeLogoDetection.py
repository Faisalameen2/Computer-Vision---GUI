# fs "I don't think this is the library that we will use for GUI /Basheer"
# Yes, i may delete the library, but i just waiting for the GUI/ fs
from PyQt5.QtCore import *

import cv2  # omran + fs
import numpy as np  # Basheer


class FakeLogosDetection:

    '''
        this is not the final version. we may add new methods if we need it. 

        useful link:
        https://datahacker.rs/feature-matching-methods-comparison-in-opencv/
    '''

    def __init__(self):

        # Preparing the FLANN Based matcher
        self.FLAN_INDEX_KDTREE = 0
        self.index_params = dict(algorithm=self.FLAN_INDEX_KDTREE, trees=5)
        self.search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(
            self.index_params, self.search_params)

        self.detector = cv2.SIFT_create()

        '''
            You need to initilize the variables here before use them in the below methods.
            follow the OOP concepts.

            for example in load_image method:
                if you want to resize the image
                you will define the variable here
                img_size = 250

                and use it inside load_image method.
        '''

    def load_image(self, img1_path, img2_path=None):  # omran
        '''
        it takes ether two or one image path as parameter

        in case of two paths is given it will return two lists each contain the image and its keypoints and descriptor
        in case of one paths is given it will return one lists contain the image and its keypoints and descriptor
        all good ? 

        '''
        if(img2_path == None):
            img = cv2.imread(img1_path)
            img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
            gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            #orb = cv2.ORB_create()
            kp, des = self.detector.detectAndCompute(gray_img, None)
            return img, kp, des
        else:
            img1 = cv2.imread(img1_path)
            img2 = cv2.imread(img2_path)
            img1 = cv2.resize(img1, (600, 600), interpolation=cv2.INTER_AREA)
            img2 = cv2.resize(img2, (600, 600), interpolation=cv2.INTER_AREA)
            #orb = cv2.ORB_create()
            kp1, des1 = self.detector.detectAndCompute(img1, None)
            kp2, des2 = self.detector.detectAndCompute(img2, None)
            return [img1, kp1, des1], [img2, kp2, des2]

    def compute_matches(self, des_image1, des_image2=None, n_coef=0.4):  # basheer
        '''
            Comment on 31-March-22 !
            *Solved 2-April-22*
            Good work. However, the code below is applicable only for real time detection. So, i need to
            add if statement for comparing two images. you can see the video here 
            (https://www.youtube.com/watch?v=Fe-KWKPk9Zc) for brute force algorithm (if the code below
            is applicable for comparing two images just write a comment below)
            *Solved 2-April-22*

            *Sloved 1-April-22*
            IMPORTANT NOTE:
            Plese use the variables that initialize it in the constructor. Also, do not forget self.
            further, you can make the k, and 0.68 as parameters in this method. Therefour, i can 
            optimaize it later. For now, put k=2, 0.68 as defulat value for the parameters.
            *Sloved 1-April-22*

        '''
        counter_good = 0
        counter_all = 0
        # Image-to-Image matching and real time matching
        matches = self.flann.knnMatch(des_image1, des_image2, k=2)
        good_matches = []

        for m1, m2 in matches:
            if m1.distance < n_coef * m2.distance:
                good_matches.append([m1])
                counter_good = counter_good + 1
            else:
                counter_all = counter_all + 1

        return good_matches

        # Drawing Matches
        # matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2) /for image-to-image
        # cv2.drawMatchesKnn(input_image,input_keypoints,frame,output_keypoints,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)/ real-time

    def input_image(self, inputImage):  # fsfs
        '''
            Comment on 31-March-22 !
            *Solved on 4/1/2022*
            1- delete global filepath
            2- use OpenCV to read images (we need to use one library for reading images to 
            prevent the conflicts)
            3- add the path variable as parameter in this method

        '''

        '''
            here you will write a code to let the user upload an image from his/her computer.
        '''
        # Here is the Temporary code until GUI is ready, you must enter the file path by yourself.

        filepath = input("Enter file path:\n")

        image = cv2.imread(filepath)  # Pass the path to cv2

        # print(image.shape)
        #cv2.imshow("Image", image)

        # cv2.waitKey(0)
        return image

        # The below code is not ready 100%, it will be modified once the GUI is uploaded.

        # def getfile(self):
        #filepath = QFileDialog.getOpenFileName(self, 'Open file', '',"Image files (*.jpg)")
        # self.le.setPixmap(QPixmap(filepath))

    def real_time_matching(self, input_image, input_keypoint, input_desc):  # mhm
        '''
            here you need to write a code to open the camera and start matching the image that we 
            have in the database and start matching.
            'https://192.168.8.191:8080/video'
        '''

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()

        #detector = cv2.ORB_create(nfeatures=5000)
        try:
            while(ret):
                ret, frame = cap.read()

                frame = cv2.resize(frame, (600, 600))
                
                frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                output_keypoints, output_desc = self.detector.detectAndCompute(
                    frame_bw, None)
                matching = self.compute_matches(
                    des_image1=input_desc, des_image2=output_desc)

                if matching != None:
                    output_final = cv2.drawMatchesKnn(
                        input_image, input_keypoint, frame, output_keypoints, matching, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                    cv2.imshow("final output", output_final)
                else:
                    # cv2.imshow("final output", frame)
                    output_final = cv2.drawMatchesKnn(
                        input_image, input_keypoint, frame, output_keypoints, matching, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                    cv2.imshow("final output", output_final)

                cv2.waitKey(50)
                if cv2.getWindowProperty('final output', 0) == -1:
                    break
        except:
            pass

    def image_to_image_matching(self, img1, kp1, img2, kp2, matches):  # mhm
        '''
            in the previous method, we apply it in real time. Now, we need to compare or matching 
            between two images only.
        '''
        # [:m]
        matching_result = cv2.drawMatchesKnn(
            img1, kp1, img2, kp2, matches, None, flags=2)
        # cv2.imshow("image1", img1)
        # cv2.imshow("image2", img2)
        cv2.imshow("Result of matching", matching_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # we may delete the below function
    def show_text(self, img, match_percent):  # omran
        '''
            Comment on 31-March-22 !

            plese add the configration for the text like, color, location of the text, and ect. Also,
            make the threshold (0.85) as parameter in the method. 

            the second thing, check if the below code is applicable in real-time and when comparing 
            two images.
        '''
        THRESHOLD = 0.85
        org = (50, 75)
        fontScale = 2
        c = (0, 0, 255)
        thickness = 4
        font = cv2.FONT_ITALIC

        if(match_percent >= THRESHOLD):
            new_img = cv2.putText(img=img, text='Real', org=org, color=c,
                                  fontFace=font, fontScale=fontScale, thickness=thickness)
        else:
            new_img = cv2.putText(img=img, text='Real', org=org, color=c,
                                  fontFace=font, fontScale=fontScale, thickness=thickness)

        return new_img

        # th old function

        #     def compute_matches(self, des_image1, des_image2=None, des_frame=None, n_coef=0.68, real_time=True):  # basheer
        # '''
        #     Comment on 31-March-22 !
        #     *Solved 2-April-22*
        #     Good work. However, the code below is applicable only for real time detection. So, i need to
        #     add if statement for comparing two images. you can see the video here
        #     (https://www.youtube.com/watch?v=Fe-KWKPk9Zc) for brute force algorithm (if the code below
        #     is applicable for comparing two images just write a comment below)
        #     *Solved 2-April-22*

        #     *Sloved 1-April-22*
        #     IMPORTANT NOTE:
        #     Plese use the variables that initialize it in the constructor. Also, do not forget self.
        #     further, you can make the k, and 0.68 as parameters in this method. Therefour, i can
        #     optimaize it later. For now, put k=2, 0.68 as defulat value for the parameters.
        #     *Sloved 1-April-22*

        # '''
        # # If the user chose (Open Camera) choice will be True otherwise it will set to False
        # if (real_time):
        #     # Function for Computing Matches between the train and query descriptors
        #     if(len(des_frame) != 0 and len(des_image1) != 0):
        #         matches = self.flann.knnMatch(np.asarray(
        #             des_frame, np.float32), np.asarray(des_image1, np.float32), k=2)
        #         good = []
        #         for m, n in matches:
        #             if m.distance < n_coef*n.distance:
        #                 good.append([m])
        #                 return good
        #             else:
        #                 return None
        #     else:
        #         # There are no descriptor
        #         pass
        # else:
        #     # Image-to-Image matching using Brute-Force
        #     matches = self.flann.knnMatch(des_image1, des_image2, k=2)
        #     good_matches = []

        #     for m1, m2 in matches:
        #         if m1.distance < 0.4 * m2.distance:
        #             good_matches.append([m1])

        #     return good_matches

        # # Drawing Matches
        # # matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2) /for image-to-image
        # # cv2.drawMatchesKnn(input_image,input_keypoints,frame,output_keypoints,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)/ real-time
