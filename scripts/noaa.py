import requests
import getopt
import os
import re
import sys
import xml.etree.ElementTree as ET

from io import StringIO
from bs4 import BeautifulSoup

def stormcarib(name):
    url = 'https://stormcarib.com/'

    r = requests.get(url, timeout = 90)

    html_soup = BeautifulSoup(r.text, 'html.parser')

    for tr in html_soup.find_all('tr'):
        if "tools" in tr.td.text and name.lower() in tr.td.text.lower():
            for a in tr.find_all('a', title='[Spaghetti plots + intensity]'):
                r2 = requests.get("{}{}".format(url, a['href']), timeout = 90)
                html_soup2 = BeautifulSoup(r2.text, 'html.parser')
                return html_soup2.find_all('img')[1]['src']

    return "NA"

def nesdis(center):
    def nesdisLatLon(url):
        return [float(x) for x in re.split('.*lat=(\d+)\w\&lon=(\d+)\w', url) if x != '']

    def nhcLatLon(center):
        return [float(x) for x in re.split('(\d+\.\d+)\,\s\-(\d+\.\d+)', center) if x != '']

    def compareLatLon(nhc, nesdis, rang = 5):
        return nesdis[0] - rang <= nhc[0] <= nesdis[0] + rang and nesdis[1] - rang <= nhc[1] <= nesdis[1] + rang

    url = 'https://www.star.nesdis.noaa.gov/GOES/'

    nhclatlon = nhcLatLon(center)

    r = requests.get("{}{}".format(url,'MESO_index.php'), timeout = 90)

    html_soup = BeautifulSoup(r.text, 'html.parser')

    for ul in html_soup.find('div', id='tab1').find_all('ul', class_='mesoItems'):
        for li in ul.find_all('li'):
            if compareLatLon(nhclatlon, nesdisLatLon(li.a['href'])):
                r2 = requests.get("{}{}".format(url, li.a['href']), timeout = 90)
                html_soup2 = BeautifulSoup(r2.text, 'html.parser')

                for tb in html_soup2.find_all('div', class_='TNBox'):
                    if 'Band 13' in tb.a['title']:
                        return tb.a['href']

    return "NA"

def getInfo(url):
    def degrees(direction):
        compass = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
        return compass.index(direction) * 22.5

    r = requests.get(url, timeout = 90)

    tree = ET.iterparse(StringIO(r.text))
    for _, el in tree:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

    root = tree.root

    for c in root.iter('Cyclone'):
        hurracane = {}

        center = c.find('center').text.strip().split(',')
        movement = c.find('movement').text
        name = c.find('name').text
        atcf = c.find('atcf').text

        hurracane['datetime'] = '"{}"'.format(c.find('datetime').text)
        hurracane['wallet'] = '"{}"'.format(c.find('wallet').text)
        hurracane['atcf'] = '"{}"'.format(c.find('atcf').text)
        hurracane['name'] = '"{}"'.format(c.find('name').text)
        hurracane['type'] = '"{}"'.format(c.find('type').text)
        hurracane['lat'] = center[0].replace(' ','')
        hurracane['lng'] = center[1].replace(' ','')
        hurracane['pressure'] = c.find('pressure').text.split(' ')[0]
        hurracane['wind'] = c.find('wind').text.split(' ')[0]
        hurracane['direction'] = '"{}"'.format(movement.split(' at ')[0])
        hurracane['speed'] = movement.split(' at ')[1].replace(' mph','')
        hurracane['degrees'] = degrees(movement.split(' at ')[0])
        hurracane['headline'] = '"{}"'.format(c.find('headline').text.strip().replace('...','').replace('"',''))

        hurracane['img-5day'] = '"NA"'
        hurracane['img-wind'] = '"NA"'

        for child in root.iter('item'):
            if('Graphics' in child.find('title').text and hurracane['name'].replace('"','') in child.find('title').text):
                html_soup = BeautifulSoup(child.find('description').text, 'html.parser')
                for img in html_soup.find_all('img'):
                    if '5day' in img['src']: hurracane['img-5day'] = '"{}"'.format(img['src'])
                    if 'wind' in img['src']: hurracane['img-wind'] = '"{}"'.format(img['src'])

        hurracane['stormcarib'] = '"{}"'.format(stormcarib(hurracane['name'].replace('"','')))
        hurracane['nesdis'] = '"{}"'.format(nesdis(c.find('center').text))

        info = ",".join(["{}={}".format(key, value) for key, value in hurracane.items()])
        print("noaa,name={} {}".format(atcf, info))

def main():
    url = None

    opts, args = getopt.getopt(sys.argv[1:], 'u:', ['url='])

    if not opts:
	    usage()
	    sys.exit(1)

    for opt, arg in opts:
        if opt in ('-u', '--url'):
            url = arg

    if url is None:
        usage()

    getInfo(url = url)

def usage():
    print("Usage: {} -u <url>".format(sys.argv[0]))
    sys.exit(1)

if __name__ == '__main__':
    main()
