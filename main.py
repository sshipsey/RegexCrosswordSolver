from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
import rstr
import re

site = 'https://regexcrossword.com/challenges/tutorial/puzzles/1'

browser = webdriver.PhantomJS()
browser.get(site)
pageSoup = BeautifulSoup(browser.page_source, "html.parser")
vertClueSoup = pageSoup.find_all(re.compile('th'), class_ = "clue")
horizClueSoup = pageSoup.find_all(re.compile('div'), class_ = "clue")

            
# Parse strings for horiz and vertical
horizClues = [ tag.contents[0] for soup in horizClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]
vertClues = [ tag.contents[0] for soup in vertClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]

print(horizClues)
print(vertClues)