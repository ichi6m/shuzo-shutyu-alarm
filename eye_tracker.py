import numpy as np
import dlib
import cv2
import numpy as np
from face_detector import FaceDetector  

class EyeTracker:
    @staticmethod
    def calculate_ear(eye_points):
        # 目の縦の長さを計算
        vertical1 = np.linalg.norm(eye_points[1] - eye_points[5])
        vertical2 = np.linalg.norm(eye_points[2] - eye_points[4])

        # 目の横の長さを計算
        horizontal = np.linalg.norm(eye_points[0] - eye_points[3])

        # EARを計算
        ear = (vertical1 + vertical2) / (2.0 * horizontal)
        return ear




if __name__ == "__main__":
    # EARの閾値を設定
	EAR_THRESHOLD = 0.4

	# 顔検出器のインスタンスを作成
	face_detector = FaceDetector("shape_predictor_68_face_landmarks.dat")

	cap = cv2.VideoCapture(0)
	blink_count = 0
	start_time = cv2.getTickCount()

	while True:
		ret, frame = cap.read()
		if not ret:
			break

		faces = face_detector.detect_faces(frame)
		for face in faces:
			landmarks = face_detector.get_landmarks(frame, face)
			landmarks = np.array([(p.x, p.y) for p in landmarks.parts()])

			# 左目と右目のEARを計算
			left_eye = landmarks[36:42]
			ear_left = EyeTracker.calculate_ear(left_eye)
			right_eye = landmarks[42:48]
			ear_right = EyeTracker.calculate_ear(right_eye)

			# EARが閾値以下の場合、瞬きと判定
			if (ear_left + ear_right)  < EAR_THRESHOLD:
				blink_count += 1

		# 経過時間の計算（秒単位）
		time_elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

		# 結果のテキストを描画
		cv2.putText(frame, f"Blink Count: {blink_count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
		cv2.putText(frame, f"Elapsed Time: {int(time_elapsed)} s", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

		cv2.imshow("Frame", frame)

		key = cv2.waitKey(1)
		if key == 27:  # Escキーで終了
			break

	cap.release()
	cv2.destroyAllWindows()