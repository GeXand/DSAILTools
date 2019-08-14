import xlsxwriter
from pathlib import Path
from nltk import tokenize

#Gets a list of links from a list of Tag objects
def linksFromTags(linkTags):
    links = []
    for linkTag in linkTags:
        link = linkTag['href']
        links.append(link)
    return links

#Gets a list of posts as strings rather than tag objects
def postTagsToStrings(postTags: list):
    posts = []
    for postTag in postTags:
        posts.append("".join(postTag.findAll(text=True)))
    return posts

def splitPostBySentence(posts: list):
    splitPosts = []
    for post in posts:
        splitPosts.append(tokenize.sent_tokenize(post))
    return splitPosts

#Builds a sheet formatted for coding
def createDSAILsheet(name: str):
    # Create an excel file to store the posts
    path = Path("C:/Users/xande/Documents/DSAIL")
    postsBook = xlsxwriter.Workbook(path / name)
    postsSheet = postsBook.add_worksheet()

    cell_format = postsBook.add_format({"text_wrap": True})
    postsSheet.set_column(2, 2, 80, cell_format)

    postsSheet.write(0, 0, "Primary")
    postsSheet.write(0, 1, "Secondary")
    postsSheet.write(0, 2, "Reviews")

    return postsBook, postsSheet

#Takes a list of posts (split into lists of sentences) and puts them in a .xlsx worksheet
def postListToSheet(l: list, sheet: xlsxwriter.Workbook.worksheet_class):
    col = 2
    row = 1
    for post in l:
        for sentence in post:
            if post.index(sentence) == 0:
                sheet.write(row, col, '"' + sentence)
            elif post.index(sentence) == len(post) - 1:
                sheet.write(row, col, sentence + '"')
            else:
                sheet.write(row, col, sentence)



            row += 1

    print("Sentences scraped: " + str(row))

#Prints any sort of list
def printList(l: list):
    print("\n".join(map(str, l)))