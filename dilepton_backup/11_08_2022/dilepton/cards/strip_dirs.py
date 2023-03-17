import os


dirs = ["2016", "2017", "2018", "2016_tDM", "2016_ttDM",  "2017_tDM", "2017_ttDM", "2018_tDM", "2018_ttDM"]
files = ["full_run2_scalar.txt", "full_run2_pseudo.txt", "full_run2_scalar_ttDM.txt", "full_run2_pseudo_ttDM.txt", "full_run2_scalar_tDM.txt", "full_run2_pseudo_tDM.txt"] 
for _file in files:
    with open(_file) as f:
        with open("tmp.txt", "w") as wf:
            for line in f:
                for finds in dirs:
                    line = line.replace(finds + "/..", "..")
                wf.write(line)
    os.replace("tmp.txt", _file)
