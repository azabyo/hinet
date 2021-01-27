#!-*-coding:utf8-*-
import os
import re
import json
import datetime
from module.clsHinet import ROOT_PATH
from module.clsMaxmind import Maxmind
from module.clsElastic import MyElasticsearch

def main():
    regex = re.compile(r'<div class="text">.*', re.I)
    max_mind = Maxmind()
    

    for file_name in os.listdir(os.path.join(ROOT_PATH,"ChatExport_20_09_2019")):
        if file_name.endswith("html"):
            with open(os.path.join(ROOT_PATH,"ChatExport_20_09_2019", file_name), "r") as f:
                html_text = f.read()

            while True:
                class_text_idx = html_text.find('<div class="text">')
                class_text_end_idx = html_text[class_text_idx:].find("</div>") + class_text_idx
                if class_text_idx == -1:
                    break

                class_text_div = html_text[class_text_idx:class_text_end_idx]
                html_text = html_text[class_text_end_idx:]
                splited_class_text_div = class_text_div.split("<br>")
                if class_text_div.find("find apk URL") != -1:
                    try:
                        find_time = datetime.datetime.strptime(splited_class_text_div[1].split(" : ")[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
                        es_index = datetime.datetime.strftime(find_time, "{}%Y%m".format(PREFIX_IDX))
                        s_find_time = datetime.datetime.strftime(find_time, "%Y-%m-%dT%H:%M:%S.%f")
                        

                        raw_domain = splited_class_text_div[2].split(" : ")[1].strip()
                        domain_start_idx = raw_domain.find(">")+1
                        domain_end_idx = raw_domain[domain_start_idx:].find("<")+domain_start_idx
                        domain = raw_domain[domain_start_idx:domain_end_idx]

                        raw_uri = splited_class_text_div[4].split(" : ")[1].strip()
                        uri_start_idx = raw_uri.find(">")+1
                        uri_end_idx = raw_uri[uri_start_idx:].find("<")+uri_start_idx
                        uri = raw_uri[uri_start_idx:uri_end_idx].replace("./","/")

                        ip = domain.split("/")[2]
                    except IndexError as ex:
                        print splited_class_text_div
                        print ex
                        continue

                    result_max_mind = max_mind.getData(ip)

                    tmp_dict = { "av" : "malicious_apk", "data_source" : "malicious_apk_collector", "data_type" : "URL", "domain" : ip, "ip" : ip, "time_insert" : s_find_time, "time_source" : s_find_time, "url" : uri}
                    tmp_dict.update(result_max_mind)

                    # print tmp_dict
                    MyElasticsearch().putData(es_index, json.dumps(tmp_dict))

                

            # break



if __name__ == "__main__":
    main()