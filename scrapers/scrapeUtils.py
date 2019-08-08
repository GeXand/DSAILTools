import xlsxwriter
from pathlib import Path

#Gets a list of links from a list of Tag objects
def links_from_tags(linkTags):
    links = []
    for linkTag in linkTags:
        link = linkTag['href']
        links.append(link)
    return links

def createDSAILsheet(name: str):
    # Create an excel file to store the posts
    path = Path("C:/Users/xande/Documents/DSAIL")
    postsBook = xlsxwriter.Workbook(path / name + ".xlsx")
    postsSheet = postsBook.add_worksheet()

    cell_format = postsBook.add_format({"text_wrap": True})
    postsSheet.set_column(2, 2, 80, cell_format)

    postsSheet.write(0, 0, "Primary")
    postsSheet.write(0, 1, "Secondary")
    postsSheet.write(0, 2, "Reviews")

    return postsBook

def printList(l: list):
    print("/n".join(map(str, l)))