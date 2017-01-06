import requests
from html.parser import HTMLParser
from link_scraper import LinkScraper
import random
from termcolor import cprint
import signal
import my_urllib

DEBUG = 0

def timeout_handler(signum, frame):
    raise Exception("requested for more 10 seconds")

def get_links(page):
    parser = LinkScraper(HTMLParser, page)
    if DEBUG:
        cprint("CREATED PARSER", "yellow")
    signal.alarm(10)
    if DEBUG:
        cprint("SET ALARM", "yellow")
    try:
        r = requests.get(page)
    except Exception as exc:
        cprint(exc, "yellow")
        return []
    signal.alarm(0)
    if DEBUG:
        cprint("REQUESTED AND GOT HTML", "yellow")
    parser.feed(r.text)
    if DEBUG:
        cprint("FEED RETURNED", "yellow")
    return parser.link_list

def choose_path(link_list):
    return link_list[random.randrange(len(link_list))]

def traverse(start):
    signal.signal(signal.SIGALRM, timeout_handler)
    choice = start
    parent = choice[:]
    choices = get_links(choice)
    jumps = 0
    domain_set = set()
    try:
        while(1):
            if(len(choices)==0):
                cprint("****LEAFED AT: " + choice + ", reattempting from " + parent, "yellow")
                choice = parent[:]
                choices = get_links(choice)
                continue
            if DEBUG:
                print("parent:", parent)
                print("choice:", choice)
            else:
                print(choice)
                domain_set.add(my_urllib.get_domain(choice))
            parent = choice[:]
            choice = choose_path(choices)
            choices = get_links(choice)
            jumps += 1
    except KeyboardInterrupt:
        cprint("\nkeyboard interrupt caught", "red")
        print("jumps: ", jumps)
        print("number of domains visited:", len(domain_set))
        print(sorted(list(domain_set)))


def main():
    traverse("http://www.homecharlottehome.com/")


if __name__ == '__main__':
    main()
