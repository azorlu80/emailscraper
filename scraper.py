#yüklenecek paketler
#pip3 install beautifulsoup4
#pip3 install requests
#pip3 install lxml

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import os,sys
user_url = input("[+]Enter target URL to scan : ")
urls = deque([user_url])

scrapped_urls = set()
emails = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        #urls listenin başından bir tane url al!    
        url = urls.popleft() #{'http://www.google.com'}
        #almış olduğum bu url li scrapped_urls set ine ekle
        scrapped_urls.add(url)   

        parts = urllib.parse.urlsplit(url) 
        #SplitResult(scheme='http', netloc='www.google.com', path='', query='', fragment='')
        base_url = "{0}://{1}".format(parts.scheme,parts.netloc)

        path=url[:url.rfind("/")+1] if "/" in parts.path else url
        print("path : ",path)
        print("[%d] Processing %s" %(count, url))

        try:
            response = requests.get(url)

        except(requests.exceptions.MissingSchema,requests.exceptions.ConnectionError()):

         continue
        #print(response.text) 
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
     
        #print(re.findall(regex, response.text))
        new_emails =   set(re.findall(regex, response.text))  
        #print(new_emails)
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs else ""
           #print("all links : ",link)
            if link.startswith("/"):
              link = base_url + link
            #ornek link /contact şeklinde başlıyor ve link = http://www.sample.com + /contact oluyor.
            elif not link.startswith("http"):
            # link sample2 şeklinde başlıyor bu durumunda link = http://www.sample.com/sample1/sample2 oluyor.
              link = path + link
            #link urls deque listemizde yok ve url scraped_urls set imizde yok ise
            if not link in urls and not link in scrapped_urls:
                urls.append(link)       

except KeyboardInterrupt:
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
        print("[-] Closing!")
    
for mail in emails:
    print(mail)