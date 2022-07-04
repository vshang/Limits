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
                    if line.startswith("---"):
                        block_num += 1
                    if block_num == 3:
                        split = split_line(line)
                        line = ""
                        for i, chunk in enumerate(split):
                            if chunk[0].isdigit():
                                if int(chunk[0]) > ttbar_num:
                                    chunk = str(int(chunk[0]) + 1) + chunk[1:]
                                if i in ttbar_idxs:
                                    chunk = chunk + str(int(chunk[0]) + 1) + chunk[1:]
                            elif i in ttbar_idxs:
                                if chunk.startswith("TTbarDL"):
                                    chunk += "TTbarSL" + chunk[7:]
                                else:
                                    chunk += chunk
                            line += chunk
                    elif block_num == 4 and not line.startswith("ttz_norm"):
                        split = split_line(line)
                        line = ""
                        for i, chunk in enumerate(split):
                            if i - 1 in ttbar_idxs:
                                chunk += chunk
                            line += chunk
                    wf.write(line)
                    if line.startswith("QCDScale_TTbarDL"):
                        line = "QCDScale_TTbarSL" + line[16:]
                        wf.write(line)
        os.replace("tmp.txt", os.path.join(d, _file))
