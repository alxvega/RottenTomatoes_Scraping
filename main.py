# -*- conding: utf-8 -*
import argparse
from datetime import datetime
from Script.rotten_tomatoes import ROTTENTOMATOES
from config import config
import time


if __name__ == "__main__":
    now = datetime.now()
    start_time = time.time()
    created_at = now.strftime("%Y-%m-%d")
    websites_choices = list(config()['websites'].keys())
    parser = argparse.ArgumentParser()
    parser.add_argument('websites', type=str, choices=websites_choices)
    parser.add_argument('-o', type=str)
    parser.add_argument('-d', type=str, default=None)
    parser.add_argument('--skip', nargs="?", default=False, const=True)
    args = parser.parse_args()

    websites = args.websites
    operation = args.o
    date = args.d
    skip = args.skip

    if operation in ('crawlers', 'scraping'):
        locals()[websites](websites, operation, skip, date)

    end_time = time.time()
    total_time = end_time - start_time
    print(f'time: {round(total_time, 2)} seconds')
