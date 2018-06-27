#import urllib.request


#urllib.request.urlretrieve("https://video.xx.fbcdn.net/v/t42.9040-2/10000000_241375296434687_6804312160710164480_n.mp4?_nc_cat=0&efg=eyJybHIiOjE1MDAsInJsYSI6NDA5NiwidmVuY29kZV90YWciOiJzdmVfaGQifQ%3D%3D&rl=1500&vabr=638&oh=f0f72aa9ad3fae24ef36430edd1a25a6&oe=5B31D94A", 'video_name.mp4')

import requests
import sys

def download (link, file_name):
    with open(file_name, "wb") as f:
        print ("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')


        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s] %i%%" % ('=' * done, ' ' * (50-done), 2*done) )
                sys.stdout.flush()
    print ("done")
