import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

df = pd.read_csv(
    r'C:\Users\preya\OneDrive\Desktop\Spotify Data Analysis\processed_data\artists_final.csv',
    encoding='latin1'
)


print(df.head())

# Quick double check that Python sees the same clean data
print(df.info())
print(df.describe())

