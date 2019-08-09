#Simple scraper for drugs-forum.com
#Uses the opiate and opioid addiction page and scrapes all the posts into an .xlsx file

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
url = "https://drugs-forum.com/forums/opiate-opioid-addiction.281/"
response = requests.get(url)

#Get all a tags marked as forum post links
soup = BeautifulSoup(response.text, "html.parser")
linkTags = soup.find_all("a", "PreviewTooltip")

#Get all links from relevant a tags
#Can probably find a way to optimize the change from html entity to a string
links = scrap.linksFromTags(linkTags)

#Remove pinned threads since they aren't typical individual user posts
for x in range(6):
    links.pop(0)

scrap.printList(links)
print("Retrieved " + str(len(links)) + " links")

allPostTags = []
#Go to each link and prepare to scrape each page
for link in links:
    curSoup = BeautifulSoup(requests.get("https://drugs-forum.com/" + link).text, "html.parser")
    #Get only the first tag that contains a user post
    #Most replies don't give the information we need so we just visit the first link
    postTag = curSoup.find("blockquote", "messageText")
    allPostTags.append(postTag)

#Get all user posts as strings
posts = scrap.postTagsToStrings(allPostTags)

#Strip out random new line junk cause of site formatting
for i in range(len(posts)):
    posts[i] = posts[i].strip("\n")

splitPosts = scrap.splitPostBySentence(posts)

#Create an excel file to store the posts
postsBook, postsSheet = scrap.createDSAILsheet("dfScrape.xlsx")

scrap.postListToSheet(splitPosts, postsSheet)

postsBook.close()

end = time.time()
print("Time elapsed: " + str(end - start) + " seconds")