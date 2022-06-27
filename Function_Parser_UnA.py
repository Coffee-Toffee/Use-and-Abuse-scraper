from bs4 import BeautifulSoup
import collections

def store_external_dictionary(string, path):
    site_text = string
    path = path
    list_of_urls = get_urls(site_text)
    dict_pairing = {path: list_of_urls}
    try:
        f2 = open("dict.txt", "a")
    except:
        f2 = open("dict.txt", "w")
        f2.close()
        f2 = open("dict.txt", "a")
    f2.write(str(dict_pairing) +"\n\n")
    f2.close()
    
def get_urls(site_text):
    pre_processed_urls = [item[0] for item in get_external_urls(site_text, "curlie")]
    list_of_urls = collections.deque()
    for url in pre_processed_urls:
            #Final_val is not updating when process_url is being called again.
            list_of_urls.append(process_url(url))

    #reason why we use a deque, is that we have to insert O(n) times, and for a list, that's O(n^2).
    return(list(list_of_urls), [item[1] for item in get_external_urls(site_text, "curlie")])

def get_external_urls(content, orgin):
    soup = BeautifulSoup(content, 'html.parser')
    to_return = collections.deque()
    all_links = [link.get('href') for link in soup.find_all('a')]
    all_names = [link.string for link in soup.find_all('a')]
    #print("----\n all links:\n", all_links, "--------")
    external = ["search.aol", "www.ask.com", "google", "startpage", "yandex", "duckduckgo", "www.bing.com", "yahoo", "gigablast", "ecosia"]
    for index, link in enumerate(all_links) :
        if (link is not None) and (link[0] not in ("/", "#")) and (orgin not in link) and (0 not in [i not in link for i in external]):
            to_return.append(tuple((link, all_names[index])))
    return(list(set(to_return)))

def process_url(url):
    url = str(url)
    '''
    removes subdomains, is not wanted at this time
    url = url.split("/")
    url = url[0] + "//" + url[2] + "/"
    '''
    with open("term_output.txt", 'a') as f:
        f.write(url + "\n")
    print(url)
    return(url)

if __name__ == "__main__":
    f = open("Website_Structure29", "r")
    testing_html_file = f.read()
    f.close()
    store_external_dictionary(testing_html_file, "Testing:Path:Curlie:Arts")
