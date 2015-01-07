#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 June 25
# Program: This program generate the Master Bias
# 1 m Reflector telescope, National Astronomical Observatory of Venezuela
# Mode f/5, 21 arcmin x 21 arcmin
# Project: Omega Centauri, Tidal Tails. 
# The program Astrometry_V1.py defined was developed by J. G. Fernandez Trincado at the Centro de Investigaciones de Astronomia "Francisco J. Duarte".
# If you have any problems, please contact J. G. Fernandez Trincado, jfernandez@cida.ve / jfernandezt87@gmail.com

import numpy as np
import scipy as sc
import pyfits
import sys, os
from pyraf import iraf

#run, program. 
#Example: 
#   Next program: ./Run_2-Master_Bias.py Feb.22.Feb.23.2013.hlv/ 
#                 >>> Feb.22.Feb.23.2013.hlv/*.fit

location='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'

if len(sys.argv[:]) < 2.:

  print '***************************************************'
  print 'Warning: ./Run_2-Master_Bias.py XXX.xx.XXX.xx.XXXX.hlv'
  print '***************************************************'
  

else:

	os.system('\ls '+sys.argv[1]+'/Bias/*.fit > temp_bias.dat')
	data_bias=sc.genfromtxt('temp_bias.dat',dtype=str)


#Checkin the Bias

	iraf.noao()
	iraf.images()
	iraf.imutil()
	
	for i in np.arange(len(data_bias)):

		statdata=iraf.imstat(data_bias[i],fields='mean,min',Stdout=1)
		statdata_min=''.join(statdata).split()[4]
		statdata_mean=''.join(statdata).split()[3]

	
		if float(statdata_mean) < 0. or float(statdata_mean) > 3000.:
				
			print 'Remove '+data_bias[i]
			os.system('rm '+location+data_bias[i])
				
		else: 

			print data_bias[i]+'  -------> (Mean): '+statdata_mean


	os.system('rm temp_bias.dat')
	os.system('\ls '+sys.argv[1]+'/Bias/*.fit > temp_bias.dat')


#Combine images MEDIAN
#TASK IRAF: images.immatch.imcombine


	im_out='Master_Bias.fit'
	
	iraf.images.immatch()
	iraf.images.immatch.imcombine.output=im_out
	iraf.images.immatch.imcombine.headers=''
	iraf.images.immatch.imcombine.bpmasks=''
	iraf.images.immatch.imcombine.rejmasks=''
	iraf.images.immatch.imcombine.nrejmasks=''
	iraf.images.immatch.imcombine.expmasks=''
	iraf.images.immatch.imcombine.sigmas=''
	iraf.images.immatch.imcombine.logfile='STDOUT'
	iraf.images.immatch.imcombine.combine='average'
	iraf.images.immatch.imcombine.reject='avsigclip'
	iraf.images.immatch.imcombine.project='no'
	iraf.images.immatch.imcombine.outtype='real'
	iraf.images.immatch.imcombine.outlimits=''
	iraf.images.immatch.imcombine.offsets='none'
	iraf.images.immatch.imcombine.masktype='none'
	iraf.images.immatch.imcombine.maskvalue=0.
	iraf.images.immatch.imcombine.blank=1.0
	iraf.images.immatch.imcombine.scale='mode'
	iraf.images.immatch.imcombine.zero='none'
	iraf.images.immatch.imcombine.weight='mode'
	iraf.images.immatch.imcombine.statsec=''
	iraf.images.immatch.imcombine.expname=''
	iraf.images.immatch.imcombine.lthreshold='INDEF'
	iraf.images.immatch.imcombine.hthreshold='INDEF'
	iraf.images.immatch.imcombine.nlow=1.
	iraf.images.immatch.imcombine.nhigh=1.
	iraf.images.immatch.imcombine.nkeep=1.
	iraf.images.immatch.imcombine.mclip='yes'
	iraf.images.immatch.imcombine.lsigma=3.
	iraf.images.immatch.imcombine.hsigma=3.
	iraf.images.immatch.imcombine.rdnoise=7.
	iraf.images.immatch.imcombine.gain=1.68
	iraf.images.immatch.imcombine.snoise=0.
	iraf.images.immatch.imcombine.sigscale=0.1
	iraf.images.immatch.imcombine.pclip=-0.5
	iraf.images.immatch.imcombine.grow=0.
	iraf.images.immatch.imcombine(input='@temp_bias.dat')

	os.system('mv '+im_out+' '+sys.argv[1])
	os.system('rm temp_bias.dat')

#END
