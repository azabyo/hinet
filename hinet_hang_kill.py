#-*-coding:utf-8-*-
import psutil
import os
import datetime
import time

def main():
    with open("/tmp/hinet.pid", "r") as f:
        hinet_pid = int(f.read())

    current_process = psutil.Process(hinet_pid)
    children = current_process.children(recursive=True)
    for child in children:
        # print child.pid, datetime.datetime.strftime("%Y-%m-%d %H:%M:%S", child.create_time())
        # ctime = datetime.datetime.strftime("%Y-%m-%d %H:%M:%S", time.localtime(child.create_time()))
        ctime = datetime.datetime.fromtimestamp(child.create_time())
        print child.pid, datetime.datetime.now() - ctime
        # child.kill()

if __name__ == "__main__":
    main()