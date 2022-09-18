import pandas as pd 
import csv

open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

cleandf = pd.HDFStore('SP500_full_data.h5')
full_df = pd.HDFStore('SP500_full_data.h5')

right_count = 0
total_count = 0

for ticker in ticker_list:
    try:
        clean_data = cleandf.get(ticker[0])
        clean_data = clean_data.astype('float64')
        #fulldf = full_df.get(ticker[0])
        dates = list(clean_data.index)
        for x in range(len(dates)):
            if (x+5) < len(dates):
                total_count += 1

                if (clean_data.loc[dates[x+5], 'Close'] < clean_data.loc[dates[x], 'BBUpper']) and (clean_data.loc[dates[x+5], 'Close'] > clean_data.loc[dates[x], 'BBLower']):
                    right_count += 1

    except:
        print(f'The {ticker} could not be found.')

print(f'Right Count: {right_count}')
print(f'Total Count: {total_count}')
print(f'Accuracy: {right_count/total_count}')