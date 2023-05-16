import bs4
import requests
import re

def crawl2(current_page, distance, action, visited):
    if current_page not in visited and distance > 0:
        visited.append(current_page)
        page = requests.get(current_page)
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        res = [(current_page, action(soup.text))]
        for link in soup.find_all('a'):
            l = link.get('href')
            if l is not None and re.match('https?://', l):
                (subres, visited2) = crawl2(l, distance - 1, action, visited)
                visited += visited2
                res += subres
        return (res, visited)
    return (list(),list())

def crawl(start_page, distance, action):
    (res, visited) = crawl2(start_page, distance, action, [])
    return res

# czy na stronie jest zdanie ze słowem 'Python' :

for url, res in crawl("http://www.ii.uni.wroc.pl", 2, lambda text : 'Python' in text):
   print(f"{url}: {res}")

# wypisanie wszystkich zdań ze słowem 'Python' :

# def Python_in_sentences(text):
#     sentences = text.split('.')
#     for s in sentences:
#         if 'Python' in s:
#             print(s, '\n')

# crawl("http://www.ii.uni.wroc.pl", 2, Python_in_sentences)
