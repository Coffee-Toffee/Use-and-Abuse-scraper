from bs4 import BeautifulSoup
import collections

def get_external_urls(content, orgin):
    soup = BeautifulSoup(content, 'html.parser')
    to_return = collections.deque()
    all_links = [link.get('href') for link in soup.find_all('a')]
    all_names = [link.string for link in soup.find_all('a')]
    #print("----\n all links:\n", all_links, "--------")
    external = ["search.aol", "www.ask.com", "google", "startpage", "yandex",
                "duckduckgo", "www.bing.com", "yahoo", "gigablast", "ecosia"]
    for index, link in enumerate(all_links) :
        if (
        (link is not None) and (link != "") and (link[0] not in ("/", "#"))
        and (orgin not in link) and (0 not in [i not in link for i in external])
        ):
            to_return.append(tuple((link, all_names[index])))
    return(list(set(to_return)))

if __name__ == "__main__":
    f = open("Website_Structure29", "r")
    testing_html_file = f.read()
    f.close()
    store_external_dictionary(testing_html_file, "Testing:Path:Curlie:Arts")
