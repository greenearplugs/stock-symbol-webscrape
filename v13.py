
'''so another program could call this by saying import v9...then later on doing v9.getCap(userinput)'''
'''another idea is to take getCap as a symbol input only, not having the input be an entire webpage'''
'''another idea:  combine all the functions into one...so that a user can just enter an symbol, and they get all the data returned'''
'''convert 1.40B into 14000000000 in python...not sql'''
'''python v5.py jim.csv > ouput.txt'''
'''asdf113'''
import urllib
import re
import csv
import time
import datetime
from bs4 import BeautifulSoup
from mechanize import *
import string
import sys

symbolfile = open(sys.argv[1], 'rU')

'''symbolfile = open('companylistALL.csv', 'rU')'''
csv_symbol = csv.reader(symbolfile, dialect=csv.excel_tab,delimiter=",")
stocksymbols = []

for row in csv_symbol:
    stocksymbols.append(row[0])

del stocksymbols[0]
k = 0

def negConverter(number):
    number = number[:-1]
    number = number[1:]
    print float(number)*-1000,
    print ",",

def getCap(keyUrl):
        try:
            cap = keyUrl.findAll('td',{'class':'yfnc_tabledata1'})[0].findAll('span')[0].text
            if cap.endswith('B'):
                cap1 = float(cap[:len(cap)-1])*1000000000
                print cap1,
                print ",",
            if cap.endswith('M'):
                cap1 = float(cap[:len(cap)-1])*1000000
                print cap1,
                print ",",
            if cap.endswith('K'):
                cap1 = float(cap[:len(cap)-1])*1000
                print cap1,
                print ",",
            if cap.endswith('A'):
                print "N/A",
        except:
            print "---1,",

def getEV(keyUrl):
    try:
        ev = keyUrl.findAll('td',{'class':'yfnc_tabledata1'})[1].text
        if ev.endswith('B'):
            ev1 = float(ev[:len(ev)-1])*1000000000
            print ev1,
            print ",",
        if ev.endswith('M'):
            ev1 = float(ev[:len(ev)-1])*1000000
            print ev1,
            print ",",
        if ev.endswith('K'):
            ev1 = float(ev[:len(ev)-1])*1000
            print ev1,
            print ",",
        if ev.endswith('A'):
            print "N/A,",
    except:
        print "---2,",

def getIncome(symbol):
        try:
            soupIncome = BeautifulSoup(urllib.urlopen("http://finance.yahoo.com/q/is?s=" +symbol+ "&annual").read())
            stockName = soupIncome.findAll('div',{'class':'title'})[0].findAll('h2')[0]
            print stockName.text.replace(","," ")+",",
            try:
                print soupIncome('table')[8].findAll('tr')[0].findAll('th')[0].text.replace("\n", "").replace(",","").strip()+",",
                years = len(soupIncome('table')[8].findAll('tr')[0].findAll('th'))
                rows = soupIncome('table')[8].findAll('tr')
                for i in range (0,len(rows)):
                    if len(rows[i].findAll('td')) > years:
                        data = rows[i].findAll('td')[-years].text.replace("\n", "").replace(",","").replace("-","0").strip()
                        try:
                            print float(data)*1000,
                            print ",",
                        except:
                            if data.startswith("("):
                                negConverter(data)

            except:
                print "error code 1,",
        except:
            print "error code 2,",

def getBalance(symbol):
        try:
            soupBalance = BeautifulSoup(urllib.urlopen("http://finance.yahoo.com/q/bs?s=" +symbol+ "+Balance+Sheet&annual").read())
            print soupBalance('table')[8].findAll('tr')[0].findAll('td')[1].text.replace(",","").replace("-","0")+",",
            rows2 = soupBalance('table')[8].findAll('tr')
            years = len(soupBalance('table')[8].findAll('tr')[0])-1
            for i in range (1, len(rows2)):
                if len(rows2[i].findAll('td')) > years:
                    data = rows2[i].findAll('td')[-years].text.replace("\n", "").replace(",","").replace("-","0").strip()
                    try:
                        print float(data)*1000,
                        print ",",
                    except:
                        if data.startswith("("):
                            negConverter(data)
        except:
            print "3333,",

def checkValid(symbol):
    soupBalance = BeautifulSoup(urllib.urlopen("http://finance.yahoo.com/q/bs?s=" +symbol+ "+Balance+Sheet&annual").read())
    rows2 = soupBalance('table')[8].findAll('tr')


while k<len(stocksymbols):
    '''while k< 150:'''

    try:
        checkValid(stocksymbols[k])
        keyUrl = BeautifulSoup(urllib.urlopen("http://finance.yahoo.com/q/ks?s=" + stocksymbols[k]+ "+Key+Statistics").read())
        print stocksymbols[k]+",",
        getCap(keyUrl)
        getEV(keyUrl)
        getIncome(stocksymbols[k])
        getBalance(stocksymbols[k])
        print k,
        print ","
        k+=1
    except:
        k+=1


