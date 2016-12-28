import requests
from html.parser import HTMLParser
from link_scraper import LinkScraper
import random
#from termcolor import colored

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def get_links(page):
    parser = LinkScraper(HTMLParser, page)
    r = requests.get(page)
    parser.feed(r.text)
    return parser.link_list

def choose_path(link_list):
    return link_list[random.randrange(len(link_list))]

def main():
    start_point = "http://www.homecharlottehome.com/"
    choices = get_links(start_point)
    while(True):
        choice = choose_path(choices)
        print(choice)
        choices = get_links(choice)
        if(len(choices)==0):
            print(bcolors.FAIL + "****LEAFED AT: " + choice + bcolors.ENDC)
            #print("****LEAFED AT: " + choice)
            break



if __name__ == '__main__':
    main()
