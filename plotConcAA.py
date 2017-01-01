
############################################################## 
# Date: 01/01/16
# Name: plot_concA.py
# Author: Alek Petty
# Description: Script to plot conc
# Input requirements: ice conc data

import matplotlib
matplotlib.use("AGG")
import seaiceFuncs as siF
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma
from matplotlib import rc
from glob import glob
import matplotlib.patches as patches
from netCDF4 import Dataset

#viridis=pfuncs.get_new_cmaps(cmap_str='viridis')
rcParams['xtick.major.size'] = 2
rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .25
rcParams['lines.linewidth'] = .25
rcParams['patch.linewidth'] = .25
rcParams['axes.labelsize'] = 8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

m = Basemap(projection='spstere',boundinglat=-56.,lon_0=180, round=True, lat_ts=0.0,resolution='l'  )

dataPath = '../../../DATA/'
figpath='./Figures/'


date1='20111020'
date2='20111030'

ice_conc, lons, lats = siF.getMeanConcDates(dataPath, poleStr='AA', alg=0, date1=date1, date2=date2, lonlat=1, mean=1)
xpts, ypts =m(lons, lats)


textwidth=3.
minval=0
maxval=1

####
fig = figure(figsize=(textwidth,textwidth))
ax1=subplot(1, 1, 1)

im1 = m.pcolormesh(xpts , ypts, ice_conc, cmap=cm.viridis, vmin=minval, vmax=maxval,shading='gouraud', zorder=2)
m.drawcoastlines(linewidth=0.25, zorder=5)
m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)

#ax1.annotate(files[x][-8:-4]+'-'+files[x][-4:-2]+'-'+files[x][-2:], xy=(0.98, 0.98), bbox=bbox_args,xycoords='axes fraction', horizontalalignment='right', verticalalignment='top', zorder=10)
label_str=r'$A$'
#ax1.annotate(str(start_year)+'-'+str(end_year-1), xy=(0.02, 0.86),xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)
cax = fig.add_axes([0.84, 0.95, 0.12, 0.03])
cbar = colorbar(im1,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label(label_str, labelpad=1)
cbar.set_ticks(np.arange(minval, maxval+0.1, 1))
cbar.solids.set_rasterized(True)
#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
#cbar.set_clim(minval, maxval)

subplots_adjust(bottom=0., top=1., left=0.0, right=1.)
savefig(figpath+'/conc'+date1+'-'+date2+'AA.png', dpi=300)
close(fig)


