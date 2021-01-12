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

allPostTags =[]

for i in range(1, 6):
    url = "https://drugs-forum.com/forums/opiate-opioid-addiction.281/page-" + str(i)
    response = requests.get(url)

    # Get all a tags marked as forum post links
    soup = BeautifulSoup(response.text, "lxml")
    linkTags = soup.find_all("a", "PreviewTooltip")

    # Get all links from relevant a tags
    # Can probably find a way to optimize the change from html entity to a string
    links = scrap.linksFromTags(linkTags)

    # Remove pinned threads since they aren't typical individual user posts

    if i == 1:
        for x in range(6):
            links.pop(0)

    scrap.printList(links)
    print("Retrieved " + str(len(links)) + " links")

    # Go to each link and prepare to scrape each page
    for link in links:
        curSoup = BeautifulSoup(requests.get("https://drugs-forum.com/" + link).text, "lxml")
        # Get only the first tag that contains a user post
        # Most replies don't give the information we need so we just visit the first link
        postTag = curSoup.find("blockquote", "messageText")
        allPostTags.append(postTag)

    time.sleep(0.2)

# Get all user posts as strings
posts = scrap.postTagsToStrings(allPostTags)

# Strip out random new line junk cause of site formatting
for i in range(len(posts)):
    posts[i] = posts[i].strip("\n")

splitPosts = scrap.splitPostBySentence(posts)

#Create an excel file to store the posts
postsBook, postsSheet = scrap.createDSAILsheet("dfScrape.xlsx")

scrap.postListToSheet(splitPosts, postsSheet)

postsBook.close()

end = time.time()
print("Time elapsed: " + str(end - start) + " seconds")