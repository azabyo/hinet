#-*-coding:utf-8-*-

from module.clsHinet import *
import urllib2
import re

def main():
    URL="http://61.231.162.207" #한국
    URL="http://59.127.87.157" #중국
    URL="http://60.248.176.186" #중국
    URL="http://59.125.26.212" #중국
    URL="http://1.34.241.41"  #decode error
    # URL="http://59.115.12.245" #"error"
    # URL="http://60.248.111.206" #china
    # URL="http://1.164.138.22" #korea timedout
    # URL="http://1.164.137.150" #korea timedout
    # URL="http://1.162.118.43" #korea timedout
    # URL="http://1.160.7.124" #korea timedout
    # URL="http://1.160.11.246" #korea timedout
    # URL="http://1.173.27.182" #korea ok

    try:
        req = urllib2.Request(URL)
        res = urllib2.urlopen(req, timeout=3)
        rawdata = res.read()
    except Exception as ex:
        print ex
        exit(-1)
    try:
        rawdata = rawdata.decode('utf-8')
        hangul_reg = re.compile(u'[ㄱ-ㅣ가-힣]+')
        return_value = re.findall(hangul_reg,rawdata)
        for v in return_value:
            print v
        print "try ----"
    except UnicodeDecodeError as udex:
        hangul_reg = re.compile(u'[ㄱ-ㅣ가-힣]+')
        return_value = re.findall(hangul_reg,rawdata)
        for v in return_value:
            print v
        print "exception ----"
    except Exception as ex:
        print "exception ----"

if __name__ == "__main__":
    main()