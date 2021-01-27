#-*-coding:utf8-*-
import os
import json
import urllib2

ROOT_PATH = os.path.dirname(os.path.join("..",os.path.dirname(__file__)))

class MyElasticsearch(object):
    PREFIX_IDX = "hacking_url_c2_"

    def __init__(self):
        self.host = "10.250.252.103"
        self.port = 9200

    def chkIndex(self, _index):
        try:
            req = urllib2.Request("http://{}:{}/{}".format(self.host, self.port, _index))
            req.add_header("content-type","application/json")
            res = urllib2.urlopen(req)
            return True
        except Exception as ex:
            return False

    def mkMapping(self, _index):
        try:
            with open(os.path.join(ROOT_PATH, "data", "hacking_url_c2_mapping.json"), "r") as f:
                mapping_info = f.read()
        except Exception as ex:
            return False

        try:
            req = urllib2.Request("http://{}:{}/{}".format(self.host, self.port, _index))
            req.add_header("content-type", "application/json")
            req.get_method = lambda: "PUT"
            res = urllib2.urlopen(req, data = mapping_info)
            return True
        except Exception as ex:
            print ex
            return False

        print loaded_mapping

    def deleteIndex(self, _index):
        try:
            req = urllib2.Request("http://{}:{}/{}".format(self.host, self.port, _index))
            req.add_header("content-type", "application/json")
            req.get_method = lambda: "DELETE"
            res = urllib2.urlopen(req)
            return True
        except Exception as ex:
            return False        

    def putData(self, _index, _data):
        print "putData"
        print _index
        if self.chkIndex(_index) is False:
            if self.mkMapping(_index) is False:
                print "if if"
                return False

        try:
            req = urllib2.Request("http://{}:{}/{}/_doc/".format(self.host, self.port, _index))
            req.add_header("content-type", "application/json")
            req.get_method = lambda: "POST"
            res = urllib2.urlopen(req, data= _data)
            print res.read()
            return True
        except Exception as ex:
            print _index
            print _data
            print ex
            return False
