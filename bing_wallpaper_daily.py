import os
import requests
import json
import re

def get_image_info(url):
    try:
        response = requests.get(url)
        if 200 == response.status_code:
            data = json.loads(response.text)
            images = data['images'][0]
            return images
    except requests.ConnectionError:
        return None

def fetch_image(base_url, url_path, fullstartdate, image_path):
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    try:
        response = requests.get(base_url + url_path)
        if 200 == response.status_code:
            file_name = re.search(r'(?<=id\=).*?(?=\.jpg)',url_path).group()
            file_path = f'{image_path}/{fullstartdate}_{file_name}.jpg'
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(response.content)
            print(f'Downloaded image path is {file_path}')
        else:
            print(f'Already downloaded {file_path}')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    images = get_image_info('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')
    fetch_image('https://bing.com', images['url'], images['fullstartdate'], 'images')
