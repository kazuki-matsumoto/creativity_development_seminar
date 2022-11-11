from matplotlib.pyplot import imshow
import cv2
from datetime import datetime
import os

# /dev/video0を指定
DEV_ID = 0

# パラメータ
WIDTH = 330
HEIGHT = 220

def main():
    # /dev/video0を指定
    cap = cv2.VideoCapture(DEV_ID)

    # 解像度の指定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # キャプチャの実施
    ret, frame = cap.read()
    if ret:
        # ファイル名に日付を指定
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = "./pictures/" + date + ".jpg"
        
        cascade_path = os.path.join(
            cv2.data.haarcascades, "haarcascade_frontalface_alt.xml"
        )
        
        face_cascade = cv2.CascadeClassifier(cascade_path)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #顔を検出
        faces = face_cascade.detectMultiScale(gray)
        
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
        
        cv2.imwrite(path, frame)

        

    # 後片付け
    cap.release()
    cv2.destroyAllWindows()
    return


if __name__ == "__main__":
    main()