#-*-coding:utf-8-*-
from module.clsHinet import ROOT_PATH, Hinet, getUrl, port_scan
from multiprocessing import Process
import os

def checkPID(pid_file):
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            return int(f.read())
    return None

def main():
    pid_file = "/tmp/{}.pid".format(os.path.splitext(os.path.basename(__file__))[0])
    with open(pid_file , "w") as f:
        f.write(str(os.getpid()))

    MAX_PROC = 5
    hinet = Hinet(50)
    if hinet.read_hinet_range():                                        
        k = 0
        for iprange_idx in range(0, len(hinet.iprange), MAX_PROC):
            j = iprange_idx
            if iprange_idx+iprange_idx > len(hinet.iprange):
                k = len(hinet.iprange)
            else:
                k = iprange_idx+iprange_idx

            procs = list()
            for iprange in hinet.iprange[j:k-1]:
                proc = Process(target=port_scan, args=(iprange, 1))
                procs.append(proc)
                proc.start()

            for proc in procs:
                proc.join()
                

if __name__ == "__main__":
    while True:
        main()
