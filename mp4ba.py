#coding: utf-8
import os
import requests

from bs4 import BeautifulSoup

class Movie(object):
    def __init__(self):
        self.links = [] # all links in one page
        self.info = [] # name, size
        self.path = u'E:\\download\\film\\Torrent' # my own path
        self.payload = {'page': 1} # start page
        self.left = "http://www.mp4ba.com/index.php?" 

    def get_magnet_torrent(self, title, url):
        # set file name
        file_name = title + u'.torrent'
        file_name = os.path.join(self.path, file_name)
        
        # send a request
        r = requests.get(url)
        
        if r.status_code == 200:
            # find the magnet and torrent
            soup = BeautifulSoup(r.content, "html.parser")
            magnet = soup.find_all("a", {"id": "magnet"})[0]['href']
            torrent = soup.find_all("a", {"id": "download"})[0]['href']
            torrent = "http://www.mp4ba.com/" + torrent

            # download torrent
            print 'downloading...',title.encode('utf-8') + '.torrent'
            r = requests.get(torrent)
            if r.status_code == 200:
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 1024):
                        f.write(chunk)

            return magnet

    # get path
    def get_path(self):
        path = raw_input('Enter path(like C:\\img) > ')
        path = path.strip()
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path.decode('utf-8')

    # get information on no page_index page
    def get_page(self, page_index):
        self.info = []
        self.links = []
        self.payload['page'] = page_index

        # send a requests
        r = requests.get(self.left, params= self.payload)
        soup = BeautifulSoup(r.content, 'html.parser')

        body = soup.find_all('tbody', {"class":"tbody"})[0]
        children = body.findChildren('a', {"target": "_blank"})

        for elm in children:
            name = elm.text.strip()
            link = "http://www.mp4ba.com/" + elm['href']
            size = elm.find_next().text
            self.info.append([name, size])
            self.links.append(link)

    # print the information[file_name, size]
    def prettify(self):
        index = 0
        for elm in self.info:
            print "%d. " % index,
            print elm[0].encode('utf-8'), elm[1].encode('utf-8')
            print
            index += 1

    def run(self):
        page_index = 0
        self.get_path()
        while True:
            self.get_page(page_index)
            self.prettify()
            print 'G: go to next page'
            print 'Q: quit'
            print 'number: download'
            choice = raw_input('> ').strip()
            if choice.isdigit():
                while True:
                    url = self.links[int(choice)]
                    title = self.info[int(choice)][0]
                    
                    print self.get_magnet_torrent(title, url)

                    choice_temp = raw_input('Continue this page(Y/N)> ').strip()
                    if choice_temp.lower() == 'n':
                        break
                    else:
                        choice = raw_input('Enter number>').strip()
                page_index += 1

            elif choice.lower() == 'g':
                page_index += 1
            else:
                break


if __name__ == "__main__":
    a = Movie()
    a.run()