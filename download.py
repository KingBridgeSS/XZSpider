import json
import concurrent.futures
from loguru import logger
import config
import xz_spider_worker
from tqdm import tqdm
import getopt
import sys


def work(url):
    worker = xz_spider_worker.XzSpiderWorker(url, config.save_path)
    worker.work()


def usage():
    print("Usage: python3 download.py -d <save_path>")
    print("Options:")
    print("  -d <save_path>  Specify the save path for downloaded files (if not specified, download to ./downloads)")
    print("  -h              Show this help message")


if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:h")
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(2)
    for option, value in optlist:
        if option == '-h':
            usage()
            sys.exit()
        elif option == '-d':
            config.save_path = value
        else:
            assert False, "Unknown option: " + option
    # load url list
    with open('./diff_list.json', 'r') as f:
        url_list = json.load(f)['url_list']
    logger.info(f'Loaded {str(len(url_list))} URLs.')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(work, url) for url in url_list]
        with tqdm(total=len(futures)) as pbar:
            for future in concurrent.futures.as_completed(futures):
                pbar.update(1)
