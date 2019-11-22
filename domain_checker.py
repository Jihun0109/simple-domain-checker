#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2019 - 2019 Jihun0109

import requests
import argparse

tmout = 6
parser = argparse.ArgumentParser(prog='domain_checker.py',add_help=False)

parser.add_argument('-u', '--url')
parser.add_argument('-l', '--list')
parser.add_argument('-t', '--timeout')
args = parser.parse_args()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}



if not args.url and not args.list:
    print ("Usage: ")
    print (">> python domain_checker.py --url,u <url> --list,l <input file>")
    exit(0)

if args.timeout:
    tmout = args.timeout

if args.url:
    try:
        r = requests.get(args.url, headers=headers, allow_redirects=False, timeout=tmout)        
        if r.status_code == 200:
            print ("The domain " + args.url + " is alive.")
        elif r.status_code == 302:
            print ("The domain " + args.url + " is alive, but it redirect to another url.")
        exit(0)
    except:
        pass
    
    print ("The domain " + args.url + " dead.")
    exit(0)

elif args.list:
    fp = open(args.list, 'r')
    urls = fp.readlines()
    fp.close()
    urls = [url.strip().strip('\n') for url in urls]

    fp_live = open("alive.txt", 'w')
    fp_dead = open("dead.txt", 'w')

    live_count = 0
    dead_count = 0

    for url in urls:
        print ("Checking.... " + url)
        try:
            r = requests.get(url, headers=headers, allow_redirects=False, timeout=tmout)
        except:
            print ("[] => timeout!")
            fp_dead.write(str(url))
            fp_dead.write('\n')
            dead_count += 1
        else:
            if (r.status_code == 200 or r.status_code == 301) and len(r.text) > 2000:
                print (str(r.status_code) + " => Alive")
                fp_live.write(str(url))
                fp_live.write('\n')
                live_count += 1
            else:
                print (str(r.status_code) + " => Dead")
                fp_dead.write(str(url))
                fp_dead.write('\n')
                dead_count += 1
        
    fp_live.close()
    fp_dead.close()

    print ("")
    print ("[Completed]")
    print ("Alive domains: " + str(live_count))
    print ("Dead domains: " + str(dead_count))
