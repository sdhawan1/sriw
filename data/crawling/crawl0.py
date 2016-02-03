
# Here, I will try to code a web crawler to extract data from John Adams' papers

# run: python crawl0.py > temp_links #(input is temp, do crawl 1)
# then run: python crawl0.py > jeff_links #(input is temp / temp_jeff recursively)
#   at final layer, move temp_jeff into jeff_links.
# finally, run: python crawl0.py #(input is jeff_links, output is several files in folder "jefferson")

from bs4 import BeautifulSoup
import urllib2
import re
import time
import os.path
import sys

#does a basic, first-run crawl of the website of whatever president you want on the "rotunda" website.
def BasicCrawl(urlin):
    #this website is for John Adams' main papers (called "Papers of John Adams").
    response = urllib2.urlopen(urlin).read()

    #now, turn the respose string into a beautiful soup, and find all the links
    soup = BeautifulSoup(response, 'html.parser')

    links = soup.find_all('a')
    for l in links:
        label = l.string
        if label is not None:
            if label.find('Volume') >= 0: #(find returns -1 if it fails)
                print l['href']


#does a second-run crawl of (Volume) links retrieved in the first run. This time, all the links retrieved should point to the text we want.
#have to run this [multiple times] until we get to the final layer of links. We will then use ThirdCrawl on this final link layer.
def SecondCrawl(urlfname, urlbase):
    urls = open(urlfname).read()
    urls = urls.split()
    for u in urls:
        turl = urlbase + u

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
        if ( os.path.isfile(location + 'jefferson_' + str(urlctr)) ):
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
            f = open(location+'jefferson_'+str(urlctr), 'w')
            line0 = (' ').join(linearr[:-1])
            f.write(line0 + '\n')
            f.write( unicode(response, errors = 'ignore') )
            urlctr += 1

        #before looping, wait for 30 seconds - politeness
        time.sleep(30)

        #start with just one...
        #break
        
    

#main: call the above functions as necessary.

## First step: basic crawl (should go into file "temp".
#BasicCrawl('http://rotunda.upress.virginia.edu/founders/default.xqy?keys=TSJN-print-01&mode=TOC')

## Second step: crawl the results of step 1 (which have been manually modified and are in the "temp_adams" file)
urlbase = "http://rotunda.upress.virginia.edu/founders/default.xqy"
#SecondCrawl("temp_jeff", urlbase)

## Third step: crawl the huge list of URLs from step 3 (and eventually store them all in separate files)
ThirdCrawl("jeff_links", urlbase, './jefferson/')
