import dlib
import cv2
from face_detector import FaceDetector 

# 顔のリサイズ後のサイズを指定
RESIZED_FACE_WIDTH = 150

class ResizeFace:
    @staticmethod
    def resize_face(frame, face, face_detector):
        # 顔の領域を取得してリサイズ
        face_width = face.right() - face.left()
        scale = RESIZED_FACE_WIDTH / face_width
        resized_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        # リサイズした顔の領域でランドマークを検出
        resized_face_rect = dlib.rectangle(int(face.left() * scale), int(face.top() * scale),
                                           int(face.right() * scale), int(face.bottom() * scale))
        landmarks = face_detector.get_landmarks(resized_frame, resized_face_rect)
        return landmarks
