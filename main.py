from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
import itertools
import re

# Python solver for RegexCrossword
# https://regexcrossword.com
class Solver:
    
    # Default constructor
    def __init__(puzzleURL):
        self.puzzleURL = puzzleURL
    
    # Valid character set for string testing against puzzle regex
    characterSet = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    # Create a browser instance and scrape the puzzle from the given URL
    browser = webdriver.PhantomJS()
    browser.get(puzzeURL)
    pageSoup = BeautifulSoup(browser.page_source, "html.parser")
    
    # Find our vertical and horizontal clues and store them in lists
    vertClueSoup = pageSoup.find_all(re.compile('th'), class_ = "clue")
    horizClueSoup = pageSoup.find_all(re.compile('div'), class_ = "clue")

    # Parse strings for horiz and vertical
    horizClues = [ tag.contents[0] for soup in horizClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]
    vertClues = [ tag.contents[0] for soup in vertClueSoup for tag in soup.contents if type(tag) == Tag and len(tag.contents) > 0 ]

    # Method to solve an entire puzzle
    def solve(self):
    
        # For every square in the grid
        for y, vc in enumerate(self.vertClues):
            for x, hc in enumerate(self.horizClues):
                print(self.getVal(x, y))

    # Method to solve the character for a x,y location
    def getVal(self, x, y):
        
        # Create a new generator for all possible string combinations at length
        verticalPerms = itertools.permutations(list(self.characterSet), len(self.vertClues))
        horizontalPerms = itertools.permutations(list(self.characterSet), len(self.horizClues))
        
        # Compile the regex for this square
        hre = re.compile('^' + self.horizClues[x] + '$')
        vre = re.compile('^' + self.vertClues[y] + '$')

        # Make a copy of the generators so we can iterate over them multiple times
        hp, hp_b = itertools.tee(horizontalPerms)
        vp, _ = itertools.tee(verticalPerms)     
                
        # For every possible combination of strings in vertical and horizontal perms
        for vstr in vp:
            hp, hp_b = itertools.tee(hp)
            for hstr in hp_b:
            
                # If we find an intersection of strings that match the regex, return the hstr[x] for that string as the answer
                if (list(hstr)[x] == list(vstr)[y] and hre.match("".join(list(hstr))) and vre.match("".join(list(vstr)))):
                    retVal = "Solution (" + str(x) + "," + str(y) + ") = " + str(list(hstr)[x])
                    return retVal
                    
        # This should never happen for a valid puzzle, no intersection found
        return "Solution (" + str(x) + "," + str(y) + ") Not found"

# Create a solver and solve
s = Solver('https://regexcrossword.com/challenges/tutorial/puzzles/4')
s.solve()