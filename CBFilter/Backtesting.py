# %% Load libraries
from  data import CBData
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

can = CBData.loadData('/home/dockimble/projects/CB_GHK/CBFilter/data/candles_2021-01-01T0:00:00__2021-01-31T18:00:00')
CBData.cleanData(can)
can.drop_duplicates()

# %% setup GHK
from filterpy.gh import GHFilter

hyperParam = {}

for w in np.arange(0., .55, .02):
    # print(w)
    g = 2 * w
    h = 2 * w**2
    #k = w**3
    hyperParam[str(w)] = {'g': g, 'h':h}
    #import ipdb; ipdb.set_trace()
    f = GHFilter(x = can.iloc[0]['close'], dx = 0., 
                  dt = 1., g = hyperParam[str(w)]['g'], h = hyperParam[str(w)]['h'])
    results = f.batch_filter(list(can['close']))
    #import ipdb; ipdb.set_trace()
    can[f'w:{w:.2f}_x'] = results[1:,0]
    can[f'w:{w:.2f}_dx'] = results[1:,1]
    print(f)
# %%
#plt.ioff()
can.iloc[0:10]
can['delMin'] = can['del']/60
can['delMin'] = pd.to_numeric(can['delMin'], downcast='integer')
can.head()
can.plot(x= 'delMin', y = ['close', 'w:0.02_x', 'w:0.04_x', 'w:0.06_x'])
#can.plot(x= 'delMin', y = ['close', 'w:0.05_x', 'w:0.10_x', 'w:0.15_x'])


#plt.close("all")
#plt.plot(s)
plt.show()


# %%
# Load from Kalman filter book
sys.path.append('/home/dockimble/projects/Kalman-and-Bayesian-Filters-in-Python/kf_book')
from book_plots import FloatSlider
from ipywidgets import interact
import matplotlib.pyplot as plt
from filterpy.gh import GHKFilter

#zs1 = gen_data(x0=5, dx=5., count=100, noise_factor=50)
#ddx = -5
#zACC = gen_data(x0=5, dx= 5., ddx = -.01, count=1000, noise_factor=50)
#print(zACC)

raw = can['close'][:5000]

fig = None
def interactive_gh(x, dx, g, h):
    global fig
    if fig is not None: plt.close(fig)
    fig = plt.figure()
    f = GHFilter(x=x, dx=dx, dt=1., g=g, h=h,)
    data = f.batch_filter(raw)
    #print(data[:, 0])
    plt.scatter(range(len(raw)), raw, edgecolor='k', 
                facecolors='none', marker='o', lw=1)
    plt.plot(data[:, 0], color='b')

print(raw.iloc[0])
interact(interactive_gh,           
         x=FloatSlider(value=raw.iloc[0], min=33000, max=42000), 
         dx=FloatSlider(value=0., min=-50, max=50), 
         #ddx=FloatSlider(value=-.1, min=-1, max=1), 
         g=FloatSlider(value=.01, min=.0, max=.02, step=.002, readout_format = '.4f'),
         h=FloatSlider(value=.0001, min=.0, max=5e-4, step=1.e-5, readout_format = '.5f'))
         #k=FloatSlider(value=.00, min=.0, max=.1, step=.0001, readout_format = '.4f'));


# %%
