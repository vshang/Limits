import os


dirs = ["2016", "2017", "2018", "2016_tDM", "2016_ttDM",  "2017_tDM", "2017_ttDM", "2018_tDM", "2018_ttDM"]
rep_strings = {"ttbar  ": "TTbarDL", "Drell_Yan ": "DYJetsToLL",  "Single_top": "ST        "}
for d in dirs:
     for _file in os.listdir(d):
         with open(os.path.join(d, _file)) as f:
             with open("tmp.txt", "w") as wf:
                 for line in f:
                     for finds, rep in rep_strings.items():
                         line = line.replace(finds, rep)
                     wf.write(line)
         os.replace("tmp.txt", os.path.join(d, _file))
