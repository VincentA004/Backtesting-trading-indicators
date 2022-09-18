import pandas as pd 
import csv
import logging



open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

cleandf = pd.HDFStore('SP500_full_data.h5')
full_df = pd.HDFStore('SP500_full_data.h5')

right_count = 0
total_count = 0

logging.basicConfig(filename = f'RSI_SMA200_backtest5.log', filemode= 'w', level = logging.INFO)

buy = []
sell = []
avg_invest = 0
total_profit = 0

buy_price = []
sell_price = []

data = {}

for ticker in ticker_list:
    try:
        clean_data = cleandf.get(ticker[0])
        clean_data = clean_data.dropna()
        clean_data = clean_data.astype('float64')
        dates = list(clean_data.index)
        data[ticker[0]] = {}
        for x in range(len(dates)):
            if x > 0 and x < len(dates)-1:
                if (clean_data.loc[dates[x], "SMA200"] > clean_data.loc[dates[x],"Close"]) and clean_data.loc[dates[x], "RSI"] > 45 and clean_data.loc[dates[x-1],"RSI"] < 45:
                    if len(buy) < 1:
                        buy.append(dates[x])
                        buy_price.append(clean_data.loc[dates[x], "Close"])
                        data[ticker[0]][dates[x]] = f'Buy Price : {clean_data.loc[dates[x], "Close"]}'
                elif clean_data.loc[dates[x], "RSI"] < 75 and clean_data.loc[dates[x-1],"RSI"] > 75 :
                    if len(buy) > 0:
                        total_count += 1
                        avg_invest += 100 * clean_data.loc[buy[0], 'Close']
                        total_profit += 100*(clean_data.loc[dates[x],'Close'] - clean_data.loc[buy[0], 'Close'])
                        sell_price.append(clean_data.loc[dates[x], "Close"])
                        data[ticker[0]][dates[x]] = f'Sell Price: {clean_data.loc[dates[x],"Close"]}'
                        if clean_data.loc[buy[0],'Close'] < clean_data.loc[dates[x],'Close']:
                            right_count += 1
                        del buy[0]
    except Exception as e:
        print(e)
        print(f'The {ticker} could not be found.')
average = 0 

for x in range(len(sell_price)):
    average += ((float(sell_price[x])-float(buy_price[x])))

logging.info(f'Right Count: {right_count}')
logging.info(f'Total Count: {total_count}')
logging.info(f'Accuracy: {right_count/total_count}')
logging.info(f'Average Increase in Price: {average/len(sell_price)}')
logging.info(f'Total Profit: {total_profit}')
logging.info(f'Avg Investment: {avg_invest/total_count}')
logging.info(f'Buy/Sell Data: {data}')