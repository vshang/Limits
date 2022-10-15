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


dirs = ["2016", "2017", "2018", "2016_tDM", "2016_ttDM",  "2017_tDM", "2017_ttDM", "2018_tDM", "2018_ttDM"]
for d in dirs:
    for _file in os.listdir(d):
        with open(os.path.join(d, _file)) as f:
            ttbar_idxs = []
            lines = f.readlines()
            for line in lines:
                if line.startswith("process"):
                    if len(ttbar_idxs) == 0:
                        split = split_line(line)
                        ttbar_idxs = [i for i, strg in enumerate(split) if strg.startswith("TTbarDL")]
                    else:
                        split_nums = split_line(line)
                        ttbar_num = int(split_nums[ttbar_idxs[0]])

            block_num = 0
            with open("tmp.txt", "w") as wf:
                for line in lines:
                    if line.startswith("CMS_PS"):
                        split = split_line(line)
                        line = ""
                        for i, chunk in enumerate(split):
                            if i - 1 not in ttbar_idxs:
                                chunk = chunk.replace("1", "0")
                            line += chunk
                    wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
