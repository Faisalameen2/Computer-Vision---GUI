from tensorflow.keras.models import load_model
import cv2
import numpy as np


class SmartDisck:

    '''
        this is not the final version. we may add new methods if we need it. 
    '''

    def __init__(self):
        '''
            You need to initilize the variables here before use them in the below methods.
            follow the OOP concepts.

            for example in model_training method:
                you will initilize the batch_size here:
                batch_size = 32

                and use it inside model_training method.
        '''
        self.res_model = load_model('FacialRecognition/modelv2.h5')

    def detect_faces(self, frame):
        '''
            here you neet to write a function to extract the faces inide each image. you may use
            haar cascade or MTCNN (better) algorithms.

            you can add as many parameters you want.
        '''
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        detected_face = face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return detected_face

    def get_extended_image(self, img, x, y, w, h, k=0.1):
        '''
            here you want to show the bounded box around the face.

            you can add as many parameters you want.
        '''
        if x - k*w > 0:
            start_x = int(x - k*w)
        else:
            start_x = x
        if y - k*h > 0:
            start_y = int(y - k*h)
        else:
            start_y = y

        end_x = int(x + (1 + k)*w)
        end_y = int(y + (1 + k)*h)

        face_image = img[start_y:end_y,
                         start_x:end_x]
        face_image = cv2.resize(face_image, (150, 150))
        face_image = np.expand_dims(face_image, axis=0)
        return face_image

    def prediction(self, face):
        classes = ['Unknown', 'Mohammed', 'Omran', 'Faisal']
        y_pred = self.res_model.predict(face)
        y_pred_class = classes[np.array(y_pred[0].argmax(axis=0))]
        confidence = np.array(y_pred[0]).max(axis=0)

        return y_pred_class, confidence

    def real_time_recognition(self):
        cap = cv2.VideoCapture(0)

        while True:
            succ, frame = cap.read()

            if not succ:
                break

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detected_face = self.detect_faces(frame)

            if len(detected_face) > 0:
                for (x, y, w, h) in detected_face:
                    face_image = self.get_extended_image(
                        frame, x, y, w, h, 0.5)

                    class_name, conf = self.prediction(face_image)

                    cv2.rectangle(frame,
                                  (x, y),  # start_point
                                  (x+w, y+h),  # end_point
                                  (0, 255, 0),
                                  2)  # thickness in px
                    cv2.putText(frame,
                                # text to put
                                f"{class_name} - {conf*100}%",
                                (x, y),
                                cv2.FONT_HERSHEY_PLAIN,  # font
                                2,  # fontScale
                                (0, 255, 0),
                                2)  # thickness in px

            cv2.imshow("Face detector - to quit press ESC", frame)

            # Exit with ESC
            key = cv2.waitKey(1)
            if key % 256 == 27:  # ESC code
                break

        # when everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
