# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://finance.sina.com.cn/stock/relnews/2024-04-03/doc-inaqnzxy4323607.shtml
import requests
from bs4 import BeautifulSoup
from ocr.extract_video import extract_video
from ocr.extract_pic import extract_pic
from ocr.extract_docx import extract_docx
from utils import write_txt,read_txt,make_dir
import os,shutil
import jieba.analyse
import pandas as pd
import argparse
jieba.analyse.set_stop_words("stopwords.txt")

hd = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

print("start")
# ---爬取视频网址
# url = 'http://photovideo.photo.qq.com/1075_0b2eywbeqqyatmahv3a5bvpdhriejcuaavsa.f0.mp4?dis_k=ea9081c375c9565e1bad4d841052ee40&dis_t=1579245843&vuin=1132600941&save=1&d=1'

# r = requests.get(url, headers=hd, stream=True)

# with open('test.mp4', "wb") as mp4:
#     for chunk in r.iter_content(chunk_size=1024 * 1024):
#         if chunk:
#             mp4.write(chunk)
#
# print("end")
#---

#爬取文字-图片

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def read_static_news(dir_path):
    docx_text_list=[]
    pic_text_list=[]
    for file in os.listdir(dir_path):
        print(file)
        if file.split(".")[-1]=="jpg":
            img_path=dir_path+"/"+file
            pic_text_list.extend(extract_pic(img_path))
        elif file.split(".")[-1]=="docx":
            docx_path=dir_path+"/"+file
            docx_text_list.extend(extract_docx(docx_path))
        return ",".join(docx_text_list),",".join(pic_text_list)

def extract_static_news(static_dir,extracted_static_dir):
    for dir_name in os.listdir(static_dir):
        docx_string,pic_string=read_static_news(static_dir+"/"+dir_name)
        if len(docx_string)!=0 or len(pic_string)!=0:
            static_string=docx_string+";"+pic_string
            extracted_file_name=dir_name+".txt"
            write_txt(extracted_static_dir+"/"+extracted_file_name,static_string)

def nlp_txt(extracted_news_dir_list,tgt_news_root_dir):
    #key_dict是个字典，字典里的key是关键字，value是关键字提到数量
    key_dict={}
    for extracted_news_dir in extracted_news_dir_list:
        for file in os.listdir(extracted_news_dir):
            raw_file_path=extracted_news_dir+"/"+file
            raw_text=read_txt(raw_file_path)
            key_res=jieba.analyse.extract_tags(raw_text,withWeight=True,topK=3)   #返回TF-IDF权重值
            if len(key_res)!=0:
                for i in range(len(key_res)):
                    key_word=key_res[i][0]
                    if key_word.isdigit() or key_word.encode("utf8").isalpha():
                        print("纯数字，或纯英文的关键字{}".format(key_word))
                    else:
                        key_info=key_dict.get(key_word,[0])
                        #更新关键字数量信息
                        cnt=key_info[0]
                        cnt=cnt+1
                        key_info[0]=cnt
                        # 创建这个关键字的文件夹
                        tgt_news_dir=tgt_news_root_dir+"/"+key_res[i][0]
                        make_dir(tgt_news_dir)
                        # 如果抽取的新闻是静态新闻
                        if extracted_news_dir.split("/")[-1]=="static_news":
                            static_news_name="".join(file.split(".")[:-1])
                            src_news_dir=static_dir+"/"+static_news_name
                            tgt_files_dir=tgt_news_dir+"/"+static_news_name
                            if not os.path.exists(tgt_news_dir+"/"+static_news_name):
                                # 将原文件夹复制到这个关键字文件夹下
                                shutil.copytree(src_news_dir,tgt_files_dir)
                            key_info.append(tgt_files_dir)
                        #如果抽取的新闻是视频新闻
                        elif extracted_news_dir.split("/")[-1]=="video_news":
                            mp4_news_name="".join(file.split(".")[:-1])+".mp4"
                            src_video_news=video_dir+"/"+mp4_news_name
                            if not os.path.exists(tgt_news_dir+"/"+mp4_news_name):
                                shutil.copy(src_video_news,tgt_news_dir)
                            key_info.append(tgt_news_dir+"/"+mp4_news_name)
                        shutil.copy(raw_file_path,tgt_news_dir)
                        key_dict[key_word]=key_info
    return key_dict
def dict_to_dataframe(key_dict):
    key_word_list=[]
    key_word_cnt_list=[]
    key_word_dir_list=[]
    for key_word,key_info in key_dict.items():
        for i in range(1,len(key_info)):
            key_word_list.append(key_word)
            key_word_cnt_list.append(key_info[0])
            key_word_dir_list.append(key_info[i])
    key_df = pd.DataFrame(list(zip(key_word_list, key_word_cnt_list, key_word_dir_list)),
                          columns=['关键字', '数量', '新闻路径'])
    return key_df
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # video_dir = "toutiao/今日头条/video_news"
    # extracted_video_dir = "toutiao/今日头条/extracted/video_news"
    # static_dir="toutiao/今日头条/static_news"
    # extracted_static_dir="toutiao/今日头条/extracted/static_news"
    # tgt_news_root_dir = "category_news"
    # extracted_news_dir_list = [extracted_static_dir,extracted_video_dir]

    parser=argparse.ArgumentParser()
    parser.add_argument("--video_dir",type=str,default="toutiao/今日头条/video_news")
    parser.add_argument("--extracted_video_dir",type=str,default="toutiao/今日头条/extracted/video_news")
    parser.add_argument("--static_dir",type=str,default="toutiao/今日头条/static_news")
    parser.add_argument("--extracted_static_dir",type=str,default="toutiao/今日头条/extracted/static_news")
    video_dir = parser.parse_args().video_dir
    extracted_video_dir = parser.parse_args().extracted_video_dir
    static_dir=parser.parse_args().static_dir
    extracted_static_dir=parser.parse_args().extracted_static_dir
    tgt_news_root_dir = "category_news"
    extracted_news_dir_list = [extracted_static_dir,extracted_video_dir]


    #----------读取视频信息

    print("aaa{}".format(video_dir))
    for video_name in os.listdir(video_dir):
        if video_name.split(".")[-1]=="mp4":
            video_file_path=video_dir+"/"+video_name
            video_res=extract_video(video_file_path)
            if video_res is not None:
                extracted_file_name=video_name[:-4]+".txt"
                print("视频新闻写入路径")
                print(extracted_video_dir+"/"+extracted_file_name)
                write_txt(extracted_video_dir+"/"+extracted_file_name,video_res)
    # ---------------------------
    #读取静态文件信息
    extract_static_news(static_dir, extracted_static_dir)
    # nlp,从txt中分析文本,提取关键字
    key_dict=nlp_txt(extracted_news_dir_list,tgt_news_root_dir)
    key_df=dict_to_dataframe(key_dict)
    key_df.to_csv("关键字信息表.csv", encoding="utf8")
    # ----------新词发现
    new_word_list=[]
    # 载入本地词典
    f=open("extra_dict/idf.txt", encoding='utf8',errors="ignore")
    exist_words=[]
    for line in f:
        exist_words.append(line.strip())
    f.close()
    # 发现新词
    for key_word in key_dict.keys():
        if key_word not in exist_words:
            print("发现新词{}".format(key_word))
            new_word_list.append(key_word)
    # 写入新词表
    with open("新词表.txt", 'w',encoding="gbk",errors="ignore") as f:
        f.write(",".join(new_word_list))
    # 将新词添加到本地词典
    for key_word in new_word_list:
        with open("extra_dict/idf.txt", 'a',encoding="utf8") as f:
            f.write(key_word+"\n")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
