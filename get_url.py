import requests
from sgmllib import SGMLParser
import sys

class LinkExtractor(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.links = []

    def start_a(self, attrs):
        for attr, value in attrs:
            if attr == 'href':
                self.links.append(value)

def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    parser = LinkExtractor()
    parser.feed(response.text)
    return parser.links

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    links = extract_links(url)

    print(f"Links found in {url}:")
    for link in links:
        print(link)
