import pandas as pd 
import csv



open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

full_df = pd.HDFStore('SP500_full_data.h5')


stock_list = []


for ticker in ticker_list:
    try:
        full_data = full_df.get(ticker[0])
        dates = list(full_data.index)[-2:]
        
        for x in range(len(dates)):
                if full_data.loc[dates[x], "RSI"] > 45 and full_data.loc[dates[x-1],"RSI"] < 45:
                    stock_list.append(ticker[0])

    except:
        print(f'The {ticker} could not be found.')   

print(stock_list)    