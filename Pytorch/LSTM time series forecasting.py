import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import yfinance as yf
from tqdm import tqdm
from datetime import date
from sklearn.preprocessing import MinMaxScaler

import statsmodels.tsa.api as tsa
from statsmodels.graphics import tsaplots

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import mean_squared_error, r2_score
from collections import defaultdict

# set graph theme
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
Color_Palette = sns.color_palette(['#01BEFE', '#FF7D00', '#FFDD00', '#FF006D', '#ADFF02', '#8F00FF'])
sns.set_palette(Color_Palette)

tqdm.pandas()

# download data
end_date = date.today().strftime("%Y-%m-%d")
start_date = '2000-01-01'

appl_df = yf.download(['AAPL'], start=start_date, end=end_date)
appl_df.columns.droplevel()
appl_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

appl_df.to_csv('AAPL_df.csv')
# print(appl_df)

plt.plot(appl_df['Close'])
plt.show()

tsaplots.acf(appl_df['Close']) # also try appl_df

# tsaplots.acf(appl_df)

plt.show()






# if __name__ == "__main__":



