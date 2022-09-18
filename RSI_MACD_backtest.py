import pandas as pd 
import csv

open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

cleandf = pd.HDFStore('SP500_clean_data.h5')

right_count = 0
total_count = 0

for ticker in ticker_list:
    try:
        clean_data = cleandf.get(ticker[0])
        dates = list(clean_data.index)
        for x in range(len(dates)):
            if x > 0:
                if clean_data.loc[dates[x], "MACDHisto"] > 0 and clean_data.loc[dates[x-1],"MACDHisto"] < 0 and clean_data.loc[dates[x], "RSI"] > 30 and clean_data.loc[dates[x-1], "RSI"] < 30:
                        total_count += 1
                        if clean_data.loc[dates[x], "Returns_Binary"] == 1:
                            right_count += 1
    except:
        print(f'The {ticker} could not be found.')

print(f'Right Count: {right_count}')
print(f'Total Count: {total_count}')
print(f'Accuracy: {right_count/total_count}')