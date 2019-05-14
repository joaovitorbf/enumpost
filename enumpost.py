#!/usr/bin/env python3
#POST request user enumeration tool
#JoaoVitorBF

from multiprocessing import Process, Queue
import argparse
import requests

def process_enum(queue, wordlist, url, payload):
    # Payload to dictionary
    payload_dict = {}
    for load in payload:
        split_load = load.split(":")
        if split_load[1] != '{USER}':
            payload_dict[split_load[0]] = split_load[1]
        else:
            payload_dict[split_load[0]] = '{USER}'
    
    # Enumeration
    for user in wordlist:
        for key, value in payload_dict.items():
            if value == '{USER}'
                payload_dict[key] = user
        r = requests.post(url, data=payload_dict)


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="POST request user enumeration tool")
    parser.add_argument("wordlist", help="username wordlist")
    parser.add_argument("url", help="the URL to send requests to")
    parser.add_argument("payload", nargs='+', help="the POST request payload to send")
    parser.add_argument("failstr", help="failure string to search in the response body")
    parser.add_argument("-c", metavar="cnt", type=int, default=10, help="process (thread) count, default 10")
    parser.add_argument("-v", action="store_true", help="verbose mode")
    args = parser.parse_args()

    wordlist = args.wordlist
    url = args.url
    payload = args.payload
    verbose = args.v
    thread_count = args.c

    # Distribute wordlist to threads
    wlfile = open(wordlist, "r", encoding="ISO-8859-1")
    tothread = 0
    wllist = [[] for i in range(thread_count)]
    for user in wlfile:
        wllist[tothread-1].append(user.strip())
        if (tothread < thread_count):
            tothread+=1
        else:
            tothread = 0
    
    q = Queue()
    processes = []
    for i in range(thread_count):
        p = Process(target=process_enum, args=(q, wllist[i], url, payload,))
        processes.append(p)
    for p in processes:
        p.join()