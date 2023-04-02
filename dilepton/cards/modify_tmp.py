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
            lines = f.readlines()
            with open("tmp.txt", "w") as wf:
                for line in lines:
                    if line.startswith("top_pt_rwght"):
                        wf.write(line)
                        wf.write(line.replace("top_pt_rwght",
                                              "top_mass    ").replace("1   ", "0.33"))
                    else:
                        wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
