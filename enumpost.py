#!/usr/bin/env python3
#POST request user enumeration tool
#JoaoVitorBF

from multiprocessing import Process, Queue
import argparse
import requests

def process_enum(queue, wordlist, url, payload, failstr, verbose, proc_id, stop):
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
        user_payload = dict(payload_dict)
        for key, value in user_payload.items():
            if value == '{USER}':
                user_payload[key] = user
        r = requests.post(url, data=user_payload)
        if failstr not in r.text:
            queue.put(user)
            print("[{}] FOUND: {}".format(proc_id, user))
            if stop: quit()
        elif verbose:
            print("[{}] Tried: {}".format(proc_id, user))


if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="POST request user enumeration tool")
    parser.add_argument("wordlist", help="username wordlist")
    parser.add_argument("url", help="the URL to send requests to")
    parser.add_argument("payload", nargs='+', help="the POST request payload to send")
    parser.add_argument("failstr", help="failure string to search in the response body")
    parser.add_argument("-c", metavar="cnt", type=int, default=10, help="process (thread) count, default 10")
    parser.add_argument("-v", action="store_true", help="verbose mode")
    parser.add_argument("-s", action="store_true", help="stop on first found")
    args = parser.parse_args()

    wordlist = args.wordlist
    url = args.url
    payload = args.payload
    verbose = args.v
    thread_count = args.c
    failstr = args.failstr
    stop = args.s

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
    
    found_q = Queue()
    processes = []
    
    for i in range(thread_count):
        p = Process(target=process_enum, args=(found_q, wllist[i], url, payload, failstr, verbose, i, stop))
        processes.append(p)
        p.start()
    
    initial_count = len(processes)

    while True:
        for k, p in enumerate(processes):
            if p.is_alive() == False:
                del processes[k]
        if len(processes) < initial_count and stop:
            for p in processes:
                p.terminate()
        if len(processes) == 0: quit()