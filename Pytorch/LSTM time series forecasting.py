import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# import seaborn as sns
# from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import mean_squared_error, r2_score
from collections import defaultdict

appl_df = yf.download('AAPL')
print(appl_df)






