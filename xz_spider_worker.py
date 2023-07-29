import requests
from bs4 import BeautifulSoup
import html2text
import os
import config


class XzSpiderWorker:
    markdown_content = ''

    def __init__(self, url, save_path):
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        self.save_path = save_path
        self.url = url

    def work(self):
        html_content = requests.get(self.url).text

        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string
        topic_content = soup.find(class_='topic-content markdown-body')

        # convert
        self.markdown_content = html2text.html2text(str(topic_content))

        dirname = os.path.join(self.save_path, title)
        # Check if the folder exists
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        # Download and replace image URLs in the Markdown content
        for img in soup.find_all('img'):
            img_url = img['src']
            img_filename = img_url.split('/')[-1]
            img_data = requests.get(img_url, headers=config.IMAGE_HEADERS).content
            img_markdown_path=os.path.join( title, img_filename)
            img_filename = os.path.join(self.save_path, img_markdown_path)
            with open(img_filename, 'wb') as f:
                f.write(img_data)
            self.markdown_content = self.markdown_content.replace(img_url, img_markdown_path)
            markdown_filename = os.path.join(self.save_path, title + '.md')
            # Save the Markdown content to a file
            with open(markdown_filename, 'w', encoding='utf-8') as f:
                f.write(self.markdown_content)
if __name__ == '__main__':
    spider= XzSpiderWorker('https://xz.aliyun.com/t/12691','aliyun')
    spider.work()