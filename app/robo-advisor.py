# this is the "app/robo_advisor.py" file

import os
import pandas as pd
import datetime
import json
import csv
import requests
from dotenv import load_dotenv

#Getting the variables:
load_dotenv()
key=os.getenv("ALPHAVANTAGE_API_KEY")

#print(KEY)
#def validation(symbol):

def get_data(symbol):
    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}"
    return requests.get(stock_url)

def ticker_check(symbol):
    chck = get_data(symbol)
    if (4 > len(symbol) > 5) or any(x.isdigit() for x in symbol) or "Error" in chck.text:
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

for x in smbs:
    df = pd.DataFrame(json.loads(get_data(x).text))
    cur_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"data/{x}-{cur_date}.csv" # https://stackoverflow.com/questions/10607688/how-to-create-a-file-name-with-the-current-date-time-in-python
    df.to_csv(filename)
    print(df)


#It may also optionally prompt the user to specify additional inputs such as risk 
#tolerance and/or other trading preferences, as desired and applicable

#Otherwise, if preliminary validations are satisfied, the system should proceed to issue a GET request to the AlphaVantage API to retrieve corresponding stock market data. NOTE: use one of the "Adjusted" URL endpoints to account for stock splits.
#
#Information Output Requirements
#After receiving a successful API response, the system should write historical stock prices to one or more CSV files located in the repository's "data" directory. The CSV file contents should resemble the following example:
#
#timestamp, open, high, low, close, volume
#2018-06-04, 101.2600, 101.8600, 100.8510, 101.6700, 27172988
#2018-06-01, 99.2798, 100.8600, 99.1700, 100.7900, 28655624
#2018-05-31, 99.2900, 99.9900, 98.6100, 98.8400, 34140891
#2018-05-30, 98.3100, 99.2500, 97.9100, 98.9500, 22158528
#HINT: create a pandas.DataFrame object from the time series data, and invoke the dataframe's to_csv() method to easily write it to a local CSV file.
#
#If the system processes only a single stock symbol at a time, the system may use a single CSV file named "data/prices.csv", or it may use multiple CSV files, each with a name corresponding to the given stock symbol (e.g. "data/prices_msft.csv, "prices_aapl.csv", etc.). If the system processes multiple stock symbols at a time, it should use multiple files, each with a name corresponding to the given stock symbol (e.g. "data/prices_msft.csv", "prices_aapl.csv", etc.).
#
#After writing historical data to a CSV file, the system should perform calculations (see "Calculation Requirements" section below) to produce/print the following outputs:
#
#The selected stock symbol(s) (e.g. "Stock: MSFT")
#The date and time when the program was executed, formatted in a human-friendly way (e.g. "Run at: 11:52pm on June 5th, 2018")
#The date when the data was last refreshed, usually the same as the latest available day of daily trading data (e.g. "Latest Data from: June 4th, 2018")
#For each stock symbol: its latest closing price, its recent high price, and its recent low price, calculated according to the instructions below, and formatted as currency with a dollar sign and two decimal places with a thousands separator as applicable (e.g. "Recent High: $1,234.56", etc.)
#A recommendation as to whether or not the client should buy the stock (see guidance below), and optionally what quantity to purchase. The nature of the recommendation for each symbol can be binary (e.g. "Buy" or "No Buy"), qualitative (e.g. a "Low", "Medium", or "High" level of confidence), or quantitative (i.e. some numeric rating scale).
#A recommendation explanation, describing in a human-friendly way the reason why the program produced the recommendation it did (e.g. "because the stock's latest closing price exceeds threshold XYZ, etc...")
#NOTE: the CSV files are information outputs of this system, not information inputs. So it shouldn't be necessary for your program to read a CSV file to perform calculations. The JSON API responses should have all the information your program needs to perform calculations.
#
#Calculation Requirements
#The latest closing price should be equal to the stock's "close" price on the latest available day of trading data.
#
#The recent high price should be equal to the maximum daily "high" price over approximately the past 100 available days of trading data.
#
#The recent low price should be calculated in a similar manner as the recent high price, but it should instead be equal to the minimum of all daily "low" prices.
#
#NOTE: By default, the daily data returned by the AlphaVantage API uses an outputsize parameter value of compact. This "compact" response should provide daily data covering the previous 100 trading days, which is sufficient to use to calculate the recent high and recent low prices. It is acceptable and recommended to use these default, "compact" responses to calculate these recent prices.
#
#You are free to develop your own custom recommendation algorithm. This is perhaps one of the most fun and creative parts of this project. 😃 One simple example algorithm would be (in pseudocode): If the stock's latest closing price is less than 20% above its recent low, "Buy", else "Don't Buy".
#
#Guided Screencast
#For a more in-depth guided exercise walkthrough, feel free but not obligated to follow the screencast, but keep in mind a few caveats:
#
#Some of the links reference a previous course repository, but you should be able to find related documents in this course repository as well.
#The video advocates using the csv module for writing a CSV file, but you're encouraged to use the pandas package instead!
#The video demonstrates fetching data from a non-adjusted URL endpoint, but you should make requests to one of the "adjusted" endpoints instead!
#If there are any discrepancies between requirements referenced in the video and requirements stated in this document, defer to the requirements stated in this document.
#Further Exploration Challenges
#If you are able to implement the basic requirements with relative ease, consider addressing one or more of these "Further Exploration Challenges" to enrich and expand your learning experience.

#print("-------------------------")
#print("SELECTED SYMBOL: XYZ")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: 2018-02-20 02:00pm")
#print("-------------------------")
#print("LATEST DAY: 2018-02-20")
#print("LATEST CLOSE: $100,000.00")
#print("RECENT HIGH: $101,000.00")
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")