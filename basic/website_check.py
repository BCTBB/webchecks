#!/usr/bin/env python
import requests
import argparse

parser = argparse.ArgumentParser(description='Website Monitor')
parser.add_argument("-u", "--url", default="", help="Specify the URL of the page that you would like to monitor)")

args = parser.parse_args()
pageurl = args.url

if pageurl == "":
    print("1")
    exit()

elif pageurl != "":
    try:
        r = requests.get(pageurl, allow_redirects=True, timeout=15)
        # We need to try getting a status code, if we cannot return a 0 as a status code.
        if r.status_code == int("200"):
            print r.status_code
        else:
            print("3")
    except:
        # CloudOps error status code
        print("0")