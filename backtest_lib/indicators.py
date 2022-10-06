import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

def peaks_and_troughs(data_df, order=5):
    # https://raposa.trade/blog/higher-highs-lower-lows-and-calculating-price-trends-in-python/
    data = data_df.copy()
    # data['local_max'] = data['Close'][(data['Close'].shift(1) < data['Close']) &
    #                                   (data['Close'].shift(-1) < data['Close']) ]
    # data['local_min'] = data['Close'][(data['Close'].shift(1) > data['Close']) &
    #                                   (data['Close'].shift(-1) > data['Close'])]
    
    # Get index (dates) of highs and lows (adjust order to widen interval scope for detection)
    max_idx = argrelextrema(data['Close'].values, np.greater, order=order)[0]
    min_idx = argrelextrema(data['Close'].values, np.less, order=order)[0]                                      
    data['Peaks'] = pd.NA
    data.iloc[max_idx, data.columns.get_loc('Peaks')] = data.iloc[max_idx]['Close']
    data['Troughs'] = pd.NA
    data.iloc[min_idx, data.columns.get_loc('Troughs')] = data.iloc[min_idx]['Close']

    return data