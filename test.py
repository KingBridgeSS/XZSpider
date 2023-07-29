import requests
from bs4 import BeautifulSoup
import html2text
import os


def convert_html_to_markdown(url):
    # Download the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    title=soup.title.string
    # Find the element with class name 'topic-content markdown-body'
    topic_content = soup.find(class_='topic-content markdown-body')

    # Convert HTML to Markdown
    markdown_content = html2text.html2text(str(topic_content))
    # Check if the folder named 'title' exists
    if not os.path.exists(title):
        os.mkdir(title)
    # Download and replace image URLs in the Markdown content
    for img in soup.find_all('img'):
        img_url = img['src']
        img_filename = img_url.split('/')[-1]
        burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "https://xz.aliyun.com/", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6"}
        img_data=requests.get(img_url, headers=burp0_headers).content
        # img_data = requests.get(img_url).content


        img_filename=os.path.join(title,img_filename)
        with open(img_filename, 'wb') as f:
            f.write(img_data)
        markdown_content = markdown_content.replace(img_url, img_filename)

    # Save the Markdown content to a file
    with open(title+'.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print('Conversion complete. Markdown content saved to output.md')


if __name__ == '__main__':
    # url = input('Enter the URL: ')
    url='https://xz.aliyun.com/t/12691'
    convert_html_to_markdown(url)
