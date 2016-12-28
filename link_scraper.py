from html.parser import HTMLParser
import requests


class LinkScraper(HTMLParser):
    link_list = [] #ayyy
    curr_point = ""
    raw_link_set = set()
    def __init__(self, HTMLParser, cp):
        super().__init__()
        self.link_list = []
        self.raw_link_set = set()
        self.curr_point = cp

    def feed(self, data):
        super().feed(data)
        try:
            self.raw_link_set.remove(self.curr_point)
        except KeyError:
            pass
        self.link_list = list(self.raw_link_set)

    def handle_starttag(self, tag, attrs): #override to extract link from <a href=foo> tags
        if(tag.lower() == 'a'):
            for k,v in attrs:
                if k.lower() == "href" and v.startswith("http"):
                    self.raw_link_set.add(v)

def main():
    parser = LinkScraper()
    r = requests.get("http://www.homecharlottehome.com/")
    parser.feed(r.text)
    print(parser.link_list)

if __name__ == '__main__':
    main()
