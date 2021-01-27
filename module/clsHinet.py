#-*-coding:utf-8-*-
import os
import socket
import struct
import urllib2
from multiprocessing import Pool
from pyquery import PyQuery as pq
import datetime
from clsTelegram import telegram
from selenium import webdriver
import re
import logging
import json
from Util import mkMSG
from clsElastic import MyElasticsearch
from clsMaxmind import Maxmind


ROOT_PATH = os.path.dirname(os.path.join("..",os.path.dirname(__file__)))
ANDROID_UAG = "Mozilla/5.0 (Linux; Android 4.4.2; sdk Build/KK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36"

hinet_logger = logging.getLogger("hinet")
hinet_logger.setLevel(logging.DEBUG)
fomatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(fomatter)

file_handler = logging.FileHandler(os.path.join(ROOT_PATH, "hinet.log"))
file_handler.setFormatter(fomatter)
hinet_logger.addHandler(file_handler)
hinet_logger.addHandler(stream_handler)

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def checkHangul(rawdata):
    try:
        rawdata = rawdata.decode('utf-8')
        hangul_reg = re.compile(u'[ㄱ-ㅣ가-힣]+')
        return_value = re.findall(hangul_reg,rawdata)
        if len(return_value) > 0:
            return True
        return False
    except UnicodeDecodeError as udex:
        hangul_reg = re.compile(u'[ㄱ-ㅣ가-힣]+')
        return_value = re.findall(hangul_reg,rawdata)
        if len(return_value) > 0:
            return True
        return False
    except Exception as ex:
        hinet_logger.error("checkHangul function ex : {}".format(ex))
        return False

class Hinet(object):
    BOT_ID = "95552206:AAHLr6pOTz4QWjRIIHuf0GcsdX0_P2e2EyI"
    CHAT_ID = [-1001282068082]

    def __init__(self, proc_cnt=10):
        hinet_logger.info("{} init".format(self.__class__.__name__))
        self.iprange = list()
        self.proc_cnt = proc_cnt
        self.opend_host = list()
        self.has_apk_host = list()
        # self.f = open(os.path.join(ROOT_PATH,"result.txt"), "a")
        
    def __del__(self):
        # self.f.close()
        pass

    def read_hinet_range(self):
        filename = os.path.join(ROOT_PATH, "hinet_ip_range.txt")
        if not os.path.exists(filename):
            hinet_logger.debug("file not found")
            return False
        with open(filename, "r") as f:
            hinet_raw_data = f.read()

        for line in hinet_raw_data.split("\n"):
            start_idx = line.find("'")
            end_idx = line.find(" - ")
            first_ip = line[start_idx+1:end_idx]
            second = line[end_idx+len(" - "):]
            s_end_idx = second.find("'")
            second_ip = second[:-1]
            self.iprange.append([first_ip, second_ip])
        return True

    def getUrls(self):
        p = Pool(self.proc_cnt)
        results = p.map(getUrl, self.opend_host)
        self.has_apk_host += [result for result in results if result is not None]
        p.close()

def port_scan(iprange, proc_cnt=3):
    start_idx = ip2int(iprange[0])
    end_idx = ip2int(iprange[1])   
    ip_range = range(start_idx, end_idx+1)
    p = Pool(proc_cnt)
    results = p.map(port_scan_proc, ip_range)
    # self.opend_host += [result for result in results if result is not None]
    # self.has_apk_host += [result for result in results if result is not None]
    p.close()

def getUrl(host):
    tg = telegram(Hinet.BOT_ID, Hinet.CHAT_ID)
    my_ela = MyElasticsearch()
    max_mind = Maxmind()
    try:
        req = urllib2.Request("http://{}".format(host))
        req.add_header("User-agent", ANDROID_UAG)
        res = urllib2.urlopen(req, timeout=3)
        raw_data = res.read()
        if checkHangul(raw_data):
            pq_a_list = pq('a', raw_data)
            if len(pq_a_list) > 0:
                for a_link in pq_a_list:
                    href = pq(a_link).attr("href")
                    if href is not None:
                        if href.lower().find(".apk") != -1:
                            hinet_logger.debug("find apk URL http://{}".format(host))
                            with open(os.path.join(ROOT_PATH, "result.txt"), "a") as f:
                                f.write("find apk URL http://{}\n".format(host))
                            
                            replaced_host = host.replace(".","_")
                            today_dir = os.path.join(ROOT_PATH, "RESULT", str(datetime.datetime.now().date()), replaced_host)

                            if save_html(replaced_host, raw_data, today_dir):
                                hinet_logger.info("{} save_html success".format(host))

                            if href.find("http") != 0:
                                fullurl_href = "http://{}/{}".format(host, href)
                            else:
                                fullurl_href = href

                            if save_apk(today_dir, fullurl_href):
                                hinet_logger.info("{} save_apk success".format(fullurl_href))
                                apk_filename = fullurl_href.split("/")[-1]
                                tg.send_telegram(mkMSG(host, fullurl_href, today_dir))

                                es_index = datetime.datetime.strftime(datetime.datetime.now(), "{}%Y%m".format(MyElasticsearch.PREFIX_IDX))
                                s_find_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S.%f")
                                try:
                                    
                                    tmp_dict = { "av" : "malicious_apk", "data_source" : "malicious_apk_collector", "data_type" : "URL", "domain" : host, "ip" : host, 
                                    "time_insert" : s_find_time, "time_source" : s_find_time, "url" : fullurl_href}
                                    tmp_dict.update(max_mind.getData(host))

                                    es_result = my_ela.putData(es_index, json.dumps(tmp_dict))
                                    hinet_logger.info("create document success : {}".format(es_result))
                                except Exception as ex:
                                    hinet_logger.error("create document exception : {}".format(ex))

                                if save_screenshot("http://{}/".format(host), today_dir, replaced_host):
                                    tg.send_photo(os.path.join(today_dir, "{}.png".format(replaced_host)))
                                    pass
                            
                            return host
        return None
    except Exception as ex:
        hinet_logger.error("{}:{}".format(host, ex))
        return None

def save_html(replaced_host, response, today_dir):
    if not os.path.exists(today_dir):
        os.makedirs(today_dir)
    try:
        with open(os.path.join(today_dir, replaced_host+".html"), "w") as f:
            f.write(response)
        return True
    except Exception as ex:
        hinet_logger.error("save_html: exception {}".format(ex))
        return False

def save_apk(today_dir, apk_url):
    try:
        req = urllib2.Request(apk_url)
        req.add_header("User-agent", ANDROID_UAG)
        res = urllib2.urlopen(req)
        raw_data = res.read()
        apk_filename = apk_url.split("/")[-1]
        with open(os.path.join(today_dir, apk_filename), "wb") as f:
            f.write(raw_data)
        return True
    except Exception as ex:
        hinet_logger.error("save apk exception {}".format(ex))
        return False

def save_screenshot(url, today_dir, replaced_host):
    hinet_logger.debug("save screenshot start : {}".format(url))
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--user-agent={}".format(ANDROID_UAG))
    with webdriver.Chrome(os.path.join(ROOT_PATH,"chromedriver"), chrome_options=options) as driver:
        try:
            driver.get(url)
            total_width = driver.execute_script("return document.body.scrollWidth")
            total_height = driver.execute_script("return document.body.scrollHeight")
            print "width : {}, height : {}".format(total_width, total_height)
            driver.set_window_size(total_width, total_height)
            driver.save_screenshot(os.path.join(today_dir, "{}.png".format(replaced_host)))
            return True
        except Exception as ex:
            hinet_logger.error("exception save screenshot : {} => {}".format(replaced_host, ex))
            return False

def port_scan_proc(addr):
    try:
        host = int2ip(addr)
    except Exception as ex:
        hinet_logger.debug(ex)
    port = 80
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        hinet_logger.debug("{} : {} opened".format(host, port))
        # with open(os.path.join(ROOT_PATH, "result.txt"), "a") as f:
        #     f.write("find apk URL http://{}\n".format(host))
        return getUrl(host) 
    except Exception as ex:
        hinet_logger.debug("port scan proc ex => {} : {}".format(host, ex))
        pass
