import requests
from bs4 import BeautifulSoup
import os

class ScrapingSite:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
            }
        )
        self.request = self.session.get('http://auto.drom.ru/all/page1')
        self.soup = BeautifulSoup(self.request.text, "lxml")
    def getEveryLink(self):
        list_link = []
        first_link = "http://auto.drom.ru/all/page1"
        page = 1

        while page < 100:
            try:
                newLink = first_link[:-1] + str(page)
                self.request = self.session.get(newLink)
                self.soup = BeautifulSoup(self.request.text, "lxml")
                if(self.request.status_code == 200):
                    for j in range(20):
                        count_ads_one_page = self.soup.find('div', {'class': 'b-media-cont b-media-cont_modifyMobile_sm'}).find('a', {'name': int('1') + j}).get('href')
                        list_link.append(count_ads_one_page)
                        print(count_ads_one_page)
                else:
                    status_code_link = 999
                page += 1
            except AttributeError:
                break
        self.getImage(list_link)

    def getImage(self, list_link):
        countFolder = 0
        for i in range(len(list_link)):
            self.request = self.session.get(list_link[i])
            soup = BeautifulSoup(self.request.text, "lxml")
            carBrand = {'nameCar': 1}
            carBrand['nameCar'] = soup.find('div', {'data-print': 'advert'}).find('h1').get_text()
            print(carBrand['nameCar'])
            path = r'D:\Фото\dromRu\{0}_{1}'.format(carBrand['nameCar'],countFolder)
            os.makedirs(path)
            countPhoto = 1
            while (True):
                try:
                    image = soup.find('a', {'data-image-hash': 'photo' + str(countPhoto)}).get('href')
                    getImg = requests.get(image)
                    if (image != None):
                        f = open(os.path.join(path, self.reversImg(image)), 'wb')
                        f.write(getImg.content)
                        f.close()
                except AttributeError:
                    break
                countPhoto = countPhoto + 1
            countFolder = countFolder + 1

    def reversImg(self,image):
        searchSlash = 0
        idImage = ""
        for j in range(len(image)):
            if (image[len(image) - (j + 1)] != "/"):
                searchSlash += 1
                idImage += image[len(image) - (j + 1)]
            else:
                break
        idImage = idImage[::-1]
        return idImage

def main():
    a = ScrapingSite()
    a.getEveryLink()
if __name__ == '__main__':
    main()

'''from bs4 import BeautifulSoup
import requests
import os

class parseDromRu:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            }
        )
        self.getLink()
    def getLink(self):
        countPage = 1
        listLink = []
        while (True):
            newURL = "http://auto.drom.ru/all/page1"
            newURL = newURL[:-1] + str(countPage)
            URL = self.session.get(newURL)
            if (URL.status_code == 200):
                soup = BeautifulSoup(URL.text, "lxml")
                for i in range(20):
                    try:
                        lint = soup.find('div', {'class': 'b-media-cont b-media-cont_modifyMobile_sm'}).find('a', {
                            'name': {i + 1}}).get('href')
                        listLink.append(str(lint))
                    except AttributeError:
                        break
                countPage = countPage + 1
                if (countPage > 100):
                    break
        self.getImage(listLink)

    def getImage(self, listLink):
        countFolder = 0
        for i in range(len(listLink)):
            URL = self.session.get(listLink[i])
            soup = BeautifulSoup(URL.text, "lxml")
            path = r'D:\image\DromRu\Car_{0}'.format(countFolder)
            os.makedirs(path)
            countPhoto = 1
            while (True):
                try:
                    underImg = soup.find('a', {'data-image-hash': 'photo' + str(countPhoto)}).get('href')
                    getImg = requests.get(underImg)
                    if (underImg != None):
                        f = open(os.path.join(path, underImg.split('/')[-1]), 'wb')
                        f.write(getImg.content)
                        f.close()
                except AttributeError:
                    break
                countPhoto = countPhoto + 1
            countFolder = countFolder + 1
a = parseDromRu()
'''