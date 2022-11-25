
import socket
import re
import time


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
			data = ""

	except:
		print('PROCESS END')
		client.send("DIE".encode('utf-8'))
		client.close()

def julius_output():
	print("a")

fn_voice_recog()


# julius -C main.conf -C am-gmm.conf -module -charconv utf-8 sjis


# https://software-data-mining.com/python%E3%81%A8%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%83%95%E3%83%AA%E3%83%BC%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2julius%E3%81%AE%E9%80%A3%E6%90%BA%E3%81%AB%E3%82%88%E3%82%8B/

# https://www.matematetea.com/entry/2021/12/02/Python%E3%81%A7Julius%E3%82%92%E5%8B%95%E3%81%8B%E3%81%97%E3%81%A6%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F%EF%BC%81