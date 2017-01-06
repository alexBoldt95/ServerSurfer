import re
from termcolor import cprint


def get_domain(url):
    try:
        match = re.search("https?://(.*\.)?([\w-]*)\.", url)
        domain = match.group(2)
        return domain
    except AttributeError:
        cprint("no match found for domain in URL: " + url, "red")
        raise


def main():
    print(get_domain("http://enable-javascript.com/"))

if __name__ == '__main__':
    main()
