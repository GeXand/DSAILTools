#Simple scraper for addictionrecoveryguide.org
#Uses the pain pills page and scrapes all the first page posts into an .xlsx file

import requests
import urllib.request
from bs4 import BeautifulSoup
import time
import xlsxwriter
from pathlib import Path
from nltk import tokenize

start = time.time()

#Dummy test url for now
url = "https://www.addictionrecoveryguide.org/message_board/index.php?s=d67a941c556e74c46aaf884b6ed4eaf5&act=SF&f=19"
response = requests.get(url)

#Get all a tags marked as forum post links
soup = BeautifulSoup(response.text, "html.parser")
linkTags = soup.find_all("a", "linkthru")

#Get all links from relevant a tags
#Can probably find a way to optimize the change from html entity to a string
links = []
for linkTag in linkTags:
    link = linkTag['href']
    links.append(link)

#print("\n".join(map(str, links)))
print("Retrieved " + str(len(links)) + " links")

allPostTags = []
#Go to each link and prepare to scrape each page
for link in links:
    curSoup = BeautifulSoup(requests.get(link).text, "html.parser")
    #Get all tags that contain user posts
    postTags = curSoup.find_all("span", "postcolor")
    allPostTags.append(postTags)

#Get all user posts as strings
posts = []
for postTags in allPostTags:
    for postTag in postTags:
        posts.append("".join(postTag.findAll(text=True)))

#Remove trash generated from signatures
for post in posts:
    if "html" in post:
        posts[posts.index(post)] = post[:post.index("html")]

#Check that everything got scraped alright
#print("\n".join(posts))

splitPosts = []
#Split everything by sentence
for post in posts:
    splitPosts.append(tokenize.sent_tokenize(post))

#Create an excel file to store the posts
path = Path("C:/Users/xande/Documents/DSAIL")
postsBook = xlsxwriter.Workbook(path / "scrapeTest.xlsx")
postsSheet = postsBook.add_worksheet()

cell_format = postsBook.add_format({"text_wrap" : True})
postsSheet.set_column(2, 2, 80, cell_format)

postsSheet.write(0, 0, "Primary")
postsSheet.write(0, 1, "Secondary")
postsSheet.write(0, 2, "Reviews")

col = 2
row = 1

for splitPost in splitPosts:
    for post in splitPost:
        postsSheet.write(row, col, post)
        row += 1

postsBook.close()

end = time.time()
print("Time elapsed: " + str(end - start) + " seconds")
print("Sentences scraped: " + str(row))