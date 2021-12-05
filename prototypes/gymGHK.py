from CB_GHK import CB_GHK
import pandas as pd

exp = pd.Dataframe(['time', 'G', 'H', 'K', 'pred'])
#set index to int

#import data

for G in range(0, 1, .05):
    for H in range(0, 1, .05):
        for K in range(0, 1, .05):
            exp[['G', 'H', 'K']] = G, H, K
            #x, dx = CB_GHK.batch_filter(data)