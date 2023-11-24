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


dirs = ["2016", "2017", "2018", "2016_tDM", "2016_ttDM",  "2017_tDM", "2017_ttDM", "2018_tDM", "2018_ttDM"]
for d in dirs:
    for _file in os.listdir(d):
        with open(os.path.join(d, _file)) as f:
            SLidxs = []
            lines = f.readlines()
            block_num = 0
            with open("tmp.txt", "w") as wf:
                for line in lines:
                    if line.startswith("process") and len(SLidxs) == 0:
                        splits = [s for s in line.split(" ") if s != ""]
                        SLidxs = np.where(np.array(splits) == "TTbarSL")[0]
                    if line.startswith("QCDScale"):
                        sysname = line.split(" ")[0]
                        samp = sysname.split("_")[1]
                        if samp == "TTbarDL":
                            newline = ""
                            i = 0
                            for c in line:
                                if c == "0" or c == "1":
                                    i += 1
                                    if i in SLidxs:
                                        c = "1"
                                newline += c
                            wf.write(newline.replace(sysname, "QCDScale_ren_TT "))
                            wf.write(newline.replace(sysname, "QCDScale_fac_TT "))
                        elif samp == "tDM":
                            wf.write(line)
                        elif samp != "TTbarSL":
                            wf.write(line.replace(sysname + "    ", "QCDScale_ren_" + samp))
                            wf.write(line.replace(sysname + "    ", "QCDScale_fac_" + samp))
                    else:
                        wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
