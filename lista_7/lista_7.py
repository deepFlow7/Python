from multiprocessing import Lock
from telnetlib import SE
import bs4
import requests
import re
import threading

class Search:
    def __init__(self):
        self.visited = []
        self.res = []
        self.lock = Lock()
    def crawl2(self, current_page, distance, action):
        self.lock.acquire()
        threads = []
        if current_page not in self.visited and distance > 0:
            self.visited.append(current_page)
            self.lock.release()
            page = requests.get(current_page)
            soup = bs4.BeautifulSoup(page.content, "html.parser")
            self.res.append((current_page, action(soup.text)))
            for link in soup.find_all('a'):
                l = link.get('href')
                if l is not None and re.match('https?://', l):
                    t = threading.Thread(target=self.crawl2, args=(l, distance - 1, action))
                    t.start()
                    threads.append(t)
            for thr in threads:
               t.join() 
        else:
            self.lock.release()
        return
    def crawl(self,start_page, distance, action):
        self.crawl2(start_page, distance, action)
        return self.res

# czy na stronie jest zdanie ze słowem 'Python' :

s = Search()
for url, res in s.crawl("https://ii.uni.wroc.pl/", 2, lambda text : 'Python' in text):
   print(f"{url}: {res}")
