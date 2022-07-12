# source:
# https://github.com/tseth92/web-scraper
# MIT License

# Highly simplified from the source

import requests

def get_data(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get(url, headers=headers)#, proxies=proxies) (I could never get those proxies working).
    content = r.content
    #print(content[:100])
    return(str(content))

if __name__ == "__main__":
    with open('data.txt', 'w') as data:
        data.write(get_data("https://www.ipecho.io/plain")+"\n______________\n")
    print("hello, we've done the initial writing!")
    
