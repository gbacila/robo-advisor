# this is the "app/robo_advisor.py" file

import os, time, datetime, csv
import pandas as pd
import json
import requests
from dotenv import load_dotenv

#Getting the variables from .env:
load_dotenv()
key=os.getenv("ALPHAVANTAGE_API_KEY")

# Classics
def to_usd(price):
    price = float(price)
    return('${0:,.2f}'.format(price))

# Our get request, we'll use it to pull data from Alpha Vantage
def get_data(symbol):
    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}"
    return requests.get(stock_url)

# Our multistep symbol check. We do the basic check first and then also check if it exists
def ticker_check(symbol):
    chck = get_data(symbol)
    if 2 > len(symbol) or len(symbol) > 5 or any(x.isdigit() for x in symbol):
        return False
    else:
        if "Error" in chck.text: # This is a questionnable step because it uses an extra slot in the allowance (5 requests per minute), but on the other hand, a symbol may look right but not exist, so we don't want to run the analysis for faulty data
            return False
        else:
            return True

# Launching the inputing loop. It collects the symbols, validates them, and manages the input process
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

# General info about the run
cur_date = datetime.datetime.now().strftime("%l:%M%p %z on %b %d, %Y.")   
print("This report was run at:",cur_date)
print("-------------------------")

# Launching the main action loop to create .csv files and print results for every valid symbol entered
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

    # Printing out the recommendations from the current dataframe. This is done in one cycle to take advantage of the DF in memory - we don't have to load it again and don't need to keep them all in a list (saving resources)
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