#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 June 26
# Program: This program correct the imagen .fit (Science) by Syntethic Flat
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
#   Next program: ./Run_4-Synthetic_Flat.py Feb.22.Feb.23.2013.hlv 
#                 >>> Feb.22.Feb.23.2013.hlv/*.fit

location='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'

if len(sys.argv[:]) < 2.:

	print '***************************************************'
	print 'Warning: ./Run_4-Synthetic_Flat.py XXX.xx.XXX.xx.XXXX.hlv'
	print '***************************************************'


else: 

#Combine images MEDIAN
#TASK IRAF: images.immatch.imcombine
#Function to combine images for generates Master Flat

	def Master_combina(inter_img,filt):

		iraf.images.immatch()
		iraf.images.immatch.imcombine.output=filt
		iraf.images.immatch.imcombine.headers=''
		iraf.images.immatch.imcombine.bpmasks=''
		iraf.images.immatch.imcombine.rejmasks=''
		iraf.images.immatch.imcombine.nrejmasks=''
		iraf.images.immatch.imcombine.expmasks=''
		iraf.images.immatch.imcombine.sigmas=''
		iraf.images.immatch.imcombine.logfile='STDOUT'
		iraf.images.immatch.imcombine.combine='median'
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
		iraf.images.immatch.imcombine(inter_img)

#END function, IRAF: imcombine

	os.system('ls '+sys.argv[1]+'/Science/*_BR.fit >list_temp_Science.txt ')
	data=sc.genfromtxt('list_temp_Science.txt',dtype=str)

	def list_s(x1,y1):

		lf='Initial_list_Syntethic_flat_'+y1
		os.system('ls '+x1+' >> '+lf)
		return lf


	for i in np.arange(len(data)): 

		data_head=pyfits.open(data[i])

		delta=data_head[0].header['DECJ2_D']
		filter_s=data_head[0].header['FILTER']
		filter_s=float(map(str,filter_s)[0])
		time_exp=data_head[0].header['EXPTIME']
		time_exp=int(time_exp)

#Selecting images of my project

#		if float(delta) < -39. and filter_s == 2. and time_exp == 60:		
		if filter_s == 2. and time_exp == 60:
				
			list_s(data[i],'V'+str(time_exp)) #Generating list

		elif filter_s == 4. and time_exp == 60:

			list_s(data[i],'I'+str(time_exp)) #Generating list


		elif filter_s == 2. and time_exp == 90:

			list_s(data[i],'V'+str(time_exp)) #Generating list


		elif filter_s == 4. and time_exp == 90:

			list_s(data[i],'I'+str(time_exp)) #Generating list

		else: 

			os.system('bzip2 '+data[i])			


	os.system('ls Initial*list* >list_temp_flat_list.dat')
	proc=sc.genfromtxt('list_temp_flat_list.dat',dtype=str)

	for j in np.arange(len(proc)):


		Master_combina('@'+proc[j],'Master_'+proc[j]+'.fit')		
		os.system('mv  Master_'+proc[j]+'.fit '+sys.argv[1]+'/')

	os.system('mv Initial*list* '+sys.argv[1]+'/')
	os.system('rm list_temp_Science.txt list_temp_flat_list.dat')


#END
