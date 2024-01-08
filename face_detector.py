import dlib
import cv2

class FaceDetector:
    def __init__(self, predictor_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    def detect_faces(self, frame):
        return self.detector(frame)

    def get_landmarks(self, frame, face):
        return self.predictor(frame, face)

if __name__ == "__main__":
    #カメラから画像を取得する
    cap = cv2.VideoCapture(0)
    # 顔検出器のインスタンスを作成
    face_detector = FaceDetector("shape_predictor_68_face_landmarks.dat")
    # 瞬きカウントと現在の時刻用の変数を初期化
    blink_count = 0
    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = face_detector.detect_faces(frame)

        for face in faces:
            # 顔の枠線を描画
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

        # 経過時間の計算（秒単位）
        time_elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

        

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:  # Escキーで終了
            break

    cap.release()
    cv2.destroyAllWindows()