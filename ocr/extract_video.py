import moviepy.editor as mp
import whisper,os
from opencc import OpenCC

# video_dir="toutiao/今日头条/video_news"
# extracted_video_dir="toutiao/今日头条/extracted/video_news"
audio_model = whisper.load_model("base")
cc = OpenCC('t2s')

def extract_audio(video_file_path):
    my_clip = mp.VideoFileClip(video_file_path)
    my_clip.audio.write_audiofile(f'{video_file_path}.mp3')

def extract_video(video_file_path):
    extract_audio(video_file_path)
    result = audio_model.transcribe(f'{video_file_path}.mp3', language="zh")
    res = cc.convert(result['text'])


# for video_name in os.listdir(video_dir):
#     if video_name.split(".")[-1]=="mp4":
#         video_file_path=video_dir+"/"+video_name
#         extract_audio(video_file_path)
#         result = audio_model.transcribe(f'{video_file_path}.mp3',language="zh")
#         res=cc.convert(result['text'])
#         extracted_file_name=video_name[:-4]+".txt"
#         print(extracted_file_name)
#         write_txt(extracted_video_dir+"/"+extracted_file_name,res)