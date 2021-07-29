# "Robo Advisor" Project
My study project on stocks advisory services using Alpha Vantage API

# Prerequisites

+ Anaconda
+ Python 3.8
+ Pip

## Installation

Clone or download [this repository](https://github.com/gbacila/robo-advisor) or get it using the command below

```
git clone https://github.com/gbacila/robo-advisor.git # This is the HTTP address

```
## Setup

Create and activate a new Anaconda virtual environment:

```
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```
Install the packages from requirements.txt:

```
pip install -r requirements.txt
```
Register in AlphaVantage to get your unique API using [this link](https://www.alphavantage.co/support/#api-key)

Create a local .env file and add your unique API key assigning it to the variable ALPHAVANTAGE_API_KEY like in the example below (abc123 is the example key):

```
ALPHAVANTAGE_API_KEY="abc123"
```
## Usage

Launch the program by navigating to its folder and using the command line:
```
python app/robo_advisor.py
```
Enter one or several symbols you want to get recommendations for and see the results

IMPORTANT: Depending on your license, you may have limitations on how many tickers and how often you can pull. If you exceed your license's limitations, the program may return an error