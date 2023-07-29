import os.path
import sys

import requests
from bs4 import BeautifulSoup
from loguru import logger
import shutil
import json
import config
from tqdm import tqdm

def get_total_page() -> int:
    r = requests.get(config.BASE_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_div = soup.find('div', {'class': 'pagination clearfix'})
    page_link = page_div.find('a', {'class': 'active'})
    total_page = int(page_link.text.split('/')[1])
    logger.info("total page: " + str(total_page))
    return total_page


def get_all_url_list(total_page) -> list:
    url_list = []
    for page_index in tqdm(range(total_page)):
        real_page_index = page_index + 1
        url = config.BASE_URL + '/?page=' + str(real_page_index)
        url_list += (get_url_list_per_page(url))
    return url_list


def get_url_list_per_page(url) -> list:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_list = []
    for a in soup.find_all('a', {'class': 'topic-title'}):
        url_list.append(config.BASE_URL + a['href'])
    return url_list


def make_diff_url_list():
    with open('./previous_list.json', 'r') as f:
        previous_url_list = json.load(f)["url_list"]
    with open('./list.json', 'r') as f:
        new_url_list = json.load(f)["url_list"]
    diff_url_list = {'url_list':list(set(new_url_list) - set(previous_url_list))}
    logger.info(f"Updated {str(len(diff_url_list))} URLs.")
    with open('./diff_list.json', 'w') as f:
        json.dump(diff_url_list, f, indent=4)
    logger.success(f"Diff list saved to diff_list.json.")


if __name__ == '__main__':
    shutil.copyfile('list.json', 'previous_list.json')
    logger.info("Copied list.json to previous_list.json.")
    url_list = {'url_list': get_all_url_list(get_total_page())}

    with open("list.json", "w") as f:
        json.dump(url_list, f, indent=4)
    logger.success("Saved url list to list.json.")

    make_diff_url_list()
