import re

def get_domain(url):
    match = re.search("https?://(.*\.)?(\w*)\.", url)
    return match.group(2)

def main():
    print(get_domain("http://gonra.tumblr.com/post/50932642826"))

if __name__ == '__main__':
    main()
