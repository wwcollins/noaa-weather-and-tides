import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize

table_MN = pd.read_html('https://en.wikipedia.org/wiki/Minnesota')

# https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1748#listing
url = 'https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1748#listing'
url = 'https://en.wikipedia.org/wiki/Minnesota'
table_MN = pd.read_html(url)

print(f'Total tables: {len(table_MN)}')