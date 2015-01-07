#!/usr/bin/python

# Created by: Jose G. Fernandez Trincado
# Date: 2013 June 25
# Program: This program organizes all the images by each night
# 1 m Reflector telescope, National Astronomical Observatory of Venezuela
# Mode f/5, 21 arcmin x 21 arcmin
# Project: Omega Centauri, Tidal Tails. 

import numpy as np
import scipy as sc
import pyfits
import sys, os 

#run, program. 
#Example: 
#		Next program: ./Organizing.py Feb.22.Feb.23.2013.hlv/ 
#									>>> Feb.22.Feb.23.2013.hlv/*.fit


if len(sys.argv[:]) < 2.:

	print '***************************************************'
	print 'Warning: ./Organizing.py Directory_with_images_.fits'
	print '***************************************************'


else: 

	os.system('mkdir Science Bias Flats Darks')
	os.system('mv Science Bias Flats Darks '+sys.argv[1])
	os.system('ls '+sys.argv[1]+'/*.fit >list_temp.txt')
	dir_img='/home/jfernandez/Escritorio/Tesis_2013-2014_CIDA_ULA/Data_Tesis_2013_2014_CIDA-ULA/Reflector/'+sys.argv[1]+'/'

	data_img=sc.genfromtxt('list_temp.txt',dtype=str)

	for i in np.arange(len(data_img)):

		data_head=pyfits.open(data_img[i])
		type_img_cal=map(str,data_head[0].header['object'].split('_'))[0]

	
		if data_head[0].header['exptime'] < 1:

			print data_img[i]+' ----> Bias' 
			os.system('mv '+data_img[i]+' '+dir_img+'/Bias')

		elif type_img_cal == 'dark' or type_img_cal == 'DARK' or type_img_cal == 'Dark':

			print data_img[i]+' ----> Darks'
			os.system('mv '+data_img[i]+' '+dir_img+'Darks')

		elif type_img_cal == 'FLAT' or type_img_cal == 'flat' or type_img_cal == 'fltas':

			print data_img[i]+' ----> Flats'
			os.system('mv '+data_img[i]+' '+dir_img+'Flats')

		else: 

			print data_img[i]+' ----> Science'
			os.system('mv '+data_img[i]+' '+dir_img+'Science')


	os.system('rm list_temp.txt')


#END
