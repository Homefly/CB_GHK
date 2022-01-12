# %%
%matplotlib widget
from data import CBData
can = CBData.loadData('data/candles_2021-01-01T0:00:00__2021-01-31T18:00:00')
CBData.cleanData(can)
can = can.drop_duplicates()
can

# %%
import numpy as np
from filterpy.gh import GHFilter

hyperParam = {}

for w in np.arange(0., .55, .02):
    print(w)
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
    print(w)

# %%
%matplotlib widget
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
import sys
sys.path.append('../../Kalman-and-Bayesian-Filters-in-Python/kf_book')
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
import sys
sys.path.append('../../Kalman-and-Bayesian-Filters-in-Python/kf_book')
from book_plots import FloatSlider

from ipywidgets import interact
import matplotlib.pyplot as plt
from filterpy.gh import GHKFilter
#zs1 = gen_data(x0=5, dx=5., count=100, noise_factor=50)
#ddx = -5
#zACC = gen_data(x0=5, dx= 5., ddx = -.01, count=1000, noise_factor=50)
#print(zACC)
raw = can['close']

fig = None
def interactive_ghk(x, dx, ddx, g, h, k):
    global fig
    if fig is not None: plt.close(fig)
    fig = plt.figure()
    f = GHKFilter(x=x, dx=dx, dt=1., ddx = ddx, g=g, h=h, k=k)
    data = f.batch_filter(raw)
    #print(data[:, 0])
    days = np.linspace(0, 30, len(raw), endpoint=True)
    plt.scatter(days, raw, edgecolor='k',
                facecolors='none', marker='o', lw=1)
    plt.plot(days, data[1:, 0], color='b')

print(raw.iloc[0])
interact(interactive_ghk,           
         x=FloatSlider(value=raw.iloc[0], min=33000, max=42000), 
         dx=FloatSlider(value=0., min=-50, max=50), 
         ddx=FloatSlider(value=0., min=-1, max=1), 
         g=FloatSlider(value=0.002, min=.0, max=.02, step=.002, readout_format = '.4f'),
         h=FloatSlider(value=1.0e-06, min=.0, max=5e-4, step=1.e-5, readout_format = '.5f'),
         k=FloatSlider(value= 0, min=.0, max=.1, step=.0001, readout_format = '.4f'));

# %%
#close open figures
plt.close('all')

# %%
#some interesting filter values
from filterpy.gh import GHFilter, least_squares_parameters

lsf = GHFilter (0, 0, 1, 0, 0)
z = 10
for i in range(10):
    g,h = least_squares_parameters(i)
    lsf.update(z, g, h)
    print(g, h)

# %%
from filterpy.gh import *
g,h,k = optimal_noise_smoothing(.001)
print(g,h,k)
#f = GHKFilter(0,0,0,1,g,h,k)
#f.update(1.)

# %%
from filterpy.gh.gh_filter import *
critical_damping_parameters(.999)

# %%
print(benedict_bornder_constants(.0002))
print(benedict_bornder_constants(.0002, critical=True))

# %%
from ipywidgets import interact
import matplotlib.pyplot as plt
from filterpy.gh import GHKFilter
from filterpy.gh.gh_filter import *
#zs1 = gen_data(x0=5, dx=5., count=100, noise_factor=50)
#ddx = -5
#zACC = gen_data(x0=5, dx= 5., ddx = -.01, count=1000, noise_factor=50)
#print(zACC)
raw = can['close']

fig = None
def benedict_gh(x, dx, g):
    global fig
    if fig is not None: plt.close(fig)
    fig = plt.figure()
    _, h = benedict_bornder_constants(g=g)
    f = GHFilter(x=x, dx=dx, dt=1., g=g, h=h)
    data = f.batch_filter(raw)
    #print(data[:, 0])
    days = np.linspace(0, len(raw)/(24*60), len(raw), endpoint=True)
    plt.scatter(days, raw, edgecolor='k',
                facecolors='none', marker='o', lw=1)
    plt.plot(days, data[1:, 0], color='b')
    print(g, h)


interact(benedict_gh,           
         x=FloatSlider(value=raw.iloc[0], min=25000, max=30000), 
         dx=FloatSlider(value=0., min=-50, max=50), 
         ddx=FloatSlider(value=0., min=-1, max=1), 
         g=FloatSlider(value=0.001, min=.0, max=.02, step=.0001, readout_format = '.4f'));
         #h=FloatSlider(value=1.0e-06, min=.0, max=5e-4, step=1.e-5, readout_format = '.5f'),
         #k=FloatSlider(value= 0, min=.0, max=.1, step=.0001, readout_format = '.4f'));

# %% [markdown]
# x
# 29079.56
# dx
# 0.00
# g
# 0.0014
# Figure 20
# x=7.851 y=2.736e+04
# 0.0014 9.806864805363754e-07
# 
# #calc 

# %%
# setting GHK
import numpy as np
from filterpy.gh import GHFilter

hyperParam = {}
0.0015
for g in np.linspace(0., 5.e-3, 51):
    print(g)
    _, h = benedict_bornder_constants(g=g)

    hyperParam[str(g)] = {'g': g, 'h':h}
    #import ipdb; ipdb.set_trace()
    f = GHFilter(x = can.iloc[0]['close'], dx = 0., 
                  dt = 1., g = hyperParam[str(g)]['g'], h = hyperParam[str(g)]['h'])
    results = f.batch_filter(list(can['close']))
    #import ipdb; ipdb.set_trace()
    can[f'g:{g:.4f}_x'] = results[1:,0]
    can[f'g:{g:.4f}_dx'] = results[1:,1]
    
    
#f = GHKFilter(x, dx, ddx, dt, g, h, k)

#results = f.batch_filter(list(can['close'])

# %%
from pprint import pprint as pp
pp(list(can.columns))
print(can.columns)
can['g:0.0014_x']

# %%
%matplotlib widget
close = can['close']
days = np.linspace(0, len(close)/(24*60), len(close), endpoint=True)
plt.scatter(days, close, edgecolor='k',
                facecolors='none', marker='o', lw=1)
plt.plot(days, can['g:0.0010_x'])
plt.plot(days, can['g:0.0005_x'])
#plt.plot(days, can['g:0.0008_x'])
#plt.plot(days, can['g:0.0007_x'])
filParams = {'x0':32640, 'dx':0.0, 'dt':1., 'g':.001, 'h':5.00e-7}
#plt.plot(days, can['g:0.0005_x'])
plt.show()

# %%
%matplotlib widget
close = can['close']
days = np.linspace(0, len(close)/(24*60), len(close), endpoint=True)
plt.scatter(days, close, edgecolor='k',
                facecolors='none', marker='o', lw=1)
plt.plot(days, can['g:0.0010_dx'])
#plt.plot(days, can['g:0.0005_x'])
plt.show()

# %%
can['g:0.0010_sdx'] = can['g:0.0010_x'].diff()
temp = can['g:0.0010_sdx'].ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()
print(temp)

can['SMA_sdx10'] = can['g:0.0010_sdx'].rolling(window=30).mean()

can[['g:0.0010_sdx', 'g:0.0010_x']]
can['SMA_sdx10']

# %%
plt.close('all')
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (D)')
ax1.set_ylabel('g:1.e-3', color=color)
ax1.scatter(days, can['close'], color='k')
ax1.plot(days, can['g:0.0010_x'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('dx', color=color)  # we already handled the x-label with ax1

ax2.plot(days, can['SMA_sdx10'], color='tab:pink')
ax2.plot(days, can['g:0.0010_sdx'], color='tab:purple')
ax2.plot(days, can['g:0.0010_dx'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

ax2.axhline(linewidth=2, color='b')
#cushion
cushion = .5
ax2.axhline(y =cushion, linewidth=1, color='b')
ax2.axhline(y =-cushion, linewidth=1, color='b')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# %%
ax2.plot(days, can['SMA_sdx10'], color='tab:pink')

# %%
print(benedict_bornder_constants(.0002))
print(benedict_bornder_constants(.0002, critical=True))

# %%
print(benedict_bornder_constants(.0002))
print(benedict_bornder_constants(.0002, critical=True))

# %%
import numpy as np
from filterpy.gh import GHFilter
from filterpy.gh.gh_filter import *
from data import CBData

canCrit = CBData.loadData('data/candles_2021-01-01T0:00:00__2021-01-31T18:00:00')
#import ipdb; ipdb.set_trace()
print(canCrit)
canCrit = canCrit.append(CBData.loadData('data/candles_2021-02-01T0:00:00__2021-02-28T18:00:00'))
print(canCrit)

hyperParam = {}
for g in np.linspace(0., 5.e-3, 51):
    print(g)
    _, h = benedict_bornder_constants(g=g, critical = True)

    hyperParam[str(g)] = {'g': g, 'h':h}
    #import ipdb; ipdb.set_trace()
    f = GHFilter(x = canCrit.iloc[0]['close'], dx = 0., 
                  dt = 1., g = hyperParam[str(g)]['g'], h = hyperParam[str(g)]['h'])
    results = f.batch_filter(list(canCrit['close']))
    #import ipdb; ipdb.set_trace()
    canCrit[f'g:{g:.4f}_x'] = results[1:,0]
    canCrit[f'g:{g:.4f}_dx'] = results[1:,1]
canCrit.set_index('time')

# %%
import matplotlib.pyplot as plt
%matplotlib widget
plt.clf()

days = np.linspace(0, len(canCritT['close'])/(24*60), len(canCritT['close']), endpoint=True)
canCritT = canCritT.sort_index()
canCritT['close'].plot(x = days, legend = True)


#plt.show()
for g in [0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008]:
    print(f'g:{g:.4f}_x')
    canCritT[f'g:{g:.4f}_x'].plot(x = days, legend = True)

g = 0.0015
canCritT[f'g:{g:.4f}_x'].plot(x = days, legend = True)

# %%

g = 0.0005
print(benedict_bornder_constants(g=g, critical = True))
print(benedict_bornder_constants(g=g, critical = False))
canCritT[f'g:{g:.4f}_x'].plot(x = days, legend = True)


