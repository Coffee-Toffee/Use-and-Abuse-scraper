from bs4 import BeautifulSoup as Soup
import time
import collections
import random

import scraper
import Function_Parser_UnA

'''
This machine id buisness is so that if you have multiple
machines to run your code on, you can paralize the scraping
'''
machine_id = 0

catagories = [
"Arts", "Business", "Computers",
"Games", "Health", "Home", "News",
"Recreation", "Reference", "Regional",
"Science", "Shopping", "Society",
"Sports", "Kids_and_Teens"]


def rec_get_sites(link, orgin, set_of_sites):
    '''
    The main function, it scrapes the website,
    saves the content, and then scrapes all the websites under
    itself, recursively.
    '''
    content = scraper.get_data(link)
    path = get_path(link)
    save_data(content)
    print("\n", "link: ", link, '\n')
    with open("term_output.txt", "a") as f:
        f.write("\n\n"+ "link:"+ link+ '\n\n')

    with open("set_output.txt", "a") as f:
        f.write("\n\n"+ "set:\n"+ str(set_of_sites)+ '\n\n')

    Function_Parser_UnA.store_external_dictionary(content, path)
    links = get_internal_links(content, orgin)
    links = set(links) - set_of_sites
    set_of_sites = set_of_sites | links
    #print("set_of_sites:", set_of_sites, '\n')
    #print("-----------------------")
    for link in links:
        time.sleep(0.9)
        time.sleep(trunc_norm(0.6, 0.1))
        rec_get_sites(link, orgin, set_of_sites)

def get_internal_links(content, orgin):
    soup = Soup(content, 'html.parser')
    to_return = collections.deque()
    all_links = [link.get('href') for link in soup.find_all('a')]
    #print("----\n all links:\n", all_links, "--------")
    for link in all_links :
        if (link is not None) and ("curlie.org/en/" in link) :
            to_return.append(link)
        elif (
        (link is not None) and (link[0] == "/") and (len(link) > 1) 
        and ("/en/" in link) and ('/docs/' not in link) and ("/editors/" not in link) 
        and ("/en/" + catagories[machine_id] +"/" in link)
        ):
            to_return.append("https://curlie.org" + link)
    #print("------------------\nto return:", list(to_return), "------------\n\n")
    return(list(to_return))

def save_data(content):
    with open("sites.txt", "a") as f:
        f.write("-----\n" + content)

def trunc_norm(mu, sigma):
    '''
    A truncated normal distribution, designed to only fall
    within 5 standard deviations of the mean. While yes, theoreticly
    this code is non-halting, it will terminate at some point in actuality
    '''
    res = random.normalvariate(mu, sigma)
    if (res < mu - 5*sigma ) or (res > mu + 5*sigma):
        trunc_norm(mu, sigma)
    else:
        return(res)

def get_path(url_string):
    url_string = url_string
    url_string = url_string[19:]
    seperator = "|"
    url_string = url_string.replace("/", seperator)
    return url_string

if __name__ == "__main__":
    initial_site = "https://curlie.org/en/" + catagories[machine_id] +"/"
    for link in get_internal_links(scraper.get_data(initial_site), initial_site):
            rec_get_sites(link, initial_site, {"https://curlie.org/en/"+ catagories[machine_id] +"/"})
'''
Old, quick example, that can be helpful.
If you use this, make sure to change catagories[machine_id] on line 61 
if __name__ == "__main__":
    initial_site =  "https://curlie.org/en/Arts/Animation/Cartoons/Titles/M/"
    for link in get_internal_links(scraper.get_data(initial_site), initial_site):
            rec_get_sites(link, initial_site, {"https://curlie.org/en/Arts/Animation/Cartoons/Titles/M/"})
'''
