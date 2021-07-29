# this is the "app/robo_advisor.py" file

import os, time, datetime, csv
import pandas as pd
import json
import requests
from dotenv import load_dotenv

#Getting the variables:
load_dotenv()
key=os.getenv("ALPHAVANTAGE_API_KEY")

def to_usd(price):
    price = float(price)
    return('${0:,.2f}'.format(price))

def get_data(symbol):
    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}"
    return requests.get(stock_url)

def ticker_check(symbol):
    chck = get_data(symbol)
    if (2 > len(symbol) > 5) or any(x.isdigit() for x in symbol) or "Error" in chck.text:
        return False
    else:
        return True

smbs =[]

inputing = True

while inputing:
    s = input("Enter the symbol: ")
    s = s.upper()
    if ticker_check(s):
        smbs.append(s)
        check = str(input("The input is valid. Do you want to add another ticker? (Y/N): ")).lower()
        if check == "n":
            inputing = False
        elif check != "y" and check != "n":
            print("The input is incorrect, we'll continue with what we have.")  
            inputing = False  
    else: 
        if s == "EXIT": break
        else: print("The symbol is incorrect, try again or type exit")

cur_date = datetime.datetime.now().strftime("%l:%M%p %z on %b %d, %Y.")   
print("This report was run at:",cur_date)
print("-------------------------")

for x in smbs:
    frm = json.loads(get_data(x).text)
    df = pd.DataFrame(frm["Time Series (Daily)"])
    df = df.transpose()
    columns = [4, 6, 7]
    df.drop(df.columns[columns], axis=1, inplace=True) # https://stackoverflow.com/questions/20297317/python-dataframe-pandas-drop-column-using-int
    cur_date = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
    filename = f"data/prices_{x}-{cur_date}.csv" # https://stackoverflow.com/questions/10607688/how-to-create-a-file-name-with-the-current-date-time-in-python
    df.to_csv(filename, header=["open","high","low","close","volume"], index_label="timestamp")
    latest_date = datetime.datetime.fromisoformat(df.index[0])

    print("Stock:",x)
    print("Latest data from:",latest_date.strftime("%B %d, %Y"))
    print("Latest closing price:",to_usd(df.iat[0,3]))    
    print("Recent high price:",to_usd(df["2. high"].max()))
    print("Recent low price:",to_usd(df["3. low"].min()))

    if float(df.iat[0,3]) <= float(df["3. low"].min()) * 1.2:
        print("RECOMMENDATION: BUY!")
        print("RECOMMENDATION REASON: The stock's latest closing price is less than 20% above its recent low")
    else:
        print("RECOMMENDATION: SELL!")
        print("RECOMMENDATION REASON: The stock's latest closing price is more than 20% above its recent low.")
    print("-------------------------")

print("HAPPY INVESTING!")
print("-------------------------")