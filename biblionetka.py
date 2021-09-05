#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.biblionetka.pl/user_ratings.aspx?id="
USER_AGENT = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}


def get_single_page(url, user_agent):
    data = []
    has_next = True

    page = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    reviews = soup.find_all(class_="row forum__list")
    for review in reviews:
        author = ""
        title = ""
        biblionetka_author_id = 0
        biblionetka_book_id = 0
        score = review.find('div', class_="col-xs-2").string
        m = re.search(r"(\d[,.]\d)", score)
        if m:
            score = float(m.group(1).replace(",", "."))
        for x in review.find_all('a'):
            href = x.get('href')
            m = re.search(r"(.*?)\.aspx\?id=(\d+)", href)
            if m:
                if m.group(1) == "author":
                    author = x.text
                    biblionetka_author_id = m.group(2)
                elif m.group(1) == "book":
                    title = x.text
                    biblionetka_book_id = m.group(2)
        book = {"title": title, "title_id": biblionetka_book_id, "author": author, "author_id": biblionetka_author_id, "score": score}
        data.append(book)

    # no data found
    if len(data) == 0:
        has_next = False

    return data, has_next


def get_all_revievs(uid, base_url, user_agent, verbose):
    alldata = []
    page = 0
    url = "{}{}".format(base_url, uid)
    has_next = True
    while has_next:
        data, has_next = get_single_page(url, user_agent)
        if verbose:
            print("Got {} with {} book reviews".format(url, len(data)))
        page += 1
        # break if last element is already known
        if data[-1] in alldata:
            has_next = False
            if verbose:
                print("Last results already known. Finished.")
        else:
            alldata += data
            url = "{}{}&p={}".format(base_url, uid, page)
    return alldata


def main():
    args = parse_arguments()
    reviews = get_all_revievs(args.uid, BASE_URL, USER_AGENT, args.verbose)
    json_string = json.dumps(reviews, indent=2)
    if args.verbose:
        print("Got {} book reviews".format(len(reviews)))

    if args.output:
        if args.verbose:
            print("Saving to file {}".format(args.output))
        with open(args.output, "w") as outfile:
            outfile.write(json_string)
    if not args.output or args.verbose:
        print(json_string)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Biblionetka reviews exporter')
    parser.add_argument(
        '-u', '--uid', required=True, type=int,
        help="Biblionetka user ID")
    parser.add_argument(
        '-o', '--output', required=False,
        help="Output file name")
    parser.add_argument(
        '-v', '--verbose', required=False,
        default=False, action='store_true',
        help="Verbose mode")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
