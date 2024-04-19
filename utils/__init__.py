import os
def write_txt(file_name,write_string):
    with open(file_name, 'w',encoding="gbk",errors="ignore") as f:
        f.write(write_string)
def read_txt(file_name):
    f=open(file_name, encoding='gbk',errors="ignore")
    txt=[]
    for line in f:
        txt.append(line.strip())
    return ",".join(txt)

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("{}Folder created".format(path))
    else:
        print("{}Folder already exists".format(path))
