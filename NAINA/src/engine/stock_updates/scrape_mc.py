# Script for Tracking
import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

#symbols added
symbols = {
    "GPIL" : "https://www.moneycontrol.com/india/stockpricequote/steel-sponge-iron/godawaripowerispat/GPI7",
    'Poddar Housing' : 'http://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/poddarhousingdevelopment/W13',
    'Sterilite Tech' :'http://www.moneycontrol.com/india/stockpricequote/cables-telephone/sterlitetechnologies/ST20',
    'PFC' : 'http://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/powerfinancecorporation/PFC02',
    'HT Media ' : 'http://www.moneycontrol.com/india/stockpricequote/media-entertainment/htmedia/HT' ,
    'KVB' : 'http://www.moneycontrol.com/india/stockpricequote/banks-private-sector/karurvysyabank/KVB',
    'Hexaware Tech' : 'http://www.moneycontrol.com/india/stockpricequote/computers-software/hexawaretechnologies/HT02'
}

#pull data for symbols
def pull_data(x):
    data={}
    data[x] = { 'BSE' : { 'price' : 0 , 'change_inrs' : 0 , 'change_inpc' : 0 , 'volume' : 0},
                'NSE' : { 'price' : 0 , 'change_inrs' : 0 , 'change_inpc' : 0 , 'volume' : 0},
              }
    add=symbols[x]
    response = requests.get(add)
    html = response.content
    soup = BeautifulSoup(html)
    price = [(strong.text) for strong in soup.findAll("span",attrs={ "class" : "span_price_wrap"})]
    change = [strong.text for strong in soup.findAll("span",attrs={ "class" : "span_price_change_prcnt"})]
    volume = [int((strong.text).replace(",","")) for strong in soup.findAll("span",attrs={ "class" : "volume_data"})]
    #data manipulation for storing
    data[x]['BSE']['price'] = price[0]
    data[x]['BSE']['volume'] = volume[0]
    change_st = []
    for h in change:
        t = h.split(" ")
        t[1]=t[1][1:-2]
        change_st.append(t)
    data[x]['BSE']['change_inrs'] = float(change_st[0][0])
    data[x]['BSE']['change_inpc'] = float(change_st[0][1])
    try:
        data[x]['NSE']['volume'] = volume[1]
        data[x]['NSE']['price'] = price[1]
        data[x]['NSE']['change_inrs'] = float(change_st[1][0])
        data[x]['NSE']['change_inpc'] = float(change_st[1][1])
    except():
        pass
    return data
    

def volume_table(soup):
    table = soup.find('table', attrs={'id':'best_5_box_table'})
    table_rows = table.find_all('tr')

    l=[]
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    return pd.DataFrame(l[2:-1], columns=l[1])


def runner(test):
    final_data = [pull_data(x) for x in symbols.keys()] 
    final_data
    final_data_prev = final_data
    return "pass"