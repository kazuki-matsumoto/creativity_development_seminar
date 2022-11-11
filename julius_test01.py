import socket
import time
import re

# ローカル環境のIPアドレス
host = '127.0.0.1'
# Juliusとの通信用ポート番号
port = 10500

# Juliusにソケット通信で接続
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
time.sleep(2)

# 正規表現で認識された言葉を抽出
extracted_word = re.compile('WORD="([^"]+)"')
data = ""

try:
    while True:
        while (data.find("</RECOGOUT>\n.") == -1):
            data += str(client.recv(1024).decode('shift_jis'))

        # 単語を抽出
        recog_text = ""
        for word in filter(bool, extracted_word.findall(data)):
            recog_text += word

        # 単語を表示
        print("認識結果: " + recog_text)

        if recog_text == 'ライトオン。':
          print("ぴかー")
        if recog_text == 'ライトオフ。':
          print("消える")

        data = ""

except:
    print('PROCESS END')
    client.send("DIE".encode('shift_jis'))
    client.close()

# https://www.matematetea.com/entry/2021/12/02/Python%E3%81%A7Julius%E3%82%92%E5%8B%95%E3%81%8B%E3%81%97%E3%81%A6%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F%EF%BC%81