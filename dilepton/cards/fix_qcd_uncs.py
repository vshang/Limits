import os

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
starts = ["top_mass"]
for d in dirs:
    for _file in os.listdir(d):
        with open(os.path.join(d, _file)) as f:
            ttbar_idxs = []
            lines = f.readlines()
            for line in lines:
                if line.startswith("process"):
                    if len(ttbar_idxs) == 0:
                        split = split_line(line)
                        ttbar_idxs = [i for i, strg in enumerate(split) if strg.startswith("TTbarSL")]
                    else:
                        split_nums = split_line(line)
                        ttbar_num = int(split_nums[ttbar_idxs[0]])

            with open("tmp.txt", "w") as wf:
                for line in lines:
                    for start in starts:
                        if line.startswith(start) and not line.startswith("CMS_scale_pu"):
                            split = split_line(line)
                            line = ""
                            for i, chunk in enumerate(split):
                                if i - 1 in ttbar_idxs:
                                    chunk = "0   " + chunk[4:]
                                line += chunk
                    wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
