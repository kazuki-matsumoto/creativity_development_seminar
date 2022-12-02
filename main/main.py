import cv2
import os
from deepface import DeepFace
import matplotlib.pyplot as plt
from led import Ws281x
from rpi_ws281x import Color, PixelStrip
from concurrent.futures import ProcessPoolExecutor


LED_COUNT = 6  # Number of LED pixels.
LED_PIN = 21  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STATE_OFF = Color(0, 0, 0)  # OFF


class Ws281x:
    def __init__(self):
        self.__strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        self.__strip.begin()

    def on(self, red: int, green: int, blue: int) -> None:
        color = Color(red, green, blue)
        for i in range(self.__strip.numPixels()):
            self.__strip.setPixelColor(i, color)
            self.__strip.show()

    def off(self) -> None:
        for i in range(self.__strip.numPixels()):
            self.__strip.setPixelColor(i, LED_STATE_OFF)
            self.__strip.show()


def faceReco() -> None:
    led = Ws281x()
     
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
                
                # print(type(cut_frame))

                #plt.imshow(cut_frame[:,:,::-1])
                #plt.show()
                #print(cut_frame)

                result = DeepFace.analyze(cut_frame, actions=['emotion'], enforce_detection=False)

                print(result)
                face = [k for k, v in result["emotion"].items() if v == max(result["emotion"].values())][0]
                print("face :",face)
                print(type(face))
                print(face == "neutral")
                
                led.off()
                if face == "neutral":
                    led.on(127, 0, 0)
                else:
                    led.off()              


        # フレームの描画
        cv2.imshow('frame', frame)
     
        # qキーの押下で処理を中止
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
     
    #メモリの解放
    video.release()
    cv2.destroyAllWindows()


def say_hello() -> None:
    print("hello!!!")   


#faceReco()

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers = 2) as executor:
        executor.submit(faceReco)
        executor.submit(say_hello)
