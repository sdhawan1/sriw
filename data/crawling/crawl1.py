
# Here, I will try to code a web crawler to extract data from George Washington's papers...

from bs4 import BeautifulSoup
import urllib2
import re
import time
import os.path
import sys

#does a basic, first-run crawl of the website of whatever president you want on the "rotunda" website.
# for Washington, the papers are structured differently, requiring multiple runs of the "basic crawl"
def BasicCrawl(urlin):
    #this website is for George Washington's main papers (called "Papers of GW").
    response = urllib2.urlopen(urlin).read()

    #now, turn the respose string into a beautiful soup, and find all the links
    soup = BeautifulSoup(response, 'html.parser')

    links = soup.find_all('a')
    #base_url: base url from which all queries are done...
    base_url = 'http://rotunda.upress.virginia.edu/founders/default.xqy'
    for l in links:
        label = l.string
        if label is not None:
            if label.find('Volume') >= 0: #(find returns -1 if it fails)
                print base_url + l['href']


#does a second-run crawl of (Volume) links retrieved in the first run. This time, all the links retrieved should point to the text we want.
def SecondCrawl(urlfname):
    urls = open(urlfname).read()
    urls = urls.split()
    for turl in urls:

        #now that we have assembled the targets, we need to scan them and print all the urls inside.
        response = urllib2.urlopen(turl).read()
        soup = BeautifulSoup(response, 'html.parser')
        
        links = soup.find_all('div', class_='TOC')[0].find_all('a')
        nonecounter = 0
        for l in links:
            if l.string is not None:
                print l.string.encode('utf8'),
            else:
                print "none " + str(nonecounter),
                nonecounter += 1

            print l['href']

            #The below may be OK at some point, but there is too much noise coming from too many sources, so for now I just want to scrape all data.
            """
            label = l.string
            if label is not None:
                if label[0:3] == "To " or label[0:5] == "From ": #this tag means it has to be a letter written by or to Adams directly.
                    print label
                elif label.find("John Adams") >= 0: #this also means it must be addressed to or from John Adams (although this will create some noise...)
                    print label                    
            """     

        #just do one for now...
        #break

#this time, take get the responses from our urls and store them all in a new folder
def ThirdCrawl(urlfname, urlbase, location):
    urls = open(urlfname).read()
    urls = urls.split('\n')
    urlctr = 0
    for u in urls:
        #before doing anything, check if file exists. If not, then skip
        if ( os.path.isfile(location + 'washington_' + str(urlctr)) ):
            print urlctr,
            urlctr += 1
            continue

        linearr = u.split(' ')

        turl = urlbase + linearr[-1]
        
        try:
            response = urllib2.urlopen(turl).read()
        except:
            print "Error with file " + str(urlctr)
            print sys.exc_info()[0]
            urlctr += 1
            continue

        if response is not None:
            f = open(location+'washington_'+str(urlctr), 'w')
            line0 = (' ').join(linearr[:-1])
            f.write(line0 + '\n')
            f.write( unicode(response, errors = 'ignore') )
            urlctr += 1

        #before looping, wait for 30 seconds - politeness
        time.sleep(30)

        #start with just one...
        #break
        
    

#main: call the above functions as necessary.

## First step: basic crawl. [Gets links of "volumes"]
"""
## for washigton, there are multiple links that need to be crawled.
# Colonial series:
BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=GEWN-print-02&mode=TOC')
# Revolutionary war series:
BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=GEWN-print-03&mode=TOC')
# Confederation series:
BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=GEWN-print-04&mode=TOC')
# Presidential series:
BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=GEWN-print-05&mode=TOC')
# Retirement series:
BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=GEWN-print-06&mode=TOC')
"""

## Second step: crawl the results of step 1 (which have been manually modified and are in the "temp_wash" file)
#SecondCrawl("temp_washington")

## Third step: crawl the huge list of URLs from step 3 (and eventually store them all in separate files)
urlbase = "http://rotunda.upress.virginia.edu/founders/default.xqy"
ThirdCrawl("washington_links", urlbase, './washington/')
