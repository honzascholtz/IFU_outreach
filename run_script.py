import numpy as np
import viz as viz

#Viz = viz.Visualize('/Users/jansen/My Drive/Astro/COS30_IFS/Saves/R2700/COS30_R2700_general_fits_maps.fits',\
#                     ['OIII','OII','OII'], indc=[1,1,0], z=6.85072093)
#Viz.showme(xlims=[3.1,3.5])

Viz = viz.Viz_outreach('/Users/jansen/My Drive/Astro/COS30_IFS/Saves/R2700/COS30_R2700_Halpha_OIII_fits_maps.fits',\
                     ['OIII', 'Narrow_vel'], indc=[1,0],vlim2 = [-100,200], z=6.85072093)
Viz.showme(xlims=[3.8,3.95])