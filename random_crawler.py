import requests
from html.parser import HTMLParser
from link_scraper import LinkScraper
import random
from termcolor import cprint
import signal

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

def main():
    signal.signal(signal.SIGALRM, timeout_handler)
    choice = "http://www.homecharlottehome.com/"
    parent = choice[:]
    choices = get_links(choice)
    while(1):
        if(len(choices)==0):
            cprint("****LEAFED AT: " + choice + ", reattempting from " + parent, "yellow")
            choice = parent[:]
            choices = get_links(choice)
            continue
        if DEBUG:
            print("parent:", parent)
        print("choice:", choice)
        parent = choice[:]
        choice = choose_path(choices)
        choices = get_links(choice)




if __name__ == '__main__':
    main()
