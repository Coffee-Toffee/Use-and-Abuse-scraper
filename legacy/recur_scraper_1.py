from bs4 import BeautifulSoup as Soup
import time
import collections
import random
import sys

import scraper
import Function_Parser_UnA

# A pen?
# No.
# Click
# And clack
# Slowly through the night
# Life is given to
# Progress

'''
This machine id buisness is so that if you have multiple
machines to run your code on, you can (and should) paralize the scraping.
In particular, the machine_id is for the catagory.
If you have more than 15 computers, you can spit the catagories even more,
alphabeticaly this time.

This subsub id shenanigans were developed in order to scrape the regional catagory,
for it seems to be nearly as large as the rest of the directory combined.

Let's say, for example, we're wanting to scrape north america. That's pretty large,
so we want to uncomment out one of the bottom two subsubcatagory lists, and then devote
those differnt machines to the same sub_id.
'''

machine_id = 9
sub_id, subsub_id = 0, 0
catagories = [
"Arts", "Business", "Computers",
"Games", "Health", "Home", "News",
"Recreation", "Reference", "Regional",
"Science", "Shopping", "Society",
"Sports", "Kids_and_Teens"]

subcatagories = ["Europe", "Middle_East", "North_America", "Oceana", "Polar_Regions"]

# These differing amounts of subcatagories determine how many machines are scraping / what part.

#subsubcatagories = ("abcdefghijkl", "mnopqrstuvwxyz")
#subsubcatagories = ["abcdefg", "hijklm", "nopqrs", "tuvwxyz"]
subsubcatagories = ["abcd", "efgh", "ijkl", "mnop", "qrst", "uvwzyz"]
#subsubcatagories = ["ab", "cd", "ef", "gh", "ij", "kl", "mn", "opq", "rst", "uvwxyz"]

sys.setrecursionlimit(100000)
#increase machine limit of stack (because recursion goes recursion goes...)


def store_set(link, sub_id, subsub_id):
    # appends the link that we went to, to the set of previous visited links
    # sorry for the poor practice
    try:
        with open("set_" + sub_id+ "_" + str(subsub_id) + ".txt", "a") as f:
            f.write(link +"\n")
    except:
         with open("set_" + sub_id+ "_" + str(subsub_id) + ".txt", "w") as f:
            f.write(link +"\n")
   
def correct_subsub(subsub_id, sub_id, link, machine_id):
    # Checks if it's the correct subsubcatagory
    lst = ["/en/" + catagories[machine_id] + "/" + subcatagories[sub_id] + "/" +  cat for cat in subsubcatagories[subsub_id] ]
    for i in lst:
        if i.lower() in link.lower():
            return(True)
    #print("no, false subsubcatagory ")
    return(False)

def in_set(sub_id, link, subsub_id):
    #Returns True if the given link is in the set of previously visited links
    try:
        with open("set_" + sub_id+ "_" + str(subsub_id) + ".txt", "r") as f:
            lines = f.readlines()
            if link+"\n" in lines:
                return(True)
            else:
                return(False)
    except:
        return(False)
        #This shouldn't ever be invoked, but it's here as a saftey

def rec_get_sites(link, orgin):
    '''
    The main function, it scrapes the website,
    saves the content, and then scrapes all the websites under
    itself, recursively.
    (Uses a text file to maintain the set of sites)

    '''
    if in_set(str(sub_id), link, subsub_id):
        print("No ", link)
        return(None)
    else:
        store_set(link, str(sub_id), subsub_id)
        time.sleep(0.9)
        time.sleep(trunc_norm(0.2, 0.02))
    
    content = scraper.get_data(link)
    path = get_path(link)
    save_data(content, sub_id, subsub_id)
    print("\n", "link: ", link, '\n')
    with open("term_output_"+ str(sub_id) + "_" + str(subsub_id) + ".txt", "a") as f:
        f.write("\n\n"+ "link:"+ link+ '\n\n')

    Function_Parser_UnA.store_external_dictionary(content, path, str(sub_id), str(subsub_id))
    links = get_internal_links(content, orgin)
    
    #print("internal links:", links)
    #links = make_fresh_links(links, machine_id, sub_id) 
    #print("fresh links:", links)

    print("Links:\n\n" + str(links) + "\n")    

    for link in links:
        rec_get_sites(link, orgin)

def get_internal_links(content, orgin):
    soup = Soup(content, 'html.parser')
    to_return = collections.deque()
    all_links = [link.get('href') for link in soup.find_all('a')]
    #print("----\n all links:\n", all_links, "--------")
    for link in all_links :
        if (link is not None) and ("curlie.org/en/" in link) :
            to_return.append(link)
        #Order of the and statements matters here:
        elif (
        (link is not None) and (len(link) > 1) and (link[0] == "/")
        and ("/en/" in link) and ('/docs/' not in link) and ("/editors/" not in link) 
        and ("/en/" + catagories[machine_id] + "/" + subcatagories[sub_id] + "/" in link) and correct_subsub(subsub_id, sub_id, link, machine_id)
        ):
            to_return.append("https://curlie.org" + link)
    #print("------------------\nto return:", list(to_return), "------------\n\n")
    return(list(to_return))

def save_data(content, sub_id, subsub_id):
    # Writes the raw html to a file (Can take this out if space is an issue (but it probably ain't)).
    try:
        with open("sites_"+ str(sub_id) + "_" + str(subsub_id) + ".txt", "a") as f:
            f.write("-----\n" + content)
    except FileNotFoundError:
        with open("sites_"+ str(sub_id) + "_" + str(subsub_id) + ".txt", "w") as f:
            f.write("-----\n" + content)
    except:
        try:
            with open("sitesv2_"+ str(sub_id) + "_" + str(subsub_id) + ".txt", "a") as f:
                f.write("-----\n" + content)
        except FileNotFoundError:
            with open("sitesv2_"+ str(sub_id) + "_" + str(subsub_id) + ".txt", "w") as f:
                f.write("-----\n" + content)
        except:
            print('error!\n\n')
   

def trunc_norm(mu, sigma):
    '''
    A normal distribution, designed to return a non-negative time
    '''
    rand = random.normalvariate(mu, sigma)
    if rand > 0:
        return(rand)
    else:
        return(0)

def get_path(url_string):
    url_string = url_string
    url_string = url_string[19:]
    seperator = "|"
    url_string = url_string.replace("/", seperator)
    return url_string

if __name__ == "__main__":
    if len(sys.argv) == 1:
        initial_site = "https://curlie.org/en/" + catagories[machine_id] +"/"+subcatagories[sub_id] + "/"
        for link in get_internal_links(scraper.get_data(initial_site), initial_site):
                rec_get_sites(link, initial_site)
        print("\n\nDONE!\n\n")
    else:
        print("usage: python recur_scraper.py")

'''
Old, quick example, that can be helpful.
If you use this, make sure to add the below line on around line 150
        and ("/en/Arts/Animation/Cartoons/"  in link) #TODO: Comment me out before deploy
if __name__ == "__main__":
    initial_site =  "https://curlie.org/en/Arts/Animation/Cartoons/"
    for link in get_internal_links(scraper.get_data(initial_site), initial_site):
            rec_get_sites(link, initial_site)
    print("\n\nDONE!\n\n")
'''
