import cv2
import numpy as np
import time
from face_detector import FaceDetector
from eye_tracker import EyeTracker
from resize_face import ResizeFace
from randam_play_movie import RandomMoviePlayer

# EARの閾値を設定
EAR_THRESHOLD = 0.4

# 顔検出器のインスタンスを作成
face_detector = FaceDetector("shape_predictor_68_face_landmarks.dat")

# カメラから画像を取得する
cap = cv2.VideoCapture(0)

# 瞬きの回数をカウントする変数を初期化
count = 0

# 現在の時刻を取得
start_time = time.time()

# 1分ごとの瞬き回数をカウントする変数を初期化
blink_count_per_minute = 0

blink_detected = False  # まばたきが検出されたかのフラグ
blink_message_duration = 0.3  # メッセージを表示する秒数
last_blink_time = None  # 最後にまばたきが検出された時刻
no_face_start_time = None  # 顔が検出されない状態が始まった時刻

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
blink_interval = 30  # 点滅の間隔（フレーム数）
counter = 0  # フレームカウンタ

video_paths = [
            "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/akiramennayo-shuzo.mp4",
            "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/shuzo-kiminradekiru.mp4",
            "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/shuzo-pekin.mp4"]

while True:
    # フレームを取得する
    ret, frame = cap.read()
    if not ret:
        break

    # 顔を検出する
    faces = face_detector.detect_faces(frame)
    # 顔が検出されたかどうかを True/False で返す
    
    # 顔ごとに処理
    for face in faces:
        # 顔の領域をリサイズしてランドマークを検出
        landmarks = ResizeFace.resize_face(frame, face, face_detector)

        # 左目と右目の座標を取得
        left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
        right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])

        # EARを計算
        ear_left = EyeTracker.calculate_ear(left_eye)
        ear_right = EyeTracker.calculate_ear(right_eye)
        # EARが閾値以下の場合、瞬きと判定
        if (ear_left + ear_right)  < EAR_THRESHOLD:
            count += 1
            blink_count_per_minute += 1
            color = (0, 0, 255)  # 赤色
            blink_detected = True
            last_blink_time = time.time()
        else:
            color = (0, 255, 0)  # 緑色

        # 目の周囲に枠を描く
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), color, 2)
        
    # まばたきが検出された場合、テキストを表示
    if blink_detected and (time.time() - last_blink_time) < blink_message_duration:
        cv2.putText(frame, "You blinked!", (frame_width // 2 - 450, frame_height // 2+50), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2)



    # 現在の時刻を取得
    current_time = time.time()
    # 経過時間を計算
    elapsed_time = round(current_time - start_time, 0)
    
    # 結果を表示する
    cv2.putText(frame, "Blink Count: {}".format(count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    cv2.putText(frame, "current_time: {}".format(elapsed_time), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    cv2.imshow("Frame", frame)
    
    

    # 1分ごとの処理
    if current_time - start_time >= 60:  # 1分経過したか確認
        print(f"1 Minute Blink Count: {blink_count_per_minute}")
        start_time = current_time
        if blink_count_per_minute > 25:
            
            
            # 一定間隔で赤いオーバーレイを点滅
            if counter % blink_interval < blink_interval / 2:
                overlay = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
                overlay[:] = (0, 0, 255)  # 赤色
                frame = cv2.addWeighted(frame, 1, overlay, 0.5, 0)
                
            cv2.imshow("Frame", frame)
            
            player = RandomMoviePlayer(video_paths)
            player.play()
            
        blink_count_per_minute = 0 
            
            
            
    # 顔が検出されない場合
    if len(faces) == 0:
        if no_face_start_time is None:
            # 顔が検出されない状態が始まった時刻を記録
            no_face_start_time = time.time()
        elif time.time() - no_face_start_time > 5:  # 5秒経過したかチェック
            # 一定間隔で赤いオーバーレイを点滅
            if counter % blink_interval < blink_interval / 2:
                overlay = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
                overlay[:] = (0, 0, 255)  # 赤色
                frame = cv2.addWeighted(frame, 1, overlay, 0.5, 0)
                
            cv2.imshow("Frame", frame)
            
            player = RandomMoviePlayer(video_paths)
            player.play()
            pass
    else:
        # 顔が検出された場合、タイマーをリセット
        no_face_start_time = None
            
        
    

    cv2.putText(frame, "1 Minute Blink Count: {}".format(blink_count_per_minute), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # Escキーで終了
        break

cap.release()
cv2.destroyAllWindows()
