import cv2
import os
from deepface import DeepFace
import matplotlib.pyplot as plt
 
#動画を読込み
#カメラ等でストリーム再生の場合は引数に0等のデバイスIDを記述する
video = cv2.VideoCapture(0)
 
# cascade_path = "haarcascade_frontalface_default.xml"
cascade_path = os.path.join(
            cv2.data.haarcascades, "haarcascade_frontalface_alt.xml"
        )
cascade = cv2.CascadeClassifier(cascade_path)
 
while video.isOpened():
    # フレームを読込み
    ret, frame = video.read()
 
    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    if not ret: break
    # 顔検出
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
     
    # 矩形線の色
    rectangle_color = (0, 255, 0) #緑色
 
    # 顔を検出した場合
    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
            # 顔部分の抽出
            cut_frame = frame[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
            # サイズの縮小
            # cut_frame = cv2.resize(cut_frame,(rect[2]//20, rect[3]//20))
            # 元のサイズにリサイズ。
            # cv2.INTER_NEAREST（最近傍補間）オプションを指定することで荒くなる。デフォルトでは cv2.INTER_LINEAR（バイリニア補間）となり、滑らかなモザイクとなる。
            # cut_frame = cv2.resize(cut_frame,(rect[2], rect[3]),cv2.INTER_NEAREST)
            # 縮小→復元画像で元の画像と置換
            # frame[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]=cut_frame
            
            print(type(cut_frame))

            plt.imshow(cut_frame[:,:,::-1])
            plt.show()
            #print(cut_frame)

            result = DeepFace.analyze(cut_frame, actions=['emotion'], enforce_detection=False)

            print(result)
 
    # フレームの描画
    cv2.imshow('frame', frame)
 
    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
 
#メモリの解放
video.release()
cv2.destroyAllWindows()