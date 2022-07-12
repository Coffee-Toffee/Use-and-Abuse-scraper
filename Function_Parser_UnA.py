from bs4 import BeautifulSoup
import collections

def store_external_dictionary(site_text, path, machine_id, sub_id):
    # takes the external urls, and them stores them with the path.
    list_of_urls = get_external_urls(site_text, "curlie")
    dict_pairing = {path: list_of_urls}
    try:
        f2 = open("dict_" + machine_id + "_" + sub_id + ".txt", "a")
    except:
        f2 = open("dict_" + machine_id + "_" + sub_id + ".txt", "w")
        f2.close()
        f2 = open("dict_" + machine_id + "_" + sub_id + ".txt", "a")
    f2.write(path+" |||  ")
    for i in list_of_urls:
        f2.write(" || " + str(i[0]) + " | " + str(i[1]))
    f2.write("\n\n")
    f2.close()
    
def get_external_urls(content, orgin):
    soup = BeautifulSoup(content, 'html.parser')
    to_return = collections.deque()
    all_links = (link.get('href') for link in soup.find_all('a'))
    all_names = [link.string for link in soup.find_all('a')]
    #print("----\n all links:\n", all_links, "--------")
    external = ["search.aol", "www.ask.com", "google", "startpage", "yandex",
                "duckduckgo", "www.bing.com", "yahoo", "gigablast", "ecosia"]
    for index, link in enumerate(all_links) :
        # For the below list comprehension:
        #we check if all of the strings in external aren't contained within the string
        if (
        (link is not None) and (link != "") and (link[0] not in ("/", "#"))
        and (orgin not in link) and (0 not in [i not in link for i in external])
        ):
            to_return.append(tuple((link, all_names[index])))
    return(list(set(to_return)))

if __name__ == "__main__":
    f = open("Func_parser_test.txt", "r")
    testing_html_file = f.read()
    f.close()
    store_external_dictionary(testing_html_file, "Testing:Path:Curlie:Arts", '0', '0')
    store_external_dictionary(testing_html_file, "Testing:Path:Curlie:Arts", '0', '0')
