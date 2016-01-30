from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
import itertools
import re

class Solver:
    site = 'https://regexcrossword.com/challenges/tutorial/puzzles/1'
    characterSet = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    browser = webdriver.PhantomJS()
    browser.get(site)
    pageSoup = BeautifulSoup(browser.page_source, "html.parser")
    vertClueSoup = pageSoup.find_all(re.compile('th'), class_ = "clue")
    horizClueSoup = pageSoup.find_all(re.compile('div'), class_ = "clue")

    # Parse strings for horiz and vertical
    horizClues = [ tag.contents[0] for soup in horizClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]
    vertClues = [ tag.contents[0] for soup in vertClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]

    def solve(self):

        # For every square in the grid
        for x, hc in enumerate(self.horizClues):
            for y, vc in enumerate(self.vertClues):
                print(self.getVal(x, y))

    def getVal(self, x, y):
        print(self)
        # Create a new generator for all possible string combinations at length
        verticalPerms = itertools.permutations(list(self.characterSet), len(self.vertClues))
        horizontalPerms = itertools.permutations(list(self.characterSet), len(self.horizClues))
            
        # Compile the regex for this square
        hre = re.compile(self.horizClues[x])
        vre = re.compile(self.vertClues[y])

        hp, _ = itertools.tee(horizontalPerms)
        vp, vp_b = itertools.tee(verticalPerms)     
                
        # For every possible combination of strings in vertical and horizontal perms
        for hstr in hp:
            vp, vp_b = itertools.tee(vp)
            for vstr in vp_b:
                if (hre.match("".join(list(hstr))) and vre.match("".join(list(vstr)))):
                    retVal = "Solution = " + str(list(hstr)[x])
                    return retVal
              
s = Solver()
s.solve()