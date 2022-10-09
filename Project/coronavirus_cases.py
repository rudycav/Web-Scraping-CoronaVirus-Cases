# -*- coding: utf-8 -*-
"""CoronaVirus_Cases.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/rudycav/Web-Scraping-CoronaVirus-Cases/blob/master/Project/%20CoronaVirus_Cases.ipynb
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import DataFrame
import pandas as pd
from datetime import datetime
import numpy as np
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def webscrape(url = 'https://www.worldometers.info/coronavirus/'):
  header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
  link = requests.get(url, header)
  bs = BeautifulSoup(link.content,'lxml')
  title_numbers = bs.find_all(['h1','span'])
  numbers = bs.find_all(class_='maincounter-number')
  data_table = bs.find_all('table', class_='main_table_countries')
   
  data = []

  for table in data_table:
      headers = []
      rows = table.find_all('tr')
      for header in table.find('tr').find_all('th'):
          headers.append(header.text)
      for row in table.find_all('tr')[1:]:
          values = []
          for column in row.find_all(['th', 'td']):
              values.append(column.text)
          if values:
              dt = {headers[i]: values[i] for i in range(len(values))}
              data.append(dt)
              
  df = pd.DataFrame(data).rename(columns={"1stcase": "FirstCase", "Serious,Critical": "Critical"})
  return df

df = webscrape()

def punctuation_removal(df):
    try:
        #removes N/A, commas, and + symbol, converts empty cells into 0s from the dataframe
        df = df.str.replace('N/A','').str.replace(',','').replace(r'^\s*$', np.nan, regex=True).replace(np.nan, 0).astype(float).astype(int)
    except:
        pass
    return df

df = df.apply(punctuation_removal)

#remove newline in Country column
df['Country,Other'] = df['Country,Other'].replace(r'\n',' ', regex=True)