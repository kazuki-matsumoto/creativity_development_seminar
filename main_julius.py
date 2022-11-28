import socket
import re
import time
from led import Ws281x
from rpi_ws281x import Color, PixelStrip

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

led = Ws281x()

def fn_voice_recog():
	host = '127.0.0.1'   # IPアドレス
	port = 10500         # Juliusとの通信用ポート番号
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #juliusサーバに接続
	client.connect((host, port))

	time.sleep(3)

	re_word = re.compile('WORD="([^"]+)"')

	data = ""
	try:
		while True:
			while(data.find("</RECOGOUT>\n.") == -1):
				data += str(client.recv(1024).decode('shift_jis'))
				
			recog_text = "" # 単語を抽出
			for word in filter(bool, re_word.findall(data)):
				recog_text += word
					
			print("認識結果: " + recog_text)

			led.off()
			if recog_text == "スイッチオン。":
					led.on(0, 127, 0)
			elif recog_text == "スイッチオフ。":
					led.off()

			data = ""

	except:
		print('PROCESS END')
		client.send("DIE".encode('utf-8'))
		client.close()

fn_voice_recog()

# コマンドラインで実行
# julius -C main.conf -C am-gmm.conf -module -charconv utf-8 sjis

# 参考文献
# https://software-data-mining.com/python%E3%81%A8%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%83%95%E3%83%AA%E3%83%BC%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2julius%E3%81%AE%E9%80%A3%E6%90%BA%E3%81%AB%E3%82%88%E3%82%8B/

# https://www.matematetea.com/entry/2021/12/02/Python%E3%81%A7Julius%E3%82%92%E5%8B%95%E3%81%8B%E3%81%97%E3%81%A6%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F%EF%BC%81