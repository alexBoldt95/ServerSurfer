'''
Alex Boldt
Traverses the internet by randomly choosing links to request given an arbitrary start point
'''

import operator
import sys
import signal
import random
from html.parser import HTMLParser
import requests
from link_scraper import LinkScraper
from termcolor import cprint
import my_urllib
from exception_lib import TimeoutException


DEBUG = 0 #Print debugging var

def timeout_handler(signum, frame):
    '''
    Called when the sigalarm times out, raises a TimeoutException
    '''
    #pylint: disable=unused-argument
    raise TimeoutException("requested for more 10 seconds")
    #pylint: enable=unused-argument

def get_links(page):
    '''
    given an HTML page, scrape the <a href> tag bodies off and return as a list of strings
    '''
    parser = LinkScraper(HTMLParser, page)
    if DEBUG:
        cprint("CREATED PARSER", "yellow")
    signal.alarm(10)
    if DEBUG:
        cprint("SET ALARM", "yellow")
    try:
        req = requests.get(page)
    except TimeoutException as exc:
        cprint(exc, "yellow")
        return []
    signal.alarm(0)
    if DEBUG:
        cprint("REQUESTED AND GOT HTML", "yellow")
    parser.feed(req.text)
    if DEBUG:
        cprint("FEED RETURNED", "yellow")
    return parser.link_list

def choose_path(link_list):
    '''
    choose a random link from the list of links
    '''
    return link_list[random.randrange(len(link_list))]

def print_dict_sorted(arg_dict):
    '''
    given a dict mapping string -> int, print dict in reverse order of values
    '''
    #pylint: disable=bad-whitespace
    sorted_tups = [(k,v) for k,v in arg_dict.items()]
    sorted_tups.sort(key=operator.itemgetter(1), reverse=True)
    for k,v in sorted_tups:
        print(k + " : " + str(v))
    #pylint: enable=bad-whitespace

def traverse(start):
    '''
    given a start point, traverse the internet, backing up by one page on pages without links and
    timing out after 10 seconds
    '''
    signal.signal(signal.SIGALRM, timeout_handler)
    choice = start
    parent = choice[:]
    choices = get_links(choice)
    jumps = 0
    domain_dict = {}
    try:
        while 1:
            if len(choices) == 0:
                cprint("****LEAFED AT: " + choice + ", reattempting from " + parent, "yellow")
                choice = parent[:]
                choices = get_links(choice)
                continue
            if DEBUG:
                print("parent:", parent)
                print("choice:", choice)
            else:
                print(choice)
            domain = my_urllib.get_domain(choice)
            if domain not in domain_dict:
                domain_dict[domain] = 0
            domain_dict[domain] += 1
            parent = choice[:]
            choice = choose_path(choices)
            choices = get_links(choice)
            jumps += 1
    except KeyboardInterrupt:
        cprint("\nkeyboard interrupt caught", "red")
        print("jumps: ", jumps)
        print("number of domains visited:", len(domain_dict.keys()))
        print_dict_sorted(domain_dict)
        #print(sorted(list(domain_set)))


def main():
    '''
    main, accepts a command line arg as the starting point
    '''
    traverse(sys.argv[1])


if __name__ == '__main__':
    main()
