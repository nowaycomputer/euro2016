from bs4 import BeautifulSoup
import urllib2
import re

class ELO_Scraper:
    def __init__(self):
        self.elo_url = "http://www.eloratings.net/"
        self.header = {'User-Agent': 'Mozilla/5.0'} 

    def get_all_ratings(self):
        req = urllib2.Request(self.elo_url,headers=self.header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)

        pattern=re.compile('(<td>)\d*<\/td><td><a href="')
        tables = soup.findAll('table')

        rows= str(tables).split("<tr>")
        countries=[]
        ratings=[]
        for r in rows:
            if(pattern.match(r)):
                values=r.split("<td>")
                # get country name
                countries.append(BeautifulSoup(str(values[2]),"html5lib").get_text())
                ratings.append(BeautifulSoup(str(values[3]),"html5lib").get_text())
                #print country, rating
        return dict(zip(countries, ratings))