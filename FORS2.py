#!/usr/bin/python

import os 
import sys
import pyfits 
import pylab as plt 
import aplpy
import scipy as sc
import numpy as np

if len(sys.argv[:]) < 3: 

	print 'Warnig: '
	print './FORS2.py Image_2D Images_1D'


else:

	img_list=str(sys.argv[1]) #Image 2D
	img_list1=str(sys.argv[2]) #Image 1D
	
	
	img_list2=pyfits.open(img_list1)
	N_slit=int(img_list2[0].header['N_SLITS'])

	for j in np.arange(N_slit):

		slit=j#raw_input('Ingrese el numero de slit: ')

		lambda1=np.array([float(img_list2[0].header['CRVAL1'])])
		
		for i in np.arange(float(img_list2[0].header['NAXIS1'])-1):
		
		    l1=lambda1[i]+float(img_list2[0].header['CD1_1'])
		    lambda1=np.append(lambda1,l1)
		
		
		#Plot
		
		fi=plt.figure(1,figsize=(14,8))
		
		f=aplpy.FITSFigure(img_list,figure=fi,subplot=[0.125,0.52,0.775,0.40])
		f.show_grayscale(invert=False,stretch='linear')
		f.set_axis_labels(xlabel=r'$\lambda (\AA)$', ylabel='Pixel')	
		
		ax1=fi.add_subplot(223)
		ax1.tick_params(bottom='off',left='off',right='off',top='off',labelbottom='off',labeltop='off',labelright='off',labelleft='off')
		ax1.set_xlim(0,2)
		ax1.set_ylim(0,2)
		ax1.text(0.65,1.8,'Universidad de Valparaiso')
		ax1.text(0.1,1.6,'')
		ax1.text(0.1,1.4,'Proyect: '+str(img_list2[0].header['OBJECT']))
		ax1.text(0.1,1.2,'Telescope: '+str(img_list2[0].header['TELESCOP']))
		ax1.text(0.1,1.0,'Instrument: '+str(img_list2[0].header['INSTRUME']))
		ax1.text(0.1,0.8,'Filter: '+str(img_list2[0].header['HIERARCH ESO INS OPTI7 NAME']))
		ax1.text(0.1,0.6,'Grism: '+str(img_list2[0].header['HIERARCH ESO INS OPTI6 NAME']))
		ax1.text(0.1,0.4,'Information of the slit #'+str(int(slit)+1),color='blue')
		ax1.text(1.2,1.4,r'$\alpha$: '+str(img_list2[0].header['RA '])+' degree')
		ax1.text(1.2,1.2,r'$\delta$: '+str(img_list2[0].header['DEC'])+' degree')
		ax1.text(1.2,1.0,'Exp time: '+str(img_list2[0].header['HIERARCH ESO INS SHUT EXPTIME'])+' s')
		
		
		ax2=fi.add_subplot(224)
		ax2.plot(lambda1,img_list2[0].data[float(slit)],color='blue')
		ax2.set_xlabel(r'$\lambda(\AA)$')
		ax2.set_ylabel('Arbitrary Flux')
		ax2.set_xlim((np.min(lambda1),np.max(lambda1)))
		
		plt.show()
