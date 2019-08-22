from __future__ import unicode_literals
import urllib.request
import urllib.parse
import re
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'downloading':
        print('Downloading in progress...')
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')



with open("muzyka.txt", 'r') as f:
    all_lines = f.readlines()
for line in all_lines:
    line = line.replace(' ', '+')
    line = line.replace('\n', '')
    query_string = urllib.parse.urlencode({"search_query" : line})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    if not search_results:
        continue
    else:
        a = "http://www.youtube.com/watch?v=" + search_results[0]
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([a])