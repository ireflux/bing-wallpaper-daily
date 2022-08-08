import os
import requests
import json
import re

session = requests.Session()

class BingWallpaper:

    def __init__(self, base_url: str, headers: str, proxies: str) -> None:
        self.base_url = base_url
        self.headers = headers
        self.proxies = proxies

    def get_image(self, url):
        try:
            response = session.get(url, proxies = self.proxies, headers = self.headers)
            if 200 == response.status_code:
                data = json.loads(response.text)
                return data['images'][0]
        except requests.ConnectionError:
            return None

    def fetch_image(self, url_path, fullstartdate, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        try:
            response = session.get(self.base_url + url_path, proxies = self.proxies, headers = self.headers)
            if 200 == response.status_code:
                file_name = re.search(r'(?<=id\=).*?(?=\.jpg)',url_path).group()
                file_path = f'{folder_path}/{fullstartdate}_{file_name}.jpg'
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
                print(f'Downloaded image path is {file_path}')
            else:
                print(f'Already downloaded {file_path}')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    
    base_url = 'https://bing.com'
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    folder_path = './images'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    proxies = {}

    wallpaper = BingWallpaper(base_url, proxies, headers)
    image = wallpaper.get_image(url)
    wallpaper.fetch_image(image['url'], image['fullstartdate'], folder_path)
