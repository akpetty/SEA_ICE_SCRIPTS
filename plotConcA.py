
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

m = Basemap(projection='npstere',boundinglat=65,lon_0=0, resolution='l'  )

dataPath = '../../../DATA/'
figpath='./Figures/'


def getMeanConcDates(dataPath, alg=0, date1='20151220', date2='20160105', lonlat=0, mean=0):
	if (alg==0):
		team = 'NASA_TEAM'
		team_s = 'nt'
		header = 300
		datatype='uint8'
		scale_factor=250.
	if (alg==1):
		team = 'BOOTSTRAP'
		team_s = 'bt'
		header = 0
		datatype='<i2'
		scale_factor=1000.

	year = date1[0:4]
	print year
	day=0
	if (int(year)>2015):
		files = glob(dataPath+'/ICE_CONC/NRT/'+team_s+'_'+'*.bin')	
	else:
		files = glob(dataPath+'/ICE_CONC/'+team+'/ARCTIC/daily/'+year+'/'+team_s+'_'+'*.bin')

	dates=[file.split('/')[-1][3:11] for file in files]
	print dates
	idx1=where(array(dates)==date1)[0][0]
	idx2=where(array(dates)==date2)[0][0]
	files=files[idx1:idx2+1]
	ice_conc = ma.masked_all((size(files), 448, 304))

	for x in xrange(size(files)):
		fd = open(files[x], 'r')
		data = fromfile(file=fd, dtype=datatype)
		data = data[header:]
		#FIRST 300 FILES ARE HEADER INFO
		ice_conc[x] = reshape(data, [448, 304])
		
	#divide by 250 to express in concentration
	ice_conc = ice_conc/scale_factor
	#GREATER THAN 250 is mask/land etc
	ice_conc = ma.masked_where(ice_conc>1., ice_conc)
	#ice_conc = ma.masked_where(ice_conc<0.15, ice_conc)
	if (mean==1):
		ice_conc=ma.mean(ice_conc, axis=0)

	if (lonlat==1):
		flat = open(dataPath+'/OTHER/psn25lats_v3.dat', 'rb')
		flon = open(dataPath+'/OTHER/psn25lons_v3.dat', 'rb')
		lats = reshape(fromfile(file=flat, dtype='<i4')/100000., [448, 304])
		lons = reshape(fromfile(file=flon, dtype='<i4')/100000., [448, 304])
		return ice_conc, lons, lats
	else:
		return ice_conc
	

date1='20111020'
date2='20111030'

ice_conc, lons, lats = siF.getMeanConcDates(dataPath, alg=0, date1=date1, date2=date2, lonlat=1, mean=1)
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
cax = fig.add_axes([0.77, 0.95, 0.12, 0.03])
cbar = colorbar(im1,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label(label_str, labelpad=1)
cbar.set_ticks(np.arange(minval, maxval+0.1, 1))
cbar.solids.set_rasterized(True)
#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
#cbar.set_clim(minval, maxval)

subplots_adjust(bottom=0., top=1., left=0.0, right=1.)
savefig(figpath+'/conc'+date1+'-'+date2+'.png', dpi=300)
close(fig)


