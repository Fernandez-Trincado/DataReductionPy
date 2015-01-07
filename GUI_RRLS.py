#!/usr/bin/python


# Centro de Investigaciones de Astronomia (CIDA)
#       Created by: Jose Gregorio Fernandez Trincado
#       Date: 2013 February 25
#       Last modification: 2013 June 06
#Importando las librerias de Python

import aplpy
import sys
import pylab as plt
import scipy as sc
import numpy as np


data=sc.genfromtxt('Inf_RRLS.dat',dtype=str) #Leyendo los datos de entrada
locate='/home/jfernandez/Escritorio/Proyectos_Ocen_2011_2012_2013/GUI_RRLS/RRLS_DATA_FINAL/'

	
for i in np.arange(len(data)):

	if (data[i,0] == 'NODATA'):	

		img_list_FC=locate+'FindingChartsRRLS/'+'V'+str(data[i,1])+'_DSS2-red.fits'
		img_list_CL=locate+'Curvas_con_Plantillas/'+'RRLS'+str(data[i,1])+'.new'
		img_list_CL_p=locate+'Curvas_con_Plantillas/'+'RRLS'+str(data[i,1])+'.plantilla'
		int_CL=sc.genfromtxt(str(img_list_CL))
		int_CL_p=sc.genfromtxt(str(img_list_CL_p))

	else:

		img_list_FC=locate+'FindingChartsRRLS/'+'V'+str(data[i,1])+'_DSS2-red.fits'
		img_list_Esp=locate+'EspectrosRRLS/'+str(data[i,0])
		img_list_CL=locate+'Curvas_con_Plantillas/'+'RRLS'+str(data[i,1])+'.new'
		img_list_CL_p=locate+'Curvas_con_Plantillas/'+'RRLS'+str(data[i,1])+'.plantilla'
		int_Esp=sc.genfromtxt(str(img_list_Esp))
		int_CL=sc.genfromtxt(str(img_list_CL))
		int_CL_p=sc.genfromtxt(str(img_list_CL_p))

	
	fi=plt.figure(1,figsize=(14,8))

#a.show_markers(188.15994,32.593043,layer='marker_set_1',edgecolor='red',facecolor='none',marker='o',s=150,alpha=1)	
#Carta de identificacion

	f=aplpy.FITSFigure(img_list_FC,figure=fi,subplot=[0.1,0.08,0.32,0.45]) 
	f.show_grayscale(invert=True)
	f.add_grid()
	f.tick_labels.set_font(size='small')
	f.axis_labels.set_font(size='medium')
	f.show_circles(float(data[i,2]),float(data[i,3]),0.0015,layer=False,zorder=None,edgecolor='red')#,linestyle='dashed')
	f.recenter(float(data[i,2]),float(data[i,3]),width=0.02,height=0.02)	
	f.set_tick_labels_xformat('ddd.ddd')
	f.set_tick_labels_yformat('ddd.ddd')
	f.set_axis_labels(xlabel=r'$\alpha$ (degree)',ylabel=r'$\delta$ (degree)')

#Datos
	type_star=('c','ab',r'$\delta$ Scuti')
	
	ax1=fi.add_subplot(221)
	ax1.text(0.1,1.8,'Fundacion Centro de Investigaciones de Astronomia (CIDA)')
	ax1.text(0.1,1.6,'ID: '+data[i,1],color='blue')
	ax1.text(0.8,1.6,'Type: '+type_star[int(data[i,13])-1])
	ax1.text(1.4,1.6,'N$_{obs}:$ '+data[i,4])
	ax1.text(0.1,1.4,r'$\alpha_{J2000}$ : '+data[i,2])
	ax1.text(0.8,1.4,r'$\delta_{J2000}$ : '+data[i,3])
	ax1.text(0.1,1.2,'Periodo: '+data[i,5]+' (day)')
	ax1.text(0.1,1.0,'Amplitude: '+data[i,6]+' (mag)')
	ax1.text(0.1,0.8,'Mag: '+data[i,7]+' $\pm$ '+data[i,8])
	ax1.text(0.1,0.6,'Filter: '+data[i,12])
	ax1.text(0.1,0.4,'E(B-V): '+data[i,9])
	ax1.text(0.8,0.4,'A$_V$: '+str((3.240)*float(data[i,9])))
	ax1.text(1.4,0.4,'A$_I$: '+str((0.48)*(3.240)*float(data[i,9])))
	ax1.text(0.1,0.2,'Distance: ('+data[i,10]+' $\pm$ '+data[i,11]+') kpc')
	ax1.tick_params(bottom='off',left='off',right='off',top='off',labelbottom='off',labeltop='off',labelright='off',labelleft='off')
	ax1.set_xlim(0,2)
	ax1.set_ylim(0,2)
	
##Curva de Luz
	
	ax2=fi.add_subplot(222)
	ax2.errorbar(int_CL[:,0],int_CL[:,1],yerr=int_CL[:,2],fmt='o',color='black')
	ax2.plot(int_CL_p[:,0],int_CL_p[:,1],color='gray',linestyle='--')
	ax2.plot(int_CL_p[:,0]+1.,int_CL_p[:,1],color='gray',linestyle='--')
	ax2.set_xlim(0.,2.)
	ax2.set_ylim(np.max(int_CL[:,1])+np.max(int_CL[:,2])*3,np.min(int_CL[:,1])-np.max(int_CL[:,2])*3)
	ax2.set_xlabel(r'$\phi$')
	ax2.set_ylabel(r'$Mag$')
	
#
	if (data[i,0] == 'NODATA'):


		ax3=fi.add_subplot(224)
		ax3.plot(1.,1.)
		ax3.text(1.,1.,'NO DATA')
		ax3.tick_params(bottom='off',left='off',right='off',top='off',labelbottom='off',labeltop='off',labelright='off',labelleft='off')	

#Espectro
	
	else: 

		ax3=fi.add_subplot(224)
		ax3.plot(int_Esp[:,0],int_Esp[:,1],color='gray')
		ax3.set_ylabel('Arbitrary flow')
		ax3.set_xlabel(r'$\lambda  (\AA{})$')
		ax3.set_xlim(3750.,5250.)
	
#Lineas espectrales
		ax3.axvline(x=4861.1,color='red',label=r'H$\beta$') #Hbeta
		ax3.axvline(x=4341.0,color='green',label=r'H$\gamma$') #Hgamma
		ax3.axvline(x=4102.0,color='black',label=r'H$\delta$') #Hdelta
		ax3.axvline(x=3968.5,color='blue',label='Ca II H-line') # H-line
		ax3.axvline(x=3933.7,color='orange',label='Ca II K-line') # K-line


		
	
	plt.legend(loc=4,prop={'size':10})
	plt.tight_layout()
	plt.savefig(str(data[i,0])+str(data[i,1])+'.png')
#	plt.show()
	plt.close()

#END
