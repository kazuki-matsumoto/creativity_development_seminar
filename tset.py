
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

	except KeyboardInterrupt:
	    print('PROCESS END')
      client.send("DIE".encode('utf-8'))
      client.close()
	    
if __name__ == '__main__':
	fn_voice_recog()