#Simple scraper for addictionrecoveryguide.org
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
url = "https://www.addictionrecoveryguide.org/message_board/index.php?s=d67a941c556e74c46aaf884b6ed4eaf5&act=SF&f=19"
response = requests.get(url)

#Get all a tags marked as forum post links
soup = BeautifulSoup(response.text, "lxml")
linkTags = soup.find_all("a", "linkthru")

#Get all links from relevant a tags
#Can probably find a way to optimize the change from html entity to a string
links = scrap.linksFromTags(linkTags)

#print("\n".join(map(str, links)))
print("Retrieved " + str(len(links)) + " links")

allPostTags = []
#Go to each link and prepare to scrape each page
for link in links:
    curSoup = BeautifulSoup(requests.get(link).text, "lxml")
    #Get only the first tag that contains a user post
    #Most replies don't give the information we need so we just visit the first link
    postTag = curSoup.find("span", "postcolor")
    allPostTags.append(postTag)

#Get all user posts as strings
posts = scrap.postTagsToStrings(allPostTags)

#Remove trash generated from signatures
for post in posts:
    if "html" in post:
        posts[posts.index(post)] = post[:post.index("html")]
    elif "Signature" in post:
        posts[posts.index(post)] = post[:post.index("Signature")]

#Check that everything got scraped alright
#print("\n".join(posts))

splitPosts = []
#Split everything by sentence
for post in posts:
    splitPosts.append(tokenize.sent_tokenize(post))

#Create an excel file to store the posts
postsBook, postsSheet = scrap.createDSAILsheet("argScrape.xlsx")

scrap.postListToSheet(splitPosts, postsSheet)

postsBook.close()

end = time.time()
print("Time elapsed: " + str(end - start) + " seconds")