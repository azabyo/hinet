#-*-coding:utf-8-*-
import urllib2
import json
import urllib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class telegram():
    def __init__(self, TOKEN=None, CHAT_ID=None):
 
        self.tg_token = TOKEN
        if (type(CHAT_ID == list)):
            self.chat_id_list = CHAT_ID
        else:
            self.chat_id_list = [CHAT_ID]
        self.api_url = r"https://api.telegram.org/bot"
        self.api_url = str(self.api_url) + str(self.tg_token)

    def send_telegram(self, send_text):
        send_url = "{}/sendMessage".format(self.api_url)

        for chat_id in self.chat_id_list:
            values = {
                "chat_id": chat_id,
                "text": send_text
            }

            http_hdr = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                'Content-Type': 'application/json'
            }
            try:
                req = urllib2.Request(send_url, json.dumps(values), headers = http_hdr)
                res = urllib2.urlopen(req)
            except Exception as ex:
                print ex

    def send_photo(self, photo, caption=None):
        send_url = "{}/sendPhoto".format(self.api_url)
        register_openers()
        with  open(photo, "rb") as f:      
            for chat_id in self.chat_id_list:
                values = {
                    "chat_id": chat_id,
                    "photo": f,
                    "caption" : caption
                }
                datagen, headers = multipart_encode({"chat_id": chat_id, "photo": f})

                try:
                    req = urllib2.Request(send_url, datagen, headers)
                    res = urllib2.urlopen(req)
                except Exception as ex:
                    print ex
