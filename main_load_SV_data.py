# -*- coding: utf-8 -*-

__author__ = "Ariel Berdah"
__email__ = "ariel.berdah@stockvider.com"
__date__ = "16/06/07"


import json
from datetime import date

import requests
import pandas as pd
import matplotlib.pyplot as plt


def returnQueryUrl(exchange, symbol, startDate, endDate, indicatorName, 
                   **kwargs):
    '''
    Return the url to query the data from Stockvider API.
    
    exchange (str): name of the stock exchange.
    symbol (str): name of the symbol.
    startDate (date): start date of the data.
    endDate (date): end date of the data.
    indicatorName (str): name of the indicatior.
    
    '''
    
    # Build the basic part of the url.
    # Made of: the exchange, the symbol, the indicator name and the start and
    # end dates.
    url = 'https://api.stockvider.com/data/' + exchange.upper() + '/' 
    url += symbol.upper() + '/' + indicatorName
    url += '?start_date=' + startDate.strftime('%Y-%m-%d') 
    url += '&end_date=' + endDate.strftime('%Y-%m-%d')
    
    # Add any query parameters (contained in kwargs) to the url (api_key, 
    # time_period, ...)
    for (key, value) in kwargs.items():
        url += '&' + str(key) + '=' + str(value)
        
    return url



if __name__ == '__main__':
    
    # In this example, I am asking data on Microsoft stock
    exchange = 'NASDAQ'
    symbol = 'MSFT'
    startDate = date(2014, 5, 1)
    endDate = date(2016, 5, 2)
    
    # Get the query url for the EOD data
    eodQueryUrl = returnQueryUrl(exchange, symbol, startDate, endDate, 'EOD')
    
    # Execute the calls to the API
    eodResponseDocument = requests.get(eodQueryUrl)
    
    if eodResponseDocument.status_code != 200:
        print("API response error. Check the URL and your credentials.")
    else:
        # Parse and load the response to a pandas data frame
        eodJsonContent = json.loads(eodResponseDocument.text)
        eodDataFrame = pd.DataFrame.from_dict(eodJsonContent['Dataset'], 
                                              orient='index')
        
    # Plot the prices
    eodDataFrame.loc[:, ['OPEN', 'HIGH', 'LOW', 'CLOSE']].plot()
    plt.show()
    
    