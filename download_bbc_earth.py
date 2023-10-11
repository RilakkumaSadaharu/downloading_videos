import os
import scrapetube
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from youtube_transcript_api import TranscriptsDisabled
import shutil
from http.client import IncompleteRead

# 先下载100个视频吧
i = 0
cnt = len(os.listdir('E:\\bbc_earth\\'))
if cnt<100: cnt=100
videos = scrapetube.get_channel("UCwmZiChSryoWQCZMIQezgTg")
for video in videos:
    if i >= 300:
        break
    i += 1
    # cnt = os.listdir('E:\\bbc_earth\\')
    if i <= cnt:
        continue
    vid = video['videoId']
    yt = YouTube('https://www.youtube.com/watch?v='+vid)
    title = yt.title.replace('?','').replace(':','').split('|')[0].strip()
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['en-GB','en'])
    except TranscriptsDisabled as e:
        print(e.CAUSE_MESSAGE)
    else:
        file_path = 'E:\\bbc_earth\\'+title
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
        os.mkdir(file_path)
        formatter = SRTFormatter()
        srt_formatted = formatter.format_transcript(transcript)
        with open('E:\\bbc_earth\\'+title+'\\'+title+'.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatted)
        try: 
            yt.streams.get_highest_resolution().download('E:\\bbc_earth\\'+title)
        except IncompleteRead as e:
            print(e)
        else:
            print(f'done... {title}')
