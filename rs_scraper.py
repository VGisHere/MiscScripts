from bs4 import BeautifulSoup
import requests
import shutil
import sys
import datetime
import trafilatura

pages_crawled = {}
recursion_level = 1

# Recursive Method
def recursive_crawler(url):
    global pages_crawled, recursion_level

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')

    sys.stdout = open('rs_logs.txt', "a")
    
    for link in links:
        if 'href' in link.attrs:
            if 'revisesociology' in link['href'] and \
                link['href'].startswith('http') and \
                not 'sellfy' in link['href'] and \
                link['href'] != 'https://revisesociology.com':
                if link['href'] not in pages_crawled:
                    print(recursion_level, link['href'])
                    pages_crawled[link['href']] = True
                    if 'i0.wp.com' in link['href']:
                        res = requests.get(link['href'], stream=True)
                        if res.status_code == 200:
                            file_name = link['href'][link['href'].rfind(
                                '/')+1:link['href'].rfind('?')]
                            try:
                                with open(file_name, 'wb') as f:
                                    shutil.copyfileobj(res.raw, f)
                            except:
                                print(file_name)
                    else:
                        try:
                            recursion_level += 1
                            recursive_crawler(link['href'])
                            recursion_level -= 1
                        except:
                            continue


# Iterative Method
def iterative_crawler(url):
    global pages_crawled, recursion_level, queue

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')

    sys.stdout = open('rs_logs.txt', "a")

    queue = []
    
    queue.extend(links)
    
    while queue:
        print("Queue Length :", len(queue), end='')
        link = queue.pop(0)
        if 'href' in link.attrs:
            if 'revisesociology' in link['href'] and \
                    link['href'].startswith('http') and \
                    not 'sellfy' in link['href'] and \
                    link['href'] != 'https://revisesociology.com' and \
                    not '#comment' in link['href'] and \
                    not 'com/shop/' in link['href']:
                if link['href'] not in pages_crawled:
                    print(datetime.datetime.now(), link['href'])
                    pages_crawled[link['href']] = True
                    if 'i0.wp.com' in link['href']:
                        res = requests.get(link['href'], stream=True)
                        if res.status_code == 200:
                            file_name = link['href'][link['href'].rfind(
                                '/')+1:link['href'].rfind('?')]
                            try:
                                with open('Images/'+file_name, 'wb') as f:
                                    shutil.copyfileobj(res.raw, f)
                            except:
                                print(file_name)
                    else:
                        try:
                            try:
                                page_content = trafilatura.extract(trafilatura.fetch_url(
                                                            link['href']))
                                file_name = link['href'].split('/')[-2] + '.txt'
                                if page_content and file_name[:-3] and len(page_content) > 625:
                                    with open('TextFiles/'+file_name, 'w') as f:
                                        f.write(page_content)
                            except:
                                pass
                            
                            page = requests.get(link['href'])
                            soup = BeautifulSoup(page.text, 'html.parser')
                            links = soup.find_all('a')
                            queue.extend(links)
                        except:
                            continue

# recursive_crawler('https://revisesociology.com/')
iterative_crawler('https://revisesociology.com/')
