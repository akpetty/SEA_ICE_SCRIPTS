
############################################################## 
# Date: 01/01/16
# Name: plot_conc3.py
# Author: Alek Petty
# Description: Script to plot conc
# Input requirements: ice conc data

import matplotlib
matplotlib.use("AGG")
import sys
sys.path.append('/Users/aapetty/GitRepos/BitBucket/ice_prediction')
import pred_funcs as pfuncs
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

m = Basemap(projection='npstere',boundinglat=65,lon_0=0, resolution='l'  )

datapath = '../../../DATA/'
figpath='./Figures/'

start_year=2005
end_year=2016
month=6

xpts, ypts, lons, lats, conc_years = pfuncs.get_conc_years(m, datapath, start_year, end_year, month=month, alg=0)
years=np.arange(start_year, end_year+1, 1)

mean_conc_years = ma.mean(conc_years[0:-1], axis=0)
melt=[]
ice_area=[]

if (month==2):
	mon_str='Mar'
if (month==3):
	mon_str='Apr'
if (month==4):
	mon_str='May'
if (month==5):
	mon_str='June'
if (month==6):
	mon_str='July'
if (month==7):
	mon_str='Aug'


textwidth=5.
fig = figure(figsize=(textwidth,textwidth*0.42))
subplots_adjust(bottom=0.205, top=0.98, left=0.01, right=0.99, wspace=0.02)

ax1=subplot(1, 3, 1)
minval=0
maxval=1
#ADD GRIDSIZE=NUMBER KWARG TO HEXBIN IF YOU WANT TO CHANGE SIZE OF THE BINS
im1 = m.pcolormesh(xpts , ypts, mean_conc_years, cmap=cm.viridis, vmin=minval, vmax=maxval,shading='gouraud', zorder=2)
#im2 = m.contour(xpts , ypts, ma.mean(Pressure, axis=0),levels=[990, 1000, 1100],colors='k', zorder=4)
m.drawcoastlines(linewidth=0.25, zorder=5)
m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)


#ax1.annotate(files[x][-8:-4]+'-'+files[x][-4:-2]+'-'+files[x][-2:], xy=(0.98, 0.98), bbox=bbox_args,xycoords='axes fraction', horizontalalignment='right', verticalalignment='top', zorder=10)
label_str='Concentration'
ax1.annotate(str(start_year)+'-'+str(end_year-1), xy=(0.02, 0.86),xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)
cax = fig.add_axes([0.07, 0.16, 0.2, 0.035])
cbar = colorbar(im1,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label(label_str, labelpad=1)
cbar.set_ticks(np.arange(minval, maxval+0.1, 1))
cbar.solids.set_rasterized(True)
#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
#cbar.set_clim(minval, maxval)

ax2=subplot(1, 3, 2)
minval=0
maxval=1
#ADD GRIDSIZE=NUMBER KWARG TO HEXBIN IF YOU WANT TO CHANGE SIZE OF THE BINS
im2 = m.pcolormesh(xpts , ypts,conc_years[-1], cmap=cm.viridis, vmin=minval, vmax=maxval,shading='gouraud', zorder=2)
m.drawcoastlines(linewidth=0.25, zorder=5)
m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)

ax2.annotate(str(end_year), xy=(0.02, 0.86),xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)

label_str='Concentration'
cax2 = fig.add_axes([0.4, 0.16, 0.2, 0.035])
cbar2 = colorbar(im2,cax=cax2, orientation='horizontal', extend='both', use_gridspec=True)
cbar2.set_label(label_str, labelpad=1)
cbar2.set_ticks(np.arange(minval, maxval+0.1, 1))
cbar2.solids.set_rasterized(True)
#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
#cbar.set_clim(minval, maxval)

ax3=subplot(1, 3, 3)
minval=-1
maxval=1
#ADD GRIDSIZE=NUMBER KWARG TO HEXBIN IF YOU WANT TO CHANGE SIZE OF THE BINS
im3 = m.pcolormesh(xpts , ypts, conc_years[-1]-mean_conc_years, cmap=cm.RdBu, vmin=minval, vmax=maxval,shading='gouraud', zorder=2)
m.drawcoastlines(linewidth=0.25, zorder=5)
m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)
label_str=r'$\Delta$'

cax3 = fig.add_axes([0.73, 0.16, 0.2, 0.035])
cbar3 = colorbar(im3,cax=cax3, orientation='horizontal', extend='both', use_gridspec=True)
cbar3.set_label(label_str, labelpad=1)
cbar3.set_ticks([minval, 0, maxval])
cbar3.solids.set_rasterized(True)

savefig(figpath+'/conc'+mon_str+'v11.png', dpi=300)
close(fig)


