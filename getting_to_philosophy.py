import sys
import requests, re
from bs4 import BeautifulSoup
import time

def find_philosophy(url):

    max_requests = 0
    heading = ''
    first_link_list = []
    first_link = url
    urlbase = 'https://en.wikipedia.org'

    while max_requests < 25 and heading != "Philosophy":
        result = get_heading_and_first_link(first_link)
        first_link = urlbase + result[1].attrs['href']
        heading = result[0]

        print(heading)
        print(result[1].text + ": " + first_link)
        print(max_requests)
        print("==============")

        if first_link in first_link_list:
            print("loop")
            break
        elif heading == "Philosophy":
            print("Philosophy found!!!")
            break

        first_link_list.append(first_link)
        max_requests = max_requests + 1


def get_heading_and_first_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    BADLINKS = ['Help:', 'File:', 'Wikipedia:', 'Talk:', '_\(disambiguation\)', '/upload.wikimedia', 'redline=1',
                'Media_help', '.ogg', '.php', '.org', ".svg", "cite_note"]
    BADTAGS = ['i', 'em', 'cite', 'tr', 'sup', 'span', 'small', 'table', 'img', 'li', 'ul', 'ol', 'style', 'noscript', 'h2', 'h3', 'h4']
    BADCLASSES = ['navbox', 'vertical-navbox', 'toc', 'mw-editsection', 'thumbinner', 'mw-empty-elt', 'mw-redirect',
                  'mw-disambig', 'printfooter']

    soup = soup.find(id="mw-content-text")
    for tag in soup.find_all(BADTAGS):
        tag.decompose()
    for tag in soup.find_all(class_=BADCLASSES):
        tag.decompose()

    first_link = ''
    pagragraph = soup.select("p")
    for p in pagragraph:
        p = str(p)
        p = re.sub("[^_]\(.*?\)", "", p)
        link = BeautifulSoup(p, "html.parser").find("a")
        if re.search(''.join(BADLINKS), str(link)) or re.search(''.join(BADCLASSES), str(link)) or link is None:
            continue  # check next link
        else:
            first_link = link
            heading = soup.select_one("p > b").text
            break

    time.sleep(2)
    return [heading, first_link]


if __name__ == '__main__':
    urlRandom = 'http://en.wikipedia.org/wiki/Special:Random'

    if len(sys.argv) == 1:  # if no arguments, use random Wikipedia page
        print("Using http://en.wikipedia.org/wiki/Special:Random")
        print("======================================")
        url = urlRandom
    else:
        url = sys.argv[1]


    find_philosophy(url)