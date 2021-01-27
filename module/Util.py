#-*-coding:utf-8-*-
import hashlib
import os
import datetime

def getHash(fname, hash_type="md5"):
    get_hash = getattr(hashlib, hash_type)
    myhash = get_hash()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            myhash.update(chunk)
    return myhash.hexdigest()

def mkMSG(host, fullurl_href, today_dir):
    replaced_host = host.replace(".","_")
    apk_filename = fullurl_href.split("/")[-1]
    html_hash = getHash(os.path.join(today_dir, "{}.html".format(replaced_host)))
    apk_hash = getHash(os.path.join(today_dir, "{}".format(apk_filename)))
    return "find apk URL \n 탐지 시간 : {} \n 유포 도메인 : http://{} \n 도메인 HTML 해시 (MD5) : {} \n APK LINK : {} \n APK 해시 (MD5) : {}".format(datetime.datetime.now(), host, html_hash, fullurl_href, apk_hash)