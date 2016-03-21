import matplotlib
matplotlib.use("AGG")

# basemap import
from mpl_toolkits.basemap import Basemap, shiftgrid
# Numpy import
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma
import string
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid.inset_locator import mark_inset
from mpl_toolkits.axes_grid.anchored_artists import AnchoredSizeBar
from scipy import stats
from matplotlib import rc
from netCDF4 import Dataset
from glob import glob
from scipy.interpolate import griddata
import csv

rcParams['axes.labelsize'] = 10
rcParams['xtick.labelsize']=10
rcParams['ytick.labelsize']=10
rcParams['legend.fontsize']=10
rcParams['font.size']=10
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

def get_min_max_extent():
	yearsL=[]
	extentL=[]
	rownum=0
	with open('../../DATA/ICE_CONC/NH_seaice_extent_final.csv', 'rb') as csvfile:
		datafile = csv.reader(csvfile)
		for row in datafile:
			if (rownum<2):
				header=row
				rownum+=1
			else:
				yearsL.append(row[0])
				extentL.append(row[3])
				rownum+=1

	yearsM=asarray(yearsL)
	yearsM = yearsM.astype(int)
	extent=asarray(extentL)
	extent=extent.astype(float)

	max_extent=[]
	min_extent=[]
	for x in xrange(1980, 2015, 1):
		max_extent.append(np.amax(extent[where(yearsM==x)]))
		min_extent.append(np.amin(extent[where(yearsM==x)]))
	return max_extent, min_extent

def get_min_max_extent_nrt(year):
	yearsL=[]
	extentL=[]
	rownum=0
	with open('../../DATA/ICE_CONC/NH_seaice_extent_nrt.csv', 'rb') as csvfile:
		datafile = csv.reader(csvfile)
		for row in datafile:
			if (rownum<2):
				header=row
				rownum+=1
			else:
				yearsL.append(row[0])
				extentL.append(row[3])
				rownum+=1

	yearsM=asarray(yearsL)
	yearsM = yearsM.astype(int)
	extent=asarray(extentL)
	extent=extent.astype(float)

	
	max_extent = np.amax(extent[where(yearsM==year)])
	min_extent = np.amin(extent[where(yearsM==year)])
	return max_extent, min_extent

max_extent, min_extent = get_min_max_extent()

max_extent2015, min_extent2015 = get_min_max_extent_nrt(2015)
max_extent2016, min_extent2016 = get_min_max_extent_nrt(2016)

min_extent.append(min_extent2015)
max_extent.append(max_extent2015)

min_extent.append('nan')
max_extent.append(max_extent2016)

years=np.arange(1980, 2017, 1)


fig = figure(figsize=(5,2.3))


ax1 = gca()
ax1.set_xlim(years[0], years[-1])

pl1 = plot(years, max_extent, linestyle='-',marker='x',markersize=3,linewidth=1, color='k')


ax2 = ax1.twinx()
pl2 = ax2.plot(years, min_extent, linestyle='-',marker='x',markersize=3,linewidth=1, color='r')



#ax1.yaxis.grid(True)
#ax1.xaxis.grid(True, which='major')
ax1.set_ylim(13, 17)
ax1.set_yticks(np.arange(13, 17+0.1, 1))
ax2.set_ylim(3, 10)
ax2.set_yticks(np.arange(3, 10+0.1, 1))

#ax1.set_xlabel( 'Years',fontsize=10)

ax1.set_ylabel( 'Maximum extent'+r' (10$^{6}$ km$^2$)')
ax2.set_ylabel( 'Minimum extent'+r' (10$^{6}$ km$^2$)',color='r', labelpad = 10, rotation=270)
ax2.spines['right'].set_color('r')
#ax1.yaxis.label.set_color('red')
ax2.tick_params(axis='y', colors='r')

plts_net = pl1+pl2
#labs = [l.get_label() for l in plts]

#Regions = ['Max Extent', 'Min Extent']

#leg = ax1.legend(plts_net, Regions, loc=3, ncol=2,columnspacing=0.1, handletextpad=0.0001, borderaxespad=0., frameon=False)


#leg = ax1.legend(plts, labs, loc=2)
#llines = leg.get_lines()
#setp(llines, linewidth=2.0)
#ltext  = leg.get_texts()
#setp(ltext, fontsize=10)
#leg.get_frame().set_alpha(0.5)

ax2.annotate('Data from NSIDC \nFigure by Alek Petty (NASA-GSFC)', xy=(0.02, 0.03), xycoords='axes fraction', fontsize=8, horizontalalignment='left', verticalalignment='bottom')
ax2.annotate('Arctic sea ice', xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12, horizontalalignment='left', verticalalignment='top')

subplots_adjust( right = 0.92, left = 0.1, top=0.96, bottom=0.1)

savefig('./Figures/max_min_Arctic_ice_extent.pdf', dpi=300)
savefig('./Figures/max_min_Arctic_ice_extent.jpg', dpi=300)
close(fig)









