import pandas as pd 
import csv



open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

cleandf = pd.HDFStore('SP500_full_data.h5')
full_df = pd.HDFStore('SP500_full_data.h5')

right_count = 0
total_count = 0

buy = []
sell = []



for ticker in ticker_list:
    try:
        clean_data = cleandf.get(ticker[0])
        clean_data = clean_data.astype('float64')
        #fulldf = full_df.get(ticker[0])
        dates = list(clean_data.index)
        for x in range(len(dates)):
            if x > 0:
                if clean_data.loc[dates[x], "AroonOSC"] > 0 and clean_data.loc[dates[x-1], "AroonOSC"] < 0:
                    if len(buy) < 1:
                        buy.append(dates[x])
                elif clean_data.loc[dates[x], "AroonOSC"] < 0 and clean_data.loc[dates[x-1], "AroonOSC"] > 0:
                    if len(buy) > 0:
                        total_count += 1
                        
                        if clean_data.loc[buy[0], 'Close'] < clean_data.loc[dates[x],'Close']:
                            right_count += 1
                        del buy[0]
    except:
        print(f'The {ticker} could not be found.')

print(f'Right Count: {right_count}')
print(f'Total Count: {total_count}')
print(f'Accuracy: {right_count/total_count}')