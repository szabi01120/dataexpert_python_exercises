import json
from PIL import Image
import urllib.request as urllib
from urllib.request import urlopen
import os

DOWNLOAD_PATH = 'pictures/'

def open_file():
    with open('earthporn.json', 'r') as f:
        data = json.load(f)
    f.close()
    return data

def get_url(data):
    url_list = []
    
    for i in data['data']['children']:
        url_list.append(i['data']['url'])
    return url_list

def open_urls(url_list):
    opened = len(url_list)
    for i in url_list:
        try:
            with urlopen(i):
                img = Image.open(urlopen(i))
                print(f"{i}\n{img.format} {img.size}")
                
                if not os.path.exists(DOWNLOAD_PATH + i.split('/')[-1]):
                    img.save(DOWNLOAD_PATH + i.split('/')[-1])
                else:
                    print(f"Already downloaded {i}")
        except Exception as e:
            print(f"Error for {i}: {e}")
            opened -= 1

    print('Opened {} images'.format(opened))

def main():
    data = open_file()
    url = get_url(data)
    open_urls(url)
    
if __name__ == '__main__':
    main()