#!/usr/bin/env python
# coding: utf-8

# # Scraping 10-Ks and 10-Qs for Alpha (Data Cleaning)

# ## THESIS:
# Major text changes in 10-K and 10-Q filings over time indicate significant decreases in future returns. We find alpha in shorting the companies with the largest text changes in their filings and buying the companies with the smallest text changes in their filings.

# ### Introduction
# Publicly listed companies in the U.S. are required by law to file "10-K" and "10-Q" reports with the [Securities and Exchange Commission](https://www.sec.gov/) (SEC). These reports provide both qualitative and quantitative descriptions of the company's performance, from revenue numbers to qualitative risk factors.
#
# When companies file 10-Ks and 10-Qs, they are required to disclose certain pieces of information. For example, companies are required to report information about ["significant pending lawsuits or other legal proceedings"](https://www.sec.gov/fast-answers/answersreada10khtm.html). As such, 10-Ks and 10-Qs often hold valuable insights into a company's performance.
#
# These insights, however, can be difficult to access. The average 10-K was [42,000 words long](https://www.wsj.com/articles/the-109-894-word-annual-report-1433203762) in 2013; put in perspective, that's roughly one-fifth of the length of Moby-Dick. Beyond the sheer length, dense language and lots of boilerplate can further obfuscate true meaning for many investors.
#
# The good news? We might not need to read companies' 10-Ks and 10-Qs from cover-to-cover in order derive value from the information they contain. Specifically, Lauren Cohen, Christopher Malloy and Quoc Nguyen argue in their [recent paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1658471) that we can simply analyze textual changes in 10-Ks and 10-Qs to predict companies' future stock returns.
#
# In this investigation, we attempt to replicate their results on Quantopian.
#
# (For an overview of this paper from Lauren Cohen himself, see [the Lazy Prices interview](https://www.youtube.com/watch?v=g96gROyc3wE) from QuantCon 2018.)

# ### Hypothesis
# Companies make major textual changes to their 10-Ks and 10-Qs when major things happen to their business. Thus, we expect that textual changes to 10-Ks and 10-Qs are a signal of future stock price movement.
#
# Since the vast majority (86%) of textual changes have negative sentiment, we generally expect that major textual changes signal a decrease in stock price (Cohen et al. 2018).
#
# Thus, we expect to find alpha by shorting companies with large textual changes in their 10-Ks and 10-Qs.

# ### Methodology
# 1. Scrape every publicly traded company's 10-Ks and 10-Qs from the [SEC EDGAR database](https://www.sec.gov/edgar/searchedgar/companysearch.html). Remove extraneous content from the 10-Ks and 10-Qs (numerical tables, HTML tags, XBRL tags, etc).
# 2. For each company, compute [cosine similarity](http://scikit-learn.org/stable/modules/metrics.html#cosine-similarity) and [Jaccard similarity](http://scikit-learn.org/stable/modules/model_evaluation.html#jaccard-similarity-score) scores over the sequence of its 10-Ks and 10-Qs. Each 10-K is compared to the previous year's 10-K; each 10-Q is compared to the 10-Q from the same quarter of the previous year.
# 3. Compile these scores into one dataset.
# 4. Upload the data to Quantopian using [Self-Serve Data](https://www.quantopian.com/posts/upload-your-custom-datasets-and-signals-with-self-serve-data), then use [Alphalens](http://quantopian.github.io/alphalens/) to analyze the performance of 10-K and 10-Q text changes as an alpha factor.
#
# This notebook covers steps 1-3. For step 4, see the [Alphalens study](https://www.quantopian.com/posts/analyzing-alpha-in-10-ks-and-10-qs) notebook.

# ## 0. Running This Notebook

# This notebook is intended to be run locally (on your own computer), *not* within the Quantopian Research environment. We run it locally in order to generate the .csv file for upload into the Self-Serve Data feature.
#
# In order to run this notebook, you will need to have Python 3 and the following packages installed:
#
# - **jupyter notebook**
# - **pandas** (version 0.23.0)
# - **numpy**
# - **requests**
# - **scikit-learn**
# - **BeautifulSoup**
# - **lxml**
# - **tqdm**
#
# All of these packages can be installed using conda or pip. For detailed installation instructions, see the installation documentation for each package ([jupyter](http://jupyter.org/install), [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html), [numpy](https://scipy.org/install.html), [Requests](http://docs.python-requests.org/en/master/user/install/#install), [scikit-learn](http://scikit-learn.org/stable/install.html), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup), [lxml](https://lxml.de/installation.html), [tqdm](https://pypi.org/project/tqdm/#installation)).
#
# To run this notebook:
#
# 1. Clone it into your own Quantopian account and open it in your research environment.
# 2. Download it as a .ipynb file (Notebook > Download as > Notebook (.ipynb))
# 3. Move the .ipynb notebook file to the desired directory on your local machine.
# 4. Open a command line window.
# 5. Use `cd` in the command line to navigate to the directory containing the notebook file.
# 6. Run `jupyter notebook` in the command line to start a jupyter notebook session.
# 7. A window should open in your default web browser displaying the contents of your current directory. Click the name of the .ipynb notebook file to open it.
# 8. Run the cells just as you would in the Quantopian Research environment.

# In[3]:


# Importing built-in libraries (no need to install these)
import re
import os
from time import gmtime, strftime
from datetime import datetime, timedelta
import unicodedata

# Importing libraries you need to install
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import bs4 as bs
from lxml import html
from tqdm import tqdm
import csv

# ## 1. Data Scraping

# We need to know what we want to scrape, so we'll begin by compiling a complete* list of U.S. stock tickers.
#
# *for our purposes, "complete" = everything traded on NASDAQ, NYSE, or AMEX.

# In[2]:


# Get lists of tickers from NASDAQ, NYSE, AMEX
#nasdaq_tickers = pd.read_csv('https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download')
#nyse_tickers = pd.read_csv('https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download')
#amex_tickers = pd.read_csv('https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download')

# Drop irrelevant cols
#nasdaq_tickers.drop(labels='Unnamed: 8', axis='columns', inplace=True)
#nyse_tickers.drop(labels='Unnamed: 8', axis='columns', inplace=True)
#amex_tickers.drop(labels='Unnamed: 8', axis='columns', inplace=True)

# Create full list of tickers/names across all 3 exchanges
#tickers = list(set(list(nasdaq_tickers['Symbol']) + list(nyse_tickers['Symbol']) + list(amex_tickers['Symbol'])))

stocks_arr =[]
pfolio_file= open("stocks-master.csv", "r", encoding='utf-8-sig')
for line in pfolio_file:
    indv_stock_arr = line.strip().split(',')
    indv_stock_arr = line.strip('[')
    indv_stock_arr = line.strip('\n')
    indv_stock_arr = line.strip()
    print('indv_stock_arr is', indv_stock_arr)
    stocks_arr.append(indv_stock_arr)

tickers =tuple(stocks_arr)
print('ticker and stock_arr type is: ', type(tickers),tickers)
#tickers =('AMAT','LRCX','CTL','HOG','PII','THO','AOBC')
# Unfortunately, the SEC indexes company filings by its own internal identifier, the "Central Index Key" (CIK). We'll need to translate tickers into CIKs in order to search for company filings on EDGAR.
#
# (The code below is an edited version of [this gist](https://gist.github.com/dougvk/8499335).)

# In[3]:



def MapTickerToCik(tickers):
    url = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    cik_re = re.compile(r'.*CIK=(\d{10}).*')

    cik_dict = {}
    for ticker in tqdm(tickers): # Use tqdm lib for progress bar
        results = cik_re.findall(requests.get(url.format(ticker)).text)
        if len(results):
            cik_dict[str(ticker).lower()] = str(results[0])

    return cik_dict


# In[11]:


cik_dict = MapTickerToCik(tickers)


# In[24]:


# Clean up the ticker-CIK mapping as a DataFrame
ticker_cik_df = pd.DataFrame.from_dict(data=cik_dict, orient='index')
ticker_cik_df.reset_index(inplace=True)
ticker_cik_df.columns = ['ticker', 'cik']
ticker_cik_df['cik'] = [int(cik) for cik in ticker_cik_df['cik']]


# Our ultimate goal is to link each ticker to a unique CIK.
#
# However, some CIKs might be linked to multiple tickers. For example, different [share classes](https://www.investopedia.com/terms/s/share_class.asp) within the same company would all be linked to the same CIK. Let's get rid of these duplicate mappings.

# In[6]:


# Check for duplicated tickers/CIKs
print("Number of ticker-cik pairings:", len(ticker_cik_df))
print("Number of unique tickers:", len(set(ticker_cik_df['ticker'])))
print("Number of unique CIKs:", len(set(ticker_cik_df['cik'])))


# It looks like about 200 (4.5%) CIKs are linked to multiple tickers. To eliminate the duplicate mappings, we'll simply keep the ticker that comes first in the alphabet. In most cases, this means we'll keep the class A shares of the stock.
#
# It's certainly possible to eliminate duplicates using other methods; for the sake of simplicity, we'll stick with alphabetizing for now. As long as we apply it uniformly across all stocks, it shouldn't introduce any bias.

# In[9]:


# Keep first ticker alphabetically for duplicated CIKs
ticker_cik_df = ticker_cik_df.sort_values(by='ticker')
ticker_cik_df.drop_duplicates(subset='cik', keep='first', inplace=True)


# In[10]:


# Check that we've eliminated duplicate tickers/CIKs
print("Number of ticker-cik pairings:", len(ticker_cik_df))
print("Number of unique tickers:", len(set(ticker_cik_df['ticker'])))
print("Number of unique CIKs:", len(set(ticker_cik_df['cik'])))


# At this point, we have a list of the CIKs for which we want to obtain 10-Ks and 10-Qs. We can now begin scraping from EDGAR.
#
# As with many web scraping projects, we'll need to keep some technical considerations in mind:
#
# - We're scraping a lot of data, so it's unlikely that we'll be able to do it all in one session without something breaking (most likely scenario: the WiFI disconnects briefly or your laptop goes to sleep). As such, we should make sure that our scraper can easily pick up where it left off without having to re-scrape anything.
# - We also probably want to log warnings/errors and save that log, just in case we need to reference it later.
# - The SEC limits users to [10 requests per second](https://www.sec.gov/developer), so we need to make sure we're not making requests too quickly.

# In[3]:


def WriteLogFile(log_file_name, text):

    '''
    Helper function.
    Writes a log file with all notes and
    error messages from a scraping "session".

    Parameters
    ----------
    log_file_name : str
        Name of the log file (should be a .txt file).
    text : str
        Text to write to the log file.

    Returns
    -------
    None.

    '''

    with open(log_file_name, "a") as log_file:
        log_file.write(text)

    return


# The function below scrapes all 10-Ks and 10-K405s one particular CIK. Our web scraper primarily depends on the [`requests`](http://docs.python-requests.org/en/master/) and [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries.
#
# Note that the scraper creates a different directory for each CIK, and puts all the filings for that CIK within that directory. After scraping, your file structure should look like this:
#
#
# ```
# - 10Ks
#     - CIK1
#         - 10K #1
#         - 10K #2
#         ...
#     - CIK2
#         - 10K #1
#         - 10K #2
#         ...
#     - CIK3
#         - 10K #1
#         - 10K #2
#         ...
#     ...
# - 10Qs
#     - CIK1
#         - 10Q #1
#         - 10Q #2
#         ...
#     - CIK2
#         - 10Q #1
#         - 10Q #2
#         ...
#     - CIK3
#         - 10Q #1
#         - 10Q #2
#         ...
#     ...
# ```
#
# The scraper will create the directory for each CIK. However, we need to create different directories to hold our 10-K and 10-Q files. The exact pathname depends on your local setup, so you'll need to fill in the correct `pathname_10k` and `pathname_10q` for your machine.

# In[ ]:


#pathname_10k = '< YOUR 10-K PATHNAME HERE>'
#pathname_10q = '< YOUR 10-Q PATHNAME HERE>'
pathname_10k = '/Users/aaronzang/desktop/SEC_grabing/10-K'
pathname_10q = '/Users/aaronzang/desktop/SEC_grabing/10-Q'


# In[ ]:


def Scrape10K(browse_url_base, filing_url_base, doc_url_base, cik, log_file_name):

    '''
    Scrapes all 10-Ks and 10-K405s for a particular
    CIK from EDGAR.

    Parameters
    ----------
    browse_url_base : str
        Base URL for browsing EDGAR.
    filing_url_base : str
        Base URL for filings listings on EDGAR.
    doc_url_base : str
        Base URL for one filing's document tables
        page on EDGAR.
    cik : str
        Central Index Key.
    log_file_name : str
        Name of the log file (should be a .txt file).

    Returns
    -------
    None.

    '''

    # Check if we've already scraped this CIK
    try:
#        Cast cik into string
        cik = str(cik)
        os.mkdir(cik)
    except OSError:
        print("Already scraped CIK", cik)
        return

    # If we haven't, go into the directory for that CIK
    os.chdir(cik)

    print('Scraping CIK', cik)

    # Request list of 10-K filings
    res = requests.get(browse_url_base % cik)

    # If the request failed, log the failure and exit
    if res.status_code != 200:
        os.chdir('..')
        os.rmdir(cik) # remove empty dir
        text = "Request failed with error code " + str(res.status_code) +                "\nFailed URL: " + (browse_url_base % cik) + '\n'
        WriteLogFile(log_file_name, text)
        return

    # If the request doesn't fail, continue...

    # Parse the response HTML using BeautifulSoup
    soup = bs.BeautifulSoup(res.text, "lxml")

    # Extract all tables from the response
    html_tables = soup.find_all('table')

    # Check that the table we're looking for exists
    # If it doesn't, exit
    if len(html_tables)<3:
        os.chdir('..')
        return

    # Parse the Filings table
    filings_table = pd.read_html(str(html_tables[2]), header=0)[0]
    filings_table['Filings'] = [str(x) for x in filings_table['Filings']]

    # Get only 10-K and 10-K405 document filings
    filings_table = filings_table[(filings_table['Filings'] == '10-K') | (filings_table['Filings'] == '10-K405')]

    # If filings table doesn't have any
    # 10-Ks or 10-K405s, exit
    if len(filings_table)==0:
        os.chdir('..')
        return

    # Get accession number for each 10-K and 10-K405 filing
    filings_table['Acc_No'] = [x.replace('\xa0',' ')
                               .split('Acc-no: ')[1]
                               .split(' ')[0] for x in filings_table['Description']]

    # Iterate through each filing and
    # scrape the corresponding document...
    for index, row in filings_table.iterrows():

        # Get the accession number for the filing
        acc_no = str(row['Acc_No'])

        # Navigate to the page for the filing
        docs_page = requests.get(filing_url_base % (cik, acc_no))

        # If request fails, log the failure
        # and skip to the next filing
        if docs_page.status_code != 200:
            os.chdir('..')
            text = "Request failed with error code " + str(docs_page.status_code) +                    "\nFailed URL: " + (filing_url_base % (cik, acc_no)) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If request succeeds, keep going...

        # Parse the table of documents for the filing
        docs_page_soup = bs.BeautifulSoup(docs_page.text, 'lxml')
        docs_html_tables = docs_page_soup.find_all('table')
        if len(docs_html_tables)==0:
            continue
        if(len(docs_html_tables) > 1):
            docs_table = pd.read_html(str(docs_html_tables[1]), header=0)[0]
            docs_table['Type'] = [str(x) for x in docs_table['Type']]
            docs_table = docs_table[(docs_table['Type'] == 'XML') | (docs_table['Type'] == 'EX-101.INS')]
        else:
            docs_table = pd.read_html(str(docs_html_tables[0]), header=0)[0]
            docs_table['Type'] = [str(x) for x in docs_table['Type']]
            docs_table = docs_table[(docs_table['Type'] == '10-K') | (docs_table['Type'] == '10-K405')]

        # Get the 10-K and 10-K405 entries for the filing


        # If there aren't any 10-K or 10-K405 entries,
        # skip to the next filing
        if len(docs_table)==0:
            continue
        # If there are 10-K or 10-K405 entries,
        # grab the first document
        elif len(docs_table)>0:
            docs_table = docs_table.iloc[0]

        docname = docs_table['Document']

        # If that first entry is unavailable,
        # log the failure and exit
        if str(docname) == 'nan':
            os.chdir('..')
            text = 'File with CIK: %s and Acc_No: %s is unavailable' % (cik, acc_no) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If it is available, continue...

        # Request the file
        file = requests.get(doc_url_base % (cik, acc_no.replace('-', ''), docname))

        # If the request fails, log the failure and exit
        if file.status_code != 200:
            os.chdir('..')
            text = "Request failed with error code " + str(file.status_code) +                    "\nFailed URL: " + (doc_url_base % (cik, acc_no.replace('-', ''), docname)) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If it succeeds, keep going...

        # Save the file in appropriate format
        if '.xml' in docname:
            # Save text as TXT
            date = str(row['Filing Date'])
            print(date, "\n")
            filename = cik + '_' + date + '.xml'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()

        elif '.txt' in docname:
            # Save text as HTML
            date = str(row['Filing Date'])
            print(date, "\n")
            filename = cik + '_' + date + '.txt'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()
        else:
            date = str(row['Filing Date'])
            print(date, "\n")
            filename = cik + '_' + date + '.html'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()


    # Move back to the main 10-K directory
    os.chdir('..')
    return


# In[4]:


def Scrape10Q(browse_url_base, filing_url_base, doc_url_base, cik, log_file_name):

    '''
    Scrapes all 10-Qs for a particular CIK from EDGAR.

    Parameters
    ----------
    browse_url_base : str
        Base URL for browsing EDGAR.
    filing_url_base : str
        Base URL for filings listings on EDGAR.
    doc_url_base : str
        Base URL for one filing's document tables
        page on EDGAR.
    cik : str
        Central Index Key.
    log_file_name : str
        Name of the log file (should be a .txt file).

    Returns
    -------
    None.

    '''

    # Check if we've already scraped this CIK
    try:
        cik=str(cik)
        os.mkdir(cik)
    except OSError:
        print("Already scraped CIK", cik)
        return

    # If we haven't, go into the directory for that CIK
    os.chdir(cik)

    print('Scraping CIK', cik)

    # Request list of 10-Q filings
    res = requests.get(browse_url_base % cik)

    # If the request failed, log the failure and exit
    if res.status_code != 200:
        os.chdir('..')
        os.rmdir(cik) # remove empty dir
        text = "Request failed with error code " + str(res.status_code) +                "\nFailed URL: " + (browse_url_base % cik) + '\n'
        WriteLogFile(log_file_name, text)
        return

    # If the request doesn't fail, continue...

    # Parse the response HTML using BeautifulSoup
    soup = bs.BeautifulSoup(res.text, "lxml")

    # Extract all tables from the response
    html_tables = soup.find_all('table')

    # Check that the table we're looking for exists
    # If it doesn't, exit
    if len(html_tables)<3:
        print("table too short")
        os.chdir('..')
        return

    # Parse the Filings table
    filings_table = pd.read_html(str(html_tables[2]), header=0)[0]
    filings_table['Filings'] = [str(x) for x in filings_table['Filings']]

    # Get only 10-Q document filings
    filings_table = filings_table[filings_table['Filings'] == '10-Q']

    # If filings table doesn't have any
    # 10-Ks or 10-K405s, exit
    if len(filings_table)==0:
        os.chdir('..')
        return

    # Get accession number for each 10-K and 10-K405 filing
    filings_table['Acc_No'] = [x.replace('\xa0',' ')
                               .split('Acc-no: ')[1]
                               .split(' ')[0] for x in filings_table['Description']]

    # Iterate through each filing and
    # scrape the corresponding document...
    for index, row in filings_table.iterrows():

        # Get the accession number for the filing
        acc_no = str(row['Acc_No'])

        # Navigate to the page for the filing
        docs_page = requests.get(filing_url_base % (cik, acc_no))

        # If request fails, log the failure
        # and skip to the next filing
        if docs_page.status_code != 200:
            os.chdir('..')
            text = "Request failed with error code " + str(docs_page.status_code) +                    "\nFailed URL: " + (filing_url_base % (cik, acc_no)) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If request succeeds, keep going...

        # Parse the table of documents for the filing
        docs_page_soup = bs.BeautifulSoup(docs_page.text, 'lxml')
        docs_html_tables = docs_page_soup.find_all('table')
        if len(docs_html_tables)==0:
            continue
        if(len(docs_html_tables) > 1):
            docs_table = pd.read_html(str(docs_html_tables[1]), header=0)[0]
            docs_table['Type'] = [str(x) for x in docs_table['Type']]
            docs_table = docs_table[(docs_table['Type'] == 'XML') | (docs_table['Type'] == 'EX-101.INS')]
        else:
            docs_table = pd.read_html(str(docs_html_tables[0]), header=0)[0]
            docs_table['Type'] = [str(x) for x in docs_table['Type']]
            docs_table = docs_table[(docs_table['Type'] == '10-K') | (docs_table['Type'] == '10-K405')]
        #docs_table = pd.read_html(str(docs_html_tables[0]), header=0)[0]
        #docs_table['Type'] = [str(x) for x in docs_table['Type']]

        # Get the 10-K and 10-K405 entries for the filing
        #docs_table = docs_table[docs_table['Type'] == '10-Q']

        # If there aren't any 10-K or 10-K405 entries,
        # skip to the next filing
        if len(docs_table)==0:
            continue
        # If there are 10-K or 10-K405 entries,
        # grab the first document
        elif len(docs_table)>0:
            docs_table = docs_table.iloc[0]

        docname = docs_table['Document']

        # If that first entry is unavailable,
        # log the failure and exit
        if str(docname) == 'nan':
            os.chdir('..')
            text = 'File with CIK: %s and Acc_No: %s is unavailable' % (cik, acc_no) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If it is available, continue...

        # Request the file
        file = requests.get(doc_url_base % (cik, acc_no.replace('-', ''), docname))

        # If the request fails, log the failure and exit
        if file.status_code != 200:
            os.chdir('..')
            text = "Request failed with error code " + str(file.status_code) +                    "\nFailed URL: " + (doc_url_base % (cik, acc_no.replace('-', ''), docname)) + '\n'
            WriteLogFile(log_file_name, text)
            os.chdir(cik)
            continue

        # If it succeeds, keep going...

        # Save the file in appropriate format
        if '.xml' in docname:
            date = str(row['Filing Date'])
            filename = cik + '_' + date + '.xml'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()
        elif '.txt' in docname:
            # Save text as TXT
            date = str(row['Filing Date'])
            filename = cik + '_' + date + '.txt'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()
        else:
            # Save text as HTML
            date = str(row['Filing Date'])
            filename = cik + '_' + date + '.html'
            html_file = open(filename, 'a')
            html_file.write(file.text)
            html_file.close()

    # Move back to the main 10-Q directory
    os.chdir('..')

    return


# Now that we've defined our scraper functions, let's scrape.
#
# (A note from the future: we're scraping a lot of data, which takes *time* and *space*. For reference, these functions ultimately scraped 170 GB of 10-Qs and 125 GB of 10-Ks; the scraping took roughly 20 hours total.)

# In[ ]:


# Run the function to scrape 10-Ks

# Define parameters
browse_url_base_10k = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-K'
filing_url_base_10k = 'http://www.sec.gov/Archives/edgar/data/%s/%s-index.html'
doc_url_base_10k = 'http://www.sec.gov/Archives/edgar/data/%s/%s/%s'

# Set correct directory
os.chdir(pathname_10k)

# Initialize log file
# (log file name = the time we initiate scraping session)
time = strftime("%Y-%m-%d %Hh%Mm%Ss", gmtime())
log_file_name = 'log '+time+'.txt'
with open(log_file_name, 'a') as log_file:
    log_file.close()

# Iterate over CIKs and scrape 10-Ks
for cik in tqdm(ticker_cik_df['cik']):
    Scrape10K(browse_url_base=browse_url_base_10k,
          filing_url_base=filing_url_base_10k,
          doc_url_base=doc_url_base_10k,
          cik=cik,
          log_file_name=log_file_name)


# In[ ]:


# Run the function to scrape 10-Qs

# Define parameters
browse_url_base_10q = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-Q&count=1000'
filing_url_base_10q = 'http://www.sec.gov/Archives/edgar/data/%s/%s-index.html'
doc_url_base_10q = 'http://www.sec.gov/Archives/edgar/data/%s/%s/%s'

# Set correct directory (fill this out yourself!)
os.chdir(pathname_10q)

# Initialize log file
# (log file name = the time we initiate scraping session)
time = strftime("%Y-%m-%d %Hh%Mm%Ss", gmtime())
log_file_name = 'log '+time+'.txt'
log_file = open(log_file_name, 'a')
log_file.close()

# Iterate over CIKs and scrape 10-Qs
for cik in tqdm(ticker_cik_df['cik']):
    Scrape10Q(browse_url_base=browse_url_base_10q,
          filing_url_base=filing_url_base_10q,
          doc_url_base=doc_url_base_10q,
          cik=cik,
          log_file_name=log_file_name)
