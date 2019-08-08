#Simple scraper for drugabuse.com
#Uses the pain pills page and scrapes all the first page posts into an .xlsx file

import requests
import urllib.request
from bs4 import BeautifulSoup
import time
import xlsxwriter
from pathlib import Path
from nltk import tokenize
import scrapers.scrapeUtils as scrap

start = time.time()

#Dummy test url for now
url = "https://talk.drugabuse.com/forums/prescription-drugs.72/"
response = requests.get(url)

#Get all a tags marked as forum post links
soup = BeautifulSoup(response.text, "html.parser")
linkTags = soup.find_all("a", "PreviewTooltip")

#Get all links from relevant a tags
#Can probably find a way to optimize the change from html entity to a string
links = []
for linkTag in linkTags:
    link = linkTag['href']
    links.append(link)

scrap.printList(links)
print("Retrieved " + str(len(links)) + " links")