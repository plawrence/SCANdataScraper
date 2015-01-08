'''
Created on Feb 8, 2013

Depends on the following packages:
libxml2 2.6.21 or later   #Not Sure about this
lxml                      #Not Sure about this
BeautifulSoup

A good download site for the packages is: 
http://www.lfd.uci.edu/~gohlke/pythonlibs/

Or you can wrangle easy_install/pip if desired


@author: patrick.lawrence
plawrencenw@gmail.com
'''
import urllib2
import urllib
import BeautifulSoup
import re

headers = {'Host': 'www.wcc.nrcs.usda.gov',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.wcc.nrcs.usda.gov/nwcc/site?sitenum=2121&state=mt',
    'Cookie': 'style=null',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '131'
}

url = 'http://www.wcc.nrcs.usda.gov/nwcc/view HTTP/1.1'

#Leave day blank if you want all the days in a month.  
#Set month = "CY" if you want the whole year - otherwise set it to 01-12
#Set Day to 01 - 31 or leave it blank if you want the whole month
#If you want a specific hour, use the following format: Hour%3A00
#Set report = "ALL" at your own peril - the code needs altering to handle this
#Set timeseries = "Daily" or "Hourly"
def requestSCANData(sitenum,timeseries,year,month,interval="MONTH", report="ALL",day=""):
    
    values = {'intervalType' : '+View+Historic+',
              'report' : report,
              'timeseries' : str(timeseries),
              'format' : 'view',
              'sitenum' : str(sitenum),
              'interval' : str(interval),
              'year' : str(year),
              'month' : str(month),
              'day' : str(day),
              'userEmail' : '' }

    data = urllib.urlencode(values)
    print(data)
    if data[-8:-3] == 'month':
        data1 = data[0:10]
        data2 = data[10:-8]
        data3 = data[-8:]
        data = data3 + data2 + data1
    print(data)

    #Make the html POST request
    req = urllib2.Request(url,data,headers)
    print(str(req.get_data()))
    f = urllib2.urlopen(req)
    insoup = f.read()
    

    soup = BeautifulSoup.BeautifulSoup(insoup)
    
    #Find The data table within the html markup
    if report == "SCAN":
        resulttable = soup.findAll(summary=re.compile("Standard"))
    else:
        resulttable = soup.findAll(summary=re.compile("All Sensors"))
    #print(resulttable)
    
    #Parse the data into a list of lists
    datalist = []
    for row in resulttable[0].findAll('tr'):
        rowsplit = row.findAll(text=True)
        rowsplit = [x.encode('UTF-8') for x in rowsplit]
        datalist.append(rowsplit)

    #Remove the last header
    datalist.pop()
    return datalist

#Write to an output file
def writetable(datalist,outfilename):
    outfile = open(outfilename,'w')
    for row in datalist:
        outfile.writelines(",".join(row) + "\n")
        
        
    
    