import xlsxwriter
from pathlib import Path

#Gets a list of links from a list of Tag objects
def linksFromTags(linkTags):
    links = []
    for linkTag in linkTags:
        link = linkTag['href']
        links.append(link)
    return links

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

def postListToSheet(l: list, sheet: xlsxwriter.Workbook.worksheet_class):
    col = 2
    row = 1
    for post in l:
        for sentence in post:
            sheet.write(row, col, sentence)
            row += 1

    print("Sentences scraped: " + str(row))

def printList(l: list):
    print("/n".join(map(str, l)))