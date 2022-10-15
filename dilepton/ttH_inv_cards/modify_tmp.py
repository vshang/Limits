import os
import numpy as np

def split_line(line):
    ret = []
    start = 0
    counting_zeros = False
    for idx, char in enumerate(line):
        if char == " ":
            counting_zeros = True
        if counting_zeros and char != " ":
            counting_zeros = False
            ret.append(line[start:idx])
            start = idx
    ret.append(line[start:])
    return ret


dirs = ["2016", "2017", "2018"]
for d in dirs:
    for _file in os.listdir(d):
        with open(os.path.join(d, _file)) as f:
            SLidxs = []
            lines = f.readlines()
            block_num = 0
            with open("tmp.txt", "w") as wf:
                for line in lines:
                    if line.startswith("ttH_HToInv_xsec"):
                        wf.write(line.replace("1.3        ", "1.058/0.908"))
                    else:
                        wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
