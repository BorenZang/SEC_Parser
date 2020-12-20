# Following import is for the Yahoo Finance Financial Statements
import ssl
import smtplib
import datetime
#from datetime import date
#from datetime import time
#from datetime import datetime
import feedparser
import requests
import bs4
import time
import io
import re, requests
import json
import xlsxwriter

#Next is for YF-Stat to get Yahoo Finance Statistics Page information
import os
import sys
import csv
#import bs4
import urllib3
#import xlsxwriter
#from selenium import webdriver
import pdb
#import requests # this is for price retrieving


########Initialize all variables

cash_dataNumber1 = []
cash_dataNumber2 = []
cash_dataNumber3 = []
cash_dataNumber4 = []
date = []
date2 = []

BS_yr_dataNumber1 = []
BS_yr_dataNumber2 = []
BS_yr_dataNumber3 = []
BS_yr_dataNumber4 = []

IS_yr_dataNumber1 = []
IS_yr_dataNumber2 = []
IS_yr_dataNumber3 = []
IS_yr_dataNumber4 = []

cash_qtrs_dataNumber1 = []
cash_qtrs_dataNumber2 = []
cash_qtrs_dataNumber3 = []
cash_qtrs_dataNumber4 = []

BS_qtrs_dataNumber1 = []
BS_qtrs_dataNumber2 = []
BS_qtrs_dataNumber3 = []
BS_qtrs_dataNumber4 = []

IS_qtrs_dataNumber1 = []
IS_qtrs_dataNumber2 = []
IS_qtrs_dataNumber3 = []
IS_qtrs_dataNumber4 = []

Elements = ['Net Income','Depreciation','Adjustments To Net Income','Changes In Accounts Receivables','Changes In Liabilities',
            'Changes In Inventories','Changes In Other Operating Activities','Total Cash Flow From Operating Activities','Capital Expenditures',
            'Investments','Other Cash flows from Investing Activities','Total Cash Flows From Investing Activities','Dividends Paid','Sale Purchase of Stock',
            'Net Borrowings','Other Cash Flows from Financing Activities','Total Cash Flows From Financing Activities','Effect Of Exchange Rate Changes','Change In Cash and Cash Equivalents']

Elements2 = ['Cash And Cash Equivalents','Short Term Investments','Net Receivables','Inventory','Other Current Assets','Total Current Assets',
             'Long Term Investments','Property Plant and Equipment','Goodwill','Intangible Assets','Other Assets','Total Assets',
             'Accounts Payable','Short/Current Long Term Debt','Other Current Liabilities','Total Current Liabilities','Long Term Debt',
             'Other Liabilities','Total Liabilities','Common Stock','Retained Earnings','Treasury Stock','Other Stockholder Equity','Total Stockholder Equity',
             'Net Tangible Assets']

Elements3 = ['Total Revenue','Cost of Revenue','Gross Profit','Research Development','Selling General and Administrative','Total Operating Expenses',
             'Operating Income or Loss','Total Other Income/Expenses Net','Earnings Before Interest and Taxes','Interest Expense','Income Before Tax',
             'Income Tax Expense','Net Income From Continuing Ops','Net Income','Net Income Applicable To Common Shares']




####### Next is for YF-Stat to obtain Yahoo Finance Statistics Page and Stock Price information

key_stats_on_main =['Market Cap']
key_stats_on_stat =['Enterprise Value', 'Trailing P/E', 'Forward P/E',
                     'PEG Ratio (5 yr expected)', 'Price/Sales','Price/Book',
                     'Enterprise Value/Revenue','Enterprise Value/EBITDA',
                     'Fiscal Year Ends','Most Recent Quarter',
                     'Profit Margin','Operating Margin','Return on Assets', 'Return on Equity',
                     'Revenue','Revenue Per Share','Quarterly Revenue Growth','Gross Profit',
                     'EBITDA', 'Net Income Avi to Common','Diluted EPS','Quarterly Earnings Growth',
                     'Total Cash','Total Cash Per Share','Total Debt','Total Debt/Equity', 'Current Ratio', 'Book Value Per Share',
                     'Operating Cash Flow','Levered Free Cash Flow','Beta (3Y Monthly)','52-Week Change','S&P500 52-Week Change',
                     '52 Week High','52 Week Low','50-Day Moving Average','200-Day Moving Average',
                     'Avg Vol (3 month)','Avg Vol (10 day)','Shares Outstanding','Float','% Held by Insiders',
                     '% Held by Institutions',
                     'Forward Annual Dividend Rate','Forward Annual Dividend Yield',
                     'Trailing Annual Dividend Rate','Trailing Annual Dividend Yield','5 Year Average Dividend Yield',
                     'Payout Ratio','Dividend Date','Ex-Dividend Date']

t1 = time.time()

now = datetime.datetime.now()
datetag = now.strftime("%Y-%m-%d-%H-%M")
######Open the File to be written
#outputfilename =  "YF2tab-" + datetag + "-" + timetag + ".xlsx"
outputfilename =  "YF2tab-" + datetag + ".xlsx"
workbook = xlsxwriter.Workbook(outputfilename)

stocks_arr =[]
pfolio_file= open("stocks-Master.csv", "r")
for line in pfolio_file:
    indv_stock_arr = line.strip().split(',')
    stocks_arr.append(indv_stock_arr)

print(stocks_arr)

#browser = webdriver.PhantomJS()
stock_info_arr = []

for stock in stocks_arr:
    stock_info = []
    ticker = stock[0]
    stock_info.append(ticker)

    url = "https://finance.yahoo.com/quote/{0}?p={0}".format(ticker)
    url2 = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}".format(ticker)
    url3 = "https://finance.yahoo.com/quote/{0}/profile?p={0}".format(ticker)


#########Next section is to obtain on Main page, currently only Market Cap

#    try:
#        res = requests.get(url,timeout=15)
#        res.raise_for_status()
#    except requests.exceptions.HTTPError as errh:
#        print ("Line 138 Http Error and ticker:",errh, ticker)
#    except requests.exceptions.ConnectionError as errc:
#        print ("Line 140 Error Connecting and ticker:",errc, ticker)
#    except requests.exceptions.Timeout as errt:
#        print ("Line 142 Timeout Error and ticker:",errt, ticker)
#    except requests.exceptions.RequestException as err:
#        print ("Line 144 OOps: Something Else and ticker",err, ticker)

    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    for stat in key_stats_on_main:
        page_stat1 = soup.find(text=stat)
        try:
            page_row1 = page_stat1.find_parent('tr')
            #print('page_row1 is', page_row1)
            try:
                page_statnum1 = page_row1.find_all('span')[1].contents[1].get_text(strip=True)
                #print('page_statnum1 span 1 1 is ',page_statnum1)
            except:
                page_statnum1 = page_row1.find_all('td')[1].contents[0].get_text(strip=True)
                #print('page_statnum1 td is', page_statnum1)
        except:
            print('Line 162 Invalid parent for this element in URL111')
            page_statnum1 = "N/A"

        stock_info.append(page_statnum1)
        print('Line 166 stock_info is: ', stock_info)
        print ((time.time()-t1),'seconds passed!')
#        if (time.time()-t1) > 700:
#            time.sleep(2)
#########Main page section is over


#######This section is to get the latest stock price which is strangly not available in other two URLs
#    try:
#        res = requests.get('http://finance.yahoo.com/q?s=' + ticker,timeout=15)
#        res.raise_for_status()
#    except requests.exceptions.HTTPError as errh:
#        print ("Line 178 Http Error and ticker:",errh, ticker)
#    except requests.exceptions.ConnectionError as errc:
#        print ("Line 180 Error Connecting and ticker:",errc, ticker)
#    except requests.exceptions.Timeout as errt:
#        print ("Line 182 Timeout Error and ticker:",errt, ticker)
#    except requests.exceptions.RequestException as err:
#        print ("Line 184 OOps: Something Else and ticker",err, ticker)

    res = requests.get('http://finance.yahoo.com/q?s=' + ticker)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.find("span","Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)")
    #print('elems is:',elems)

##### elems.string is string. Sometimes Yahoo Finance's URL does not have any data.
##### To avoid early exit from the rest of ticker files, we add this try statement to handle the situation
    try:
#    print('ticker, cash_yr are:',ticker, cash_yr)
        current_price = elems.string
        stock_info.append(current_price)
        print(ticker,'Line 196 current_price is ', elems.string)
    except TypeError:
        print('line 198 ticker, elems does not have string', ticker)
        continue
    #print('stock_info after price info is:', stock_info)
########## Stock Price section is over


#######This section is to get the Profile page's Description Info
    res = requests.get(url3)
#    print('line 122 res and ticker is',ticker, res)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.find("p","Mt(15px) Lh(1.6)")
#    print(' line 124 elems is:',soup, elems)

##### elems.string is string. Sometimes Yahoo Finance's URL does not have any data.
##### To avoid early exit from the rest of ticker files, we add this if statement to handle the situation
    if(bool(elems) and bool(elems.string)):
#    print('ticker, cash_yr and type bool()is:',ticker, cash_yr, type(cash_yr),bool(cash_yr))
        Description = elems.string
        stock_info.append(Description)
#        print(ticker,'Line 132 Company Description is ', elems.string)
    else:
        print('line 217 ticker, elems,string is emplty', ticker)
        continue

####### Profile page's Description Info is over



#########This section is to get bulk of information from Yahoo Finance Statistics page
#    browser.get(url2)
#    innerHTML2 = browser.execute_script("return document.body.innerHTML")
#    soup2 = bs4.BeautifulSoup(innerHTML2, 'html.parser')
#    try:
#        res = requests.get(url2,timeout=15)
#        res.raise_for_status()
#    except requests.exceptions.HTTPError as errh:
#        print ("Line 211 Http Error and ticker:",errh, ticker)
#    except requests.exceptions.ConnectionError as errc:
#        print ("Line 213 Error Connecting and ticker:",errc, ticker)
#    except requests.exceptions.Timeout as errt:
#        print ("Line 215 Timeout Error and ticker:",errt, ticker)
#    except requests.exceptions.RequestException as err:
#        print ("Line 217 OOps: Something Else and ticker",err, ticker)

    try:
        res = requests.get(url2)
#        print('line 204 res is: ', res)
    except:
        print('line 206 res failed without successful connection:')

    soup2 = bs4.BeautifulSoup(res.text, 'html.parser')

    for stat in key_stats_on_stat:
        page_stat2 = soup2.find(text=stat)
        #print('stat and page_stat2 is', stat, page_stat2)
        try:
            page_row2 = page_stat2.find_parent('tr')
            #print('line 253 page_row2 is :', page_row2)
            try:

                page_statnum2 = page_row2.find_all('span')[1].contents[1]
                print(ticker,'Line 257 current span', stat, 'is', page_statnum2)

            except:
                #page_row2.find_all('span')[1].contents[1] and page_row2.find_all('td')[1].contents[1] are strings
                # in order to find the right pasring results, using print() to parse down page_row2
                # it turns out 'td' tage includes the data for attributes in key_stats_on_stat, such as Enterprise Value', 'Trailing P/E', 'Forward P/E'
                # while 'span' only includes the name. The parse down all 'td' tags using print() functions:
                # First print(page_row2.find_all('td')[0]), then print(page_row2.find_all('td')[0].contents[0]), then print(page_row2.find_all('td')[0].contents[1]),
                # If do not find the right attribute, the
                #print(page_row2.find_all('td')[1]), then print(page_row2.find_all('td')[1].contents[0]), print(page_row2.find_all('td')[1].contents[1])
                # After reviewing the printouts, it shows we do not need to use get_text(strip=True) at end of page_rows2 parsing
                #print('page_statnum2 td[1] is:', page_row2.find_all('td')[1])

                page_statnum2 = page_row2.find_all('td')[1].contents[0]
                #print(ticker,' line 212 current ', stat, 'is', page_statnum2)
                #if (page_statnum2.find_all('span'))
                #    page_statnum2=page_statnum2.find_all('span')[1]
                #else
#                print(ticker,' line 190 current ', stat, 'is', page_statnum2)
                #print('page_statnum2 td 1,0 is', page_statnum2)
                #page_statnum2 = page_row2.find_all('td')[0].contents[1].get_text(strip=True) <-- Original function
                #print('page_statnum2 td 0,1 is', page_row2.find_all('td')[0].contents[1])
                #print('page_statnum2 td 1,0 is', page_row2.find_all('td')[1].contents[0])
                #print('page_statnum2 td 1,0 get_text is', page_row2.find_all('td')[1].contents[0].get_text(strip=True))
                #print('page_statnum2 td 1,1 and get_text is', page_row2.find_all('td')[1].contents[1].get_text(strip=True))
        except:
            print('Line 283 Invalid parent for this element in URL2, likey Beta missing page_row2 and page_statnum2 are:')#, page_row2, page_statnum2)
            page_statnum2 = 'N/A'
        stock_info.append(page_statnum2)
        #print('Line 286 page_statnum2 after URL2 is: ', page_statnum2)

    stock_info_arr.append(stock_info)

print('line 232',stock_info_arr)
#########Yahoo Finance Statistics page is over


########## WRITING OUR RESULTS INTO EXCEL
#print('key_stats_on_main before extend is:',key_stats_on_main)
key_stats_on_main.append('Current Price')
key_stats_on_main.append('Company Description')
key_stats_on_main.extend(key_stats_on_stat)
#print('key_stats_on_main is: ', key_stats_on_main)

#### Now add a worksheet called Summary at the beginning

worksheet = workbook.add_worksheet('Summary')
worksheet.freeze_panes(1, 1)

row = 1
col = 0

for stat in key_stats_on_main:
    print('stat to be written to Excel is', stat)
    worksheet.write(row, col, stat)
    row +=1

row = 0
col = 1
for our_stock in stock_info_arr:
    row = 0
    for info_bit in our_stock:
        info_bit=str(info_bit)
        #print('line 138 info_bit to be written into Excel is:', info_bit)
        worksheet.write(row, col, info_bit)
        row += 1
    col += 1

#workbook.close()

print('line 327 YF Statiscs Completed')



##########Next section is to download all Yahoo Finance Financial Statements
stocks_arr =[]

pfolio_file= open("stocks-Master.csv", "r")
for line in pfolio_file:
    indv_stock_arr = line.strip().split(',')
    stocks_arr.append(indv_stock_arr)
print(stocks_arr)

#    worksheet = workbook.add_worksheet('{0}-K'.format(ticker))
worksheet = workbook.add_worksheet('Annual')
worksheet.freeze_panes(1, 1)

worksheet2 = workbook.add_worksheet('Quarter')
worksheet.freeze_panes(1, 1)

## To wirte in all annual data to one worksheet, we set col = 0 and incremental from here.
col = 0
dateCol = 0
ElementCol = 0
Qcol = 0
Qrow = 0
QdateCol = 0
QElementCol = 0

for stock in stocks_arr:
    stock_info = []
    ticker = stock[0]
    stock_info.append(ticker)

    url = "https://finance.yahoo.com/quote/{0}/financials?p={0}".format(ticker)

#    try:
#        res = requests.get(url,timeout=15)
#        res.raise_for_status()
#    except requests.exceptions.HTTPError as errh:
#        print ("Line 346 Http Error and ticker:",errh, ticker)
#    except requests.exceptions.ConnectionError as errc:
#        print ("Line 348 Error Connecting and ticker:",errc, ticker)
#    except requests.exceptions.Timeout as errt:
#        print ("Line 350 Timeout Error and ticker:",errt, ticker)
#    except requests.exceptions.RequestException as err:
#        print ("Line 352 OOps: Something Else and ticker",err, ticker)
    try:
        html = requests.get(url).text
    except:
        print('line 377 requests failed without successful connection:')
#        break

    soup = bs4.BeautifulSoup(html,'html.parser')
    #print('line 381 soup type is:', type(soup))

    soup_script = soup.find("script",text=re.compile("root.App.main")).text
    print('line 384 soup_script type is :', type(soup_script))
    json_script = json.loads(re.search("root.App.main\s+=\s+(\{.*\})",soup_script)[1])
#print('json_script type is:', type(json_script))
    fin_data = json_script['context']['dispatcher']['stores']['QuoteSummaryStore']
#print('fin_data type is:', type(fin_data))

    cash_yr = fin_data['cashflowStatementHistory']

##### cash_yr is dict. Sometimes Yahoo Finance's Financial page does not
##### have any data. Example is as of 2018-09-07, LRCX does not have any fin data
##### To avoid early exit from the rest of ticker files, we add this if statement to handle the situation
    if(bool(cash_yr)):
#    print('ticker, cash_yr and type bool()is:',ticker, cash_yr, type(cash_yr),bool(cash_yr))
        cash_yr_a = cash_yr['cashflowStatements']
        print('line 398 ticker, ticker has cash_yr', ticker)
    else:
        print('line 400 ticker, cash_yr is emplty', ticker)
        continue
#    print('ticker, cash_yr_a is:',ticker, cash_yr_a)
#    print('line 307 after the cash_yr if statment, ticker', ticker)
    dope_data = []
    dope_data1 = []
    Dope_data = []
    Dope_data1 = []
    date = []
    date2 = []
    annual_data1 = []
    annual_data2 = []
    annual_data3 = []
    annual_data4 = []
    cash_dataNumber1 = []
    cash_dataNumber2 = []
    cash_dataNumber3 = []
    cash_dataNumber4 = []

    BS_yr_dataNumber1 = []
    BS_yr_dataNumber2 = []
    BS_yr_dataNumber3 = []
    BS_yr_dataNumber4 = []

    IS_yr_dataNumber1 = []
    IS_yr_dataNumber2 = []
    IS_yr_dataNumber3 = []
    IS_yr_dataNumber4 = []

    cash_qtrs_dataNumber1 = []
    cash_qtrs_dataNumber2 = []
    cash_qtrs_dataNumber3 = []
    cash_qtrs_dataNumber4 = []

    BS_qtrs_dataNumber1 = []
    BS_qtrs_dataNumber2 = []
    BS_qtrs_dataNumber3 = []
    BS_qtrs_dataNumber4 = []

    IS_qtrs_dataNumber1 = []
    IS_qtrs_dataNumber2 = []
    IS_qtrs_dataNumber3 = []
    IS_qtrs_dataNumber4 = []


    matching_elements = ['netIncome','depreciation','changeToNetincome','changeToAccountReceivables','changeToLiabilities','changeToInventory',
                     'changeToOperatingActivities','totalCashFromOperatingActivities','capitalExpenditures','investments','otherCashflowsFromInvestingActivities',
                     'totalCashflowsFromInvestingActivities','dividendsPaid','salePurchaseOfStock','netBorrowings','otherCashflowsFromFinancingActivities',
                     'totalCashFromFinancingActivities','effectOfExchangeRate','changeInCash']

    print('Line 450, ticker, len(cash_yr_a)', ticker, len(cash_yr_a))

    if(len(cash_yr_a)>=4):
        annual_data1 = cash_yr_a[3]
        print('line 454 ticker, ticker has len(cash_yr_a)', ticker,len(cash_yr_a))
        data_keys = annual_data1.keys()
        #print(data_keys)
        for i in range(len(matching_elements)):
            if matching_elements[i] in data_keys:
                dope_data = annual_data1.get(matching_elements[i])
                Dope_data = dope_data.get('raw')
                cash_dataNumber1.append(Dope_data)
                #print(Dope_data)
            else:
                zero = 0
                cash_dataNumber1.append(zero)
            #print(cash_dataNumber1)
    else:
        print('line 468 ticker has less than 4 year financials length of cash_yr is ', ticker, len(cash_yr_a))
        continue ## Continue will skip codes from line 471 to 1076 and back to Line 356 for the next item in the big For Loop

    annual_data2 = cash_yr_a[2]
    data_keys2 = annual_data2.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in data_keys2:
            dope_data = annual_data2.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_dataNumber2.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_dataNumber2.append(zero)
    print('Line 482')

    annual_data3 = cash_yr_a[1]
    data_keys3 = annual_data3.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in data_keys3:
            dope_data = annual_data3.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_dataNumber3.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_dataNumber3.append(zero)
    print('Line 495')

    annual_data4 = cash_yr_a[0]
    data_keys4 = annual_data4.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in data_keys4:
            dope_data1 = annual_data4.get(matching_elements[i])
            Dope_data1 = dope_data1.get('raw')
            cash_dataNumber4.append(Dope_data1)
        else:
            zero = 0
            cash_dataNumber4.append(zero)
    print('line 507')


    b = len(cash_yr_a)
    cash_yr_a.reverse()
####add ticker to the first of date
    date.append(ticker)
    for i in range(b):
        cash_yr_a_b = cash_yr_a[i]
        endDate = cash_yr_a_b.get('endDate')
        dateEnd = endDate.get('fmt')
        date.append(dateEnd)

###Next section is to write the data to Excel file
# Line 0 is for the Date
    row = 0
    for D in date:
        worksheet.write(row,dateCol,D)
        print('line 525 ticker, row, dateCol content is: ', ticker, row, dateCol, D)
        dateCol +=1

    row = 1
#### First iteration we start col from 0, then incremental from here.

    for d in Elements:
        worksheet.write(row, ElementCol, d)
        print('line 533 ticker, row, col content is: ', ticker, row, ElementCol, d)
        row +=1

### Next is financial data write to Excel: starting from line 2 or row 1
    row = 1
    col = ElementCol+1
    initialCol = col
    for i in cash_dataNumber1:
        worksheet.write(row,col,i)
        print('line 542 ticker, row, col content is: ', ticker, row, col,i)
        row+=1
    row = 1
    col = col + 1
    for i in cash_dataNumber2:
        worksheet.write(row,col,i)
        print('line 548 ticker, row, col content is: ', ticker, row, col,i)
        row+=1

    row = 1
    col += 1
    for i in cash_dataNumber3:
        worksheet.write(row,col,i)
        print('line 555 ticker, row, col content is: ', ticker, row, col,i)
        row+=1

    row = 1
    col += 1
    for i in cash_dataNumber4:
        worksheet.write(row,col,i)
        print('line 562 ticker, row, col content is: ', ticker, row, col,i)
        row+=1


    BS_yr = fin_data['balanceSheetHistory']['balanceSheetStatements']

    matching_elements2 = ['cash','shortTermInvestments','netReceivables','inventory','otherCurrentAssets','totalCurrentAssets','longTermInvestments',
                          'propertyPlantEquipment','goodWill','intangibleAssets','otherAssets','deferredLongTermAssetCharges','totalAssets','accountsPayable','shortLongTermDebt',
                          'otherCurrentLiab','totalCurrentLiabilities','longTermDebt','otherLiab','deferredLongTermLiab','minorityInterest','totalLiab','commonStock','retainedEarnings','treasuryStock','capitalSurplus',
                          'otherStockholderEquity','totalStockholderEquity','netTangibleAssets']

    BS_yr_data = BS_yr[3]
    BS_yr_keys1 = BS_yr_data.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_yr_keys1:
            dope_data = BS_yr_data.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_yr_dataNumber1.append(Dope_data)
        else:
            zero = 0
            BS_yr_dataNumber1.append(zero)
    #print(BS_yr_dataNumber1)
    BS_yr_data2 = BS_yr[2]
    BS_yr_keys2 = BS_yr_data2.keys()

    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_yr_keys2:
            dope_data = BS_yr_data2.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_yr_dataNumber2.append(Dope_data)
        else:
            zero = 0
            BS_yr_dataNumber2.append(zero)
    #print(BS_yr_dataNumber2)
    BS_yr_data3 = BS_yr[1]
    BS_yr_keys3 = BS_yr_data3.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_yr_keys3:
            dope_data = BS_yr_data3.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_yr_dataNumber3.append(Dope_data)
        else:
            zero = 0
            BS_yr_dataNumber3.append(zero)
    #print(BS_yr_dataNumber3)
    BS_yr_data4 = BS_yr[0]
    BS_yr_keys4 = BS_yr_data4.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_yr_keys4:
            dope_data = BS_yr_data4.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_yr_dataNumber4.append(Dope_data)
        else:
            zero = 0
            BS_yr_dataNumber4.append(zero)
    #print(BS_yr_dataNumber4)
    CashFlowNumberofLineItem = len(cash_dataNumber4)
    #print('line 297 CashFlowNumberofLineItem is: ', CashFlowNumberofLineItem)

# Need to add 2 to get the first line of balance sheet item, 1 is for top line of Date,
# 2nd line is to add extra line between Cash Flow Statement and Balance Sheet
    FirstLineofBS_yr = CashFlowNumberofLineItem+2

    row = FirstLineofBS_yr
    col = initialCol - 1
    for i in matching_elements2:
        worksheet.write(row,ElementCol,i)
        print('line 629 ticker, row, col is: ', ticker, row, ElementCol)
        row+=1

    row = FirstLineofBS_yr
    col += 1
    for i in BS_yr_dataNumber1:
        worksheet.write(row,col,i)
        print('line 636 ticker, row, col is: ', ticker, row, col)
        row+=1

    row = FirstLineofBS_yr
    col += 1
    for i in BS_yr_dataNumber2:
        worksheet.write(row,col,i)
        row+=1

    row = FirstLineofBS_yr
    col += 1
    for i in BS_yr_dataNumber3:
        worksheet.write(row,col,i)
        row+=1

    row = FirstLineofBS_yr
    col += 1
    for i in BS_yr_dataNumber4:
        worksheet.write(row,col,i)
        row+=1




    IS_yr = fin_data['incomeStatementHistory']['incomeStatementHistory']
    #print(IS_yr[0])
    matching_elements3 = ['totalRevenue','costOfRevenue','grossProfit','researchDevelopment','sellingGeneralAdministrative','nonRecurring','otherOperatingExpenses','totalOperatingExpenses',
                          'operatingIncome','totalOtherIncomeExpenseNet','ebit','interestExpense','incomeBeforeTax','incomeTaxExpense','minorityInterest','netIncomeFromContinuingOps',
                          'discontinuedOperations','extraordinaryItems','effectOfAccountingCharges','otherItems',
                          'netIncome','netIncomeApplicableToCommonShares']
    IS_yr_data = IS_yr[3]
    #print(IS_yr_data)
    IS_yr_keys1 = IS_yr_data.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_yr_keys1:
            dope_data = IS_yr_data.get(matching_elements3[i])
            if dope_data == {} :
                Dope_data = 0
                IS_yr_dataNumber1.append(Dope_data)

            else:
                Dope_data = dope_data.get('raw')
                IS_yr_dataNumber1.append(Dope_data)
        else:
            zero = 0
            IS_yr_dataNumber1.append(zero)


    IS_yr_data2 = IS_yr[2]
    IS_yr_keys2 = IS_yr_data2.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_yr_keys2:
            dope_data = IS_yr_data2.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_yr_dataNumber2.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_yr_dataNumber2.append(Dope_data)
        else:
            zero = 0
            IS_yr_dataNumber2.append(zero)
    #print(IS_yr_dataNumber2)

    IS_yr_data3 = IS_yr[1]
    IS_yr_keys3 = IS_yr_data3.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_yr_keys3:
            dope_data = IS_yr_data3.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_yr_dataNumber3.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_yr_dataNumber3.append(Dope_data)
        else:
            zero = 0
            IS_yr_dataNumber3.append(zero)
    #print(IS_yr_dataNumber3)

    IS_yr_data4 = IS_yr[0]
    IS_yr_keys4 = IS_yr_data4.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_yr_keys4:
            dope_data = IS_yr_data4.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_yr_dataNumber4.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_yr_dataNumber4.append(Dope_data)
        else:
            zero = 0
            IS_yr_dataNumber4.append(zero)

    BSNumberofLineItem = len(BS_yr_dataNumber4)

# First line of Income Statement should be total lines of BS and CashFlow Statement, then add 3 lines
# 1st line is for Date, 2nd line is extra line between BS/CashFlow, 3rd line is extra line between CashFlow/IS
    FirstLineofIS_yr = BSNumberofLineItem+CashFlowNumberofLineItem+3

    row = FirstLineofIS_yr
    col = initialCol - 1

    for i in matching_elements3:
        worksheet.write(row,ElementCol,i)
        row+=1

    row = FirstLineofIS_yr
    col += 1
    for i in IS_yr_dataNumber1:
        worksheet.write(row,col,i)
        row+=1

    row = FirstLineofIS_yr
    col += 1
    for i in IS_yr_dataNumber2:
        worksheet.write(row,col,i)
        row+=1

    row = FirstLineofIS_yr
    col += 1
    for i in IS_yr_dataNumber3:
        worksheet.write(row,col,i)
        row+=1

    row = FirstLineofIS_yr
    col += 1
    for i in IS_yr_dataNumber4:
        worksheet.write(row,col,i)
        row+=1

    #print('the length of Elements is', len(Element))

###### Next is quarterly data
###################################
    cash_qtrs = fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']

    cash_qtrs_data1 = cash_qtrs[3]
    cash_qtrsdata_keys1 = cash_qtrs_data1.keys()
    #print(data_keys)
    for i in range(len(matching_elements)):
        if matching_elements[i] in cash_qtrsdata_keys1:
            dope_data = cash_qtrs_data1.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_qtrs_dataNumber1.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_qtrs_dataNumber1.append(zero)



    cash_qtrs_data2 = cash_qtrs[2]
    cash_qtrsdata_keys2 = cash_qtrs_data2.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in cash_qtrsdata_keys2:
            dope_data = cash_qtrs_data2.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_qtrs_dataNumber2.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_qtrs_dataNumber2.append(zero)

    cash_qtrs_data3 = cash_qtrs[1]
    cash_qtrsdata_keys3 = cash_qtrs_data3.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in cash_qtrsdata_keys3:
            dope_data = cash_qtrs_data3.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_qtrs_dataNumber3.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_qtrs_dataNumber3.append(zero)


    cash_qtrs_data4 = cash_qtrs[0]
    cash_qtrsdata_keys4 = cash_qtrs_data4.keys()
    for i in range(len(matching_elements)):
        if matching_elements[i] in cash_qtrsdata_keys4:
            dope_data = cash_qtrs_data4.get(matching_elements[i])
            Dope_data = dope_data.get('raw')
            cash_qtrs_dataNumber4.append(Dope_data)
            #print(Dope_data)
        else:
            zero = 0
            cash_qtrs_dataNumber4.append(zero)

    e = len(cash_qtrs)
    cash_qtrs.reverse()
    ####add ticker to the first of date
    date2.append(ticker)
    for i in range(e):
        cash_qtrs_a_b = cash_qtrs[i]
        endDate1 = cash_qtrs_a_b.get('endDate')
        dateEnd1 = endDate1.get('fmt')
        date2.append(dateEnd1)

#####Next section is to write quarterly data to Excel File
    Qrow = 0
    for i in date2:
        worksheet2.write(Qrow,QdateCol,i)
        QdateCol+=1

    Qrow = 1
#### First iteration we start col from 0, then incremental from here.
    for i in Elements:
        worksheet2.write(Qrow,QElementCol,i)
        Qrow+=1

### Next is financial data write to Excel: starting from line 2 or row 1
    Qrow = 1
    Qcol = QElementCol+1
    QinitialCol = Qcol

    for i in cash_qtrs_dataNumber1:
        worksheet2.write(Qrow,Qcol,i)
        Qrow+=1

    Qrow = 1
    Qcol += 1
    for i in cash_qtrs_dataNumber2:
        worksheet2.write(Qrow,Qcol,i)
        Qrow+=1

    Qrow = 1
    Qcol += 1
    for i in cash_qtrs_dataNumber3:
        worksheet2.write(Qrow,Qcol,i)
        Qrow+=1

    Qrow = 1
    Qcol += 1
    for i in cash_qtrs_dataNumber4:
        worksheet2.write(Qrow,Qcol,i)
        Qrow+=1

    BS_qtrs = fin_data['balanceSheetHistoryQuarterly']['balanceSheetStatements']

    BS_qtrs_data1 = BS_qtrs[3]
    BS_qtrs_keys1 = BS_qtrs_data1.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_qtrs_keys1:
            dope_data = BS_qtrs_data1.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_qtrs_dataNumber1.append(Dope_data)
        else:
            zero = 0
            BS_qtrs_dataNumber1.append(zero)


    BS_qtrs_data2 = BS_qtrs[2]
    BS_qtrs_keys2 = BS_qtrs_data2.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_qtrs_keys2:
            dope_data = BS_qtrs_data2.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_qtrs_dataNumber2.append(Dope_data)
        else:
            zero = 0
            BS_qtrs_dataNumber2.append(zero)

    BS_qtrs_data3 = BS_qtrs[1]
    BS_qtrs_keys3 = BS_qtrs_data3.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_qtrs_keys3:
            dope_data = BS_qtrs_data3.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_qtrs_dataNumber3.append(Dope_data)
        else:
            zero = 0
            BS_qtrs_dataNumber3.append(zero)


    BS_qtrs_data4 = BS_qtrs[0]
    BS_qtrs_keys4 = BS_qtrs_data4.keys()
    for i in range(len(matching_elements2)):
        if matching_elements2[i] in BS_qtrs_keys4:
            dope_data = BS_qtrs_data4.get(matching_elements2[i])
            Dope_data = dope_data.get('raw')
            BS_qtrs_dataNumber4.append(Dope_data)
        else:
            zero = 0
            BS_qtrs_dataNumber4.append(zero)

    CashFlowQtrsNumberofLineItem = len(cash_qtrs_dataNumber4)

# Need to add 2 to get the first line of balance sheet item, 1 is for top line of Date,
# 2nd line is to add extra line between Cash Flow Statement and Balance Sheet
    FirstLineofBS_qtrs = CashFlowQtrsNumberofLineItem+2
    print('First line of BS starts at: ', FirstLineofBS_qtrs)

    Qrow = FirstLineofBS_qtrs
    Qcol = QinitialCol - 1
    for i in matching_elements2:
        worksheet2.write(Qrow,QElementCol,i)
        Qrow+=1

    Qrow = FirstLineofBS_qtrs
    Qcol += 1
    for i in BS_qtrs_dataNumber1:
        worksheet2.write(Qrow,Qcol,i)
        print('Line 940 ticker quarterly BS Qrow, Qcol, and i is: ', ticker, Qrow, Qcol, i)
        Qrow+=1

    Qrow = FirstLineofBS_qtrs
    Qcol += 1
    for i in BS_qtrs_dataNumber2:
        worksheet2.write(Qrow,Qcol,i)
        print('Line 947 quarterly BS is: ', i)
        Qrow+=1

    Qrow = FirstLineofBS_qtrs
    Qcol += 1
    for i in BS_qtrs_dataNumber3:
        worksheet2.write(Qrow,Qcol,i)
        print('Line 954 quarterly BS is: ', i)
        Qrow+=1

    Qrow = FirstLineofBS_qtrs
    Qcol += 1
    for i in BS_qtrs_dataNumber4:
        worksheet2.write(Qrow,Qcol,i)
        print('Line 961 ticker, quarterly BS is: ', ticker, i)
        Qrow+=1




    IS_qtrs = fin_data['incomeStatementHistoryQuarterly']['incomeStatementHistory']

    IS_qtrs_data1 = IS_qtrs[3]
    IS_qtrs_keys1 = IS_qtrs_data1.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_qtrs_keys1:
            dope_data = IS_qtrs_data1.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_qtrs_dataNumber1.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_qtrs_dataNumber1.append(Dope_data)
        else:
            zero = 0
            IS_qtrs_dataNumber1.append(zero)


    IS_qtrs_data2 = IS_qtrs[2]
    IS_qtrs_keys2 = IS_qtrs_data2.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_qtrs_keys2:
            dope_data = IS_qtrs_data2.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_qtrs_dataNumber2.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_qtrs_dataNumber2.append(Dope_data)
        else:
            zero = 0
            IS_qtrs_dataNumber2.append(zero)


    IS_qtrs_data3 = IS_qtrs[1]
    IS_qtrs_keys3 = IS_qtrs_data3.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_qtrs_keys3:
            dope_data = IS_qtrs_data3.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_qtrs_dataNumber3.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_qtrs_dataNumber3.append(Dope_data)
        else:
            zero = 0
            IS_qtrs_dataNumber3.append(zero)

    print('line 1016, ticker', ticker)
    IS_qtrs_data4 = IS_qtrs[0]
    IS_qtrs_keys4 = IS_qtrs_data4.keys()
    for i in range(len(matching_elements3)):
        if matching_elements3[i] in IS_qtrs_keys4:
            dope_data = IS_qtrs_data4.get(matching_elements3[i])
            if dope_data == {}:
                Dope_data = 0
                IS_qtrs_dataNumber4.append(Dope_data)
            else:
                Dope_data = dope_data.get('raw')
                IS_qtrs_dataNumber4.append(Dope_data)
        else:
            zero = 0
            IS_qtrs_dataNumber4.append(zero)

    BSQtrsNumberofLineItem = len(BS_qtrs_dataNumber4)

# First line of Income Statement should be total lines of BS and CashFlow Statement, then add 3 lines
# 1st line is for Date, 2nd line is extra line between BS/CashFlow, 3rd line is extra line between CashFlow/IS
    FirstLineofIS_qtrs = BSQtrsNumberofLineItem+CashFlowQtrsNumberofLineItem+3
    print('ticker',ticker, 'first line of Income Statement starts at: ', FirstLineofIS_qtrs)

    Qrow = FirstLineofIS_qtrs
    Qcol = QinitialCol - 1
    for i in matching_elements3:
        worksheet2.write(Qrow,Qcol,i)
        print('line 1043 ticker contne is writen to worksheet2,Qrow,Qcol,i ',ticker, Qrow,Qcol,i)
        Qrow+=1

    Qrow = FirstLineofIS_qtrs
    Qcol +=1
    for i in IS_qtrs_dataNumber1:
        worksheet2.write(Qrow,Qcol,i)
        print('line 1050 ticker contne is writen to worksheet2,Qrow,Qcol,i ',ticker, Qrow,Qcol,i)
        Qrow+=1

    Qrow = FirstLineofIS_qtrs
    Qcol += 1
    for i in IS_qtrs_dataNumber2:
        worksheet2.write(Qrow,Qcol,i)
        print('line 1057 ticker contne is writen to worksheet2,Qrow,Qcol,i ',ticker, Qrow,Qcol,i)
        Qrow+=1

    Qrow = FirstLineofIS_qtrs
    Qcol += 1
    for i in IS_qtrs_dataNumber3:
        worksheet2.write(Qrow,Qcol,i)
        Qrow+=1

    Qrow = FirstLineofIS_qtrs
    Qcol += 1
    for i in IS_qtrs_dataNumber4:
        worksheet2.write(Qrow,Qcol,i)
        print('line 1070 ticker contne is writen to worksheet2,Qrow,Qcol,i ',ticker, Qrow,Qcol,i)
        Qrow+=1
    print('line 1072, ticker', ticker)
### After the elements write up, ElementCol shift 4 positions
    ElementCol +=5
    QElementCol +=5
    print('line 1076, ticker', ticker)

print('line 1078, ticker', ticker)
workbook.close()
print('Workbook finsihed writing and closed now at line 1080, ticker', ticker)

print('Line 1082 YF Financial Statements Completed')

t2 = time.time()
print ('Total Time taken:')
print (t2-t1)










#print('cash_yr_a type is:', type(cash_yr_a))
#print(cash_yr)
#cash_stats_yr = cash_yr.keys()
#print(cash_stats_yr)
#print(cash_yr_a)
#print(cash_yr_a_b)
#cash_qtrs = fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']

#BS_yr = fin_data['balanceSheetHistory']['balanceSheetStatements']
#BS_qtrs = fin_data['balanceSheetHistoryQuarterly']['balanceSheetStatements']

#IS_yr = fin_data['incomeStatementHistory']['incomeStatementHistory']
#IS_qtrs = fin_data['incomeStatementHistoryQuarterly']['incomeStatementHistory']
