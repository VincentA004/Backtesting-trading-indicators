import pandas as pd 
import csv
import math
import logging 

open_file = open('SP500.csv','r')
csv_file = csv.reader(open_file, delimiter = ',')
ticker_list = list(csv_file)

cleandf = pd.HDFStore('SP500_full_data.h5')
full_df = pd.HDFStore('SP500_full_data.h5')



logging.basicConfig(filename = f'RSI_backtest_short.log', filemode= 'w', level = logging.INFO)

#ticker_list =[['ABBV']]


def backtest(n1, n2):
    right_count = 0
    total_count = 0

    buy = []
    buy_price = []
    sell_price = []
    total_profit = 0
    avg_invest = 0


    for ticker in ticker_list:
        try:
            clean_data = cleandf.get(ticker[0])
            clean_data = clean_data.astype('float64')
            #fulldf = full_df.get(ticker[0])
            dates = list(clean_data.index)
            for x in range(len(dates)):
                if x > 0:
                    if clean_data.loc[dates[x], "RSI"] < n2 and clean_data.loc[dates[x-1],"RSI"] > n2:
                        if(len(buy) < 1):
                            buy.append(dates[x])
                            buy_price.append(clean_data.loc[dates[x], "Close"])
                    elif clean_data.loc[dates[x], "RSI"] > n1 and clean_data.loc[dates[x-1],"RSI"] < n1:
                        if len(buy) > 0:
                            total_count += 1
                            avg_invest += 100 * clean_data.loc[buy[0], 'Close']
                            total_profit += 100*(clean_data.loc[buy[0],'Close'] - clean_data.loc[dates[x], 'Close'])
                            if clean_data.loc[buy[0], 'Close'] < clean_data.loc[dates[x],'Close']:
                                sell_price.append(clean_data.loc[dates[x], "Close"])
                                right_count += 1
                            del buy[0]
        except:
            print(f'The {ticker} could not be found.')

    average = 0 

    for x in range(len(sell_price)):
        average += ((float(sell_price[x])/float(buy_price[x])))

    avg_invest = avg_invest/total_count

    logging.info(f'Buy Parameter: {n1}')
    logging.info(f'Sell Parameter: {n2}')
    logging.info(f'Right Count: {right_count}')
    logging.info(f'Total Count: {total_count}')
    logging.info(f'Accuracy: {right_count/total_count}')
    logging.info(f'Average Increase in Price: {average/len(sell_price)}')
    logging.info(f'Total Profit: {total_profit}')
    logging.info(f'Avg Investment: {avg_invest}')
    

def main():
    backtest(45,75)

main()