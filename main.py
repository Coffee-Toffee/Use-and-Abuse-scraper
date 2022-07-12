from bs4 import BeautifulSoup as Soup
import time
import collections
import random
import sys

import scraper
import Function_Parser_UnA


'''
This machine id buisness is so that if you have multiple
machines to run your code on, you can (and should) paralize the scraping.
In particular, the machine_id is for the catagory.
If you have more than 15 computers, you can spit the catagories even more,
alphabeticaly this time
(set sub_id to 50 to not do sub id's)
(If you have over 50 subcatagories in a single catagory, 
then you can change the number (but you probably shouldn't have that amount))
'''

#By default, doesn't do subcatagories
machine_id, sub_id = 0, 50

catagories = [
"Arts", "Business", "Computers",
"Games", "Health", "Home", "News",
"Recreation", "Reference", "Regional",
"Science", "Shopping", "Society",
"Sports", "Kids_and_Teens"]

subcatagories = ("abcdefghijkl", "mnopqrstuvwxyz")
#subcatagories = ["abcdefg", "hijklm", "nopqrs", "tuvwxyz"]
# (So if you want to have 3 subcatagories, you'd choose this)
#subcatagories = ["abcd", "efgh", "ijkl", "mnos", "pqrt", "uvwxyz"]

sys.setrecursionlimit(100000)
# increase machine limit of stack. (While yes, this is probably overkill,
# at least it won't crash due to recursion depth being exceeded)


def store_set(link, machine_id, sub_id):
    # appends the link that we went to, to the set
    try:
        with open("set_" + machine_id + "_" + str(sub_id) + ".txt", "a") as f:
            f.write(link +"\n")
    except:
         with open("set_" + machine_id + "_" + str(sub_id) + ".txt", "w") as f:
            f.write(link +"\n")

def correct_sub(sub_id, link, machine_id):
    if sub_id == 50:
        return(True)
    lst = ("/en/" + catagories[machine_id] + "/" + cat for cat in subcatagories[sub_id])
    # If this breaks, replace "(" with "[" (and the other way too)
    for i in lst:
        if i.lower() in link.lower():
            return(True)
    print("no, false subcatagory ")
    return(False)

def in_set(machine_id, link, sub_id):
    #Returns True if the given link is in the set of previously visited links
    try:
        with open("set_" + machine_id + "_" + str(sub_id) + ".txt", "r") as f:
            lines = f.readlines()
            if link+"\n" in lines:
                return(True)
            else:
                return(False)
    except:
        return(False)

def rec_get_sites(link, orgin):
    '''
    The main function, it scrapes the website,
    saves the content, and then scrapes all the websites under
    itself, recursively.
    (Uses a text file to maintain set_of_sites)

    '''
    if in_set(str(machine_id), link, sub_id):
        print("No ", link)
        return(None)
    else:
        store_set(link, str(machine_id), sub_id)
        time.sleep(0.9)
        time.sleep(norm(0.2, 0.05))
        #If you have working proxies, comment out the above two lines

    content = scraper.get_data(link)
    path = get_path(link)
    save_data(content, machine_id, sub_id)
    print("\n", "link: ", link, '\n')
    with open("term_output_"+ str(machine_id) + "_" + str(sub_id) + ".txt", "a") as f:
        f.write("\n\n"+ "link:"+ link+ '\n\n')

    Function_Parser_UnA.store_external_dictionary(content, path, str(machine_id), str(sub_id))
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
        #Old crash issue used to be here:
        elif (
        (link is not None) and (len(link) > 1) and (link[0] == "/")
        and ("/en/" in link) and ('/docs/' not in link) and ("/editors/" not in link) 
        and ("/en/" + catagories[machine_id] +"/" in link) and correct_sub(sub_id, link, machine_id)
        ):
            to_return.append("https://curlie.org" + link)
    #print("------------------\nto return:", list(to_return), "------------\n\n")  Old debug line
    return(list(to_return))

def save_data(content, machine_id, sub_id):
    try:
        with open("sites_"+ str(machine_id) + "_" + str(sub_id) + ".txt", "a") as f:
            f.write("-----\n" + content)
    except FileNotFoundError:
        with open("sites_"+ str(machine_id) + "_" + str(sub_id) + ".txt", "w") as f:
            f.write("-----\n" + content)
    except:
        try:
            with open("sitesv2_"+ str(machine_id) + "_" + str(sub_id) + ".txt", "a") as f:
                f.write("-----\n" + content)
        except FileNotFoundError:
            with open("sitesv2_"+ str(machine_id) + "_" + str(sub_id) + ".txt", "w") as f:
                f.write("-----\n" + content)
        except:
            print('error!\n\n')
   
def norm(mu, sigma):
    '''
    A normal distribution that always returns a nonnegative output
    '''
    rand = random.normalvariate(mu, sigma)
    return(0 if rand < 0 else rand)

def get_path(url_string):
    url_string = url_string
    url_string = url_string[19:]
    seperator = "|"
    url_string = url_string.replace("/", seperator)
    return url_string

if __name__ == "__main__":
    if len(sys.argv) == 1:
        initial_site = "https://curlie.org/en/" + catagories[machine_id] +"/"
        for link in get_internal_links(scraper.get_data(initial_site), initial_site):
                rec_get_sites(link, initial_site)
        print("\n\nDONE!\n\n")
    else:
        print("usage: main.py")

'''
Old, quick example, that can be helpful.
If you use this, make sure to add the below line on around line 150
        and ("/en/Arts/Animation/Cartoons/"  in link) 
if __name__ == "__main__":
    initial_site =  "https://curlie.org/en/Arts/Animation/Cartoons/"
    for link in get_internal_links(scraper.get_data(initial_site), initial_site):
            rec_get_sites(link, initial_site)
    print("\n\nDONE!\n\n")
'''
