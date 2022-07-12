# Process based on the straight HTML content
# Hopefully you shouldn't have to use this
# But it's here because I previously made a mistake with the Funcion Parser earlier, and 
# ran the programs before I realized this.

from bs4 import BeautifulSoup as Soup
import os
import time

import external

def parse(site):
    wikinum = 0
    catnum = 0
    sitenum = 0
    cats = set()
    sites = set()
    wikiset = set()
    #to_return = [] 
    with open(site, "r") as file:
        for line in file:
            #temp = []
            if line != "-----\n": # I haven't tested w/o the conditional, but it's harmless enough, I think.
                urls = external.get_external_urls(line, "curlie.org")
                #temp = [get_path(line), []]
                #print("\n\n\n\n", get_path(line))
                path = get_path(line)
                if path is not None:
                    catnum += 1
                    cats.add(path)
                for i in urls:
                    if i[1] is not None and "/en/" not in i[0]:
                        #print(i)
                        sites.add(i[0])
                        sitenum += 1
                        #temp[1].append(i)

                        if "wikipedia" in i[0]:
                            wikinum += 1
                            wikiset.add(i[0])

                #to_return.append(temp)  (This is *Very* slow, idk why)
                # When we integrate this into the scraper, I think the timing won't matter *as* much, but we'll see...
    return(wikinum, catnum, sitenum, len(cats), len(sites), len(wikiset))

def get_path(data):
    # Coded by Joe Harrison, not me, for once.
    try:
        idx = data.lower().index("<title>")+len("<title>")  # First pass is to look at the title part of the html
    except:
        return(None)
    endidx = data.lower().index("</title>")
    path = data[idx:endidx]
    path = path.replace("&shy;", "")
    path = path.replace(" ", "_")
    path = path.replace(" -", "|")
    path = path.replace(":_", "|")
    path = path.replace("_-_", "|") # Standardizing format
    if (path == "Oops, an Error occured") or (path == "Curlie"):
        #print("aah\n")
        endidx = data.lower().find("<span class=\"volunteer\">") # Next place to look is in the volunteer link
        finalstartidx = data[2:endidx].rfind("</i>")
        finalendidx = data[2:endidx].rfind("<div") # rfind finds the next instance
        newend = data[2:endidx].rfind("</a>")
        idx = data[2:endidx].rfind("href=\'")

        path = data[(idx+9):(newend-7)] + data[(finalstartidx+6):(finalendidx+1)] # Who doesn't love hard-coded values

        path = path.replace("/", "|")
        path = path.replace(" ", "_")
        path = "Curlie" + path[2:None] # Can't do -1 because it wouldn't include the last thing. None is apparently the way to do things

        if ((idx == -1) or (newend == -1) or (endidx == -1)): # Our next attempt after volunteer is in Creating an Account
            try:
                newString = data.split("Create an Account")[1]
                newidx = newString.index("redirect=/")
                newendidx = newString.index("\"", newString.index("\"")+1)
                path = newString[(newidx+len("redirect=/")):newendidx-1]
                return(path)
            except:
                path = "a"
                print("HERE")
                print(filename) # This is the reject code that pipes to the next line

            if ((len(path) < 3) or (len(path)>150)):
                path = "REJECT"
                return(None)
            else:
                path = path.replace("%2f", ":")
                path = path.replace(" ", "_")
                path = "Curlie" + path[2:None] # The third try also needs to be cleaned
        else:
            return(None)
    return(path)



if __name__ == "__main__":
    ls = os.listdir("./")
    #ls = ["sites.txt"] (Useful for testing)
    tcats, tsites, twiki = 0, 0, 0
    
    f = open("log.txt", "r")
    done = f.readlines()
    f.close()

    for f in ls:
        if "sites" in f and (f+"\n" not in done):
            print("name: ", f)
            print("wiki, cat, site, true cat, true site, true wiki")
            parsed = parse(f)
            print(parsed)
            #print("true cat, true site, true wiki")
            #print(parsed[3], ",", parsed[4], ",", parsed[5])
            tcats += parsed[3]
            tsites += parsed[4]
            twiki += parsed[5]
            print("cats, sites, wiki totals: ", tcats, tsites, twiki)
            print("\n\n\n")
            with open("log.txt", 'a') as log:
                log.write(f+"\n")
    print("cats, sites, wiki totals: ", tcats, tsites, twiki)


