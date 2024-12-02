import yfinance as yf

#List of top stocks
topStocks = ['AAPL', 'NVDA', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-B', 'WMT', 'V']
#Dictionary to hold each stock and info
topStocksDict = {}

for ticker in topStocks: #Get data for all 10 stock using the tickers in topStocks
    stock = yf.Ticker(ticker) #Create ticker object to collect data
    stock_info = stock.info  #Retrieve company info for the stock
    topStocksDict[ticker] = { #Place dictionary for stock in topStocksDict
        'Company Name': stock_info.get('longName', 'N/A'),
        'Current Price': stock_info.get('currentPrice', 'N/A'),
        'Sector': stock_info.get('sector', 'N/A'),
        'Day High': stock_info.get('dayHigh', 'N/A'),
        'Day Low': stock_info.get('dayLow', 'N/A'),
        '52 Week High': stock_info.get('fiftyTwoWeekHigh', 'N/A'),
        '52 Week Low': stock_info.get('fiftyTwoWeekLow', 'N/A'),
        'Dividend Rate' : stock_info.get('dividendRate', 'N/A'),
        'Market Cap': stock_info.get('marketCap', 'N/A'),
    }

#print nested dictionary
for key in topStocksDict: 
    print(key)
    print(topStocksDict[key])
