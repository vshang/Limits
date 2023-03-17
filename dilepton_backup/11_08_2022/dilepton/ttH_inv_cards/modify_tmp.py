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
    #for _file in os.listdir(d):
    with open(os.path.join(d, "DL_ttZCR.txt")) as f:
        lines = f.readlines()
        with open("tmp.txt", "w") as wf:
            for line in lines:
                if line.startswith("CMS_scale_pu"):
                    wf.write(line)
                    wf.write(line.replace("CMS_scale_pu         ", "CMS_eff_dilep_trigger"))
                else:
                    wf.write(line)
    os.replace("tmp.txt", os.path.join(d, "DL_ttZCR.txt"))
