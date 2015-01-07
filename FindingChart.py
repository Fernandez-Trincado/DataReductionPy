#!/usr/bin/python

# Centro de Investigaciones de Astronomia (CIDA)
#	Created by: Jose Fernandez
#	Date: 2012 September 11

#Importando las librerias de Python

import matplotlib # Para graficar desde Python
import aplpy # Modificar imagenes fits
import numpy # Usar operaciones matematicas y otros, ver documentacion en Python
import sys # Usa varibles de entrada por pantalla
from ds9 import * # Carga el ds9 desde Python, se debe instalar pyds9
import os # Libreria para usar comandos de UNIX

#Entrada por pantalla
#ID=raw_input("ID: ")
#ra=raw_input("Ingrese RA: ") #entrada por pantalla 
#raw_input: reconoce la variable de entrada como string, se puede cambiar con: float(nombre_variable), int(nombre_variable) ver documentacion de Python
#dec=raw_input("Ingrese DEC: ")

ID=sys.argv[1] #ID
ra=sys.argv[2]#raw_input("Ingrese RA: ")
dec=sys.argv[3]#raw_input("Ingrese DEC: ")

#Coordenadas centrales en grados decimales
#map(float,'13:08:32.7'.split(":"))
#dec_tmp=map(eval,dec.split(":"))
dec_tmp=map(float,dec.split(":"))

if dec_tmp[0] < 0.0: 

	ra1=map(float,ra.split(":"))
	ra_deg=(ra1[0]+((ra1[1]+(ra1[2]/60.0))/60.0))*15.0

	dec1=map(float,dec.split(":"))
	dec_deg=(dec1[0]-(((dec1[2]/60.0)+dec1[1])/60.0))
	print ra_deg, dec_deg

else:

	ra1=map(float,ra.split(":"))
	ra_deg=(ra1[0]+((ra1[1]+(ra1[2]/60.0))/60.0))*15.0

        dec1=map(float,dec.split(":"))
        dec_deg=(dec1[0]+(((dec1[2]/60.0)+dec1[1])/60.0))
        print ra_deg, dec_deg


#Descargando la imagen fits del servidor

ancho=4.0   #Tamano del campo
ancho=str(ancho)
largo=4.0
largo=str(largo)


d=ds9()
d.set('dsseso size '+ancho+' '+largo) #Tamano de la imagen a descargar 
#Otros servidores: dsssao, dssstsci, skyview, 2mass. Ver documentacion del ds9 (vD9)
d.set('dsseso coord '+ra+' '+dec) #Coordenadas centrales de la imagen 
d.set('dsseso survey DSS2-infrared') #Filtro: DSS2-blued, DSS2-red, DSS1, DSS2-infrared
d.set('file save salida.fits as fits') #se guarda la imagen .fits descargada del servidor
d.set('exit')



# Se genera el Finding Chart, documentacion de esta libreria en aplpy.FITSFigure Python. 

f=aplpy.FITSFigure("salida.fits") #slices=[222], figsize=(5,5))
f.show_colorscale()
f.show_grayscale(invert=True)
colors='navy' # Color del texto en la imagen 
f.add_grid() #Ingresa a la imagen una grid
f.tick_labels.set_font(size='xx-small')
f.axis_labels.set_font(size='x-small')
f.show_scalebar(1.0/120.0)
f.scalebar.set_label('30 arcsec')
f.show_arrows(ra_deg,dec_deg-0.0170,0,0.016,width=0.5,head_width=1.5,layer=False,zorder=None,color=colors)#inferior
f.show_arrows(ra_deg-0.025,dec_deg,0.0235,0,width=0.5,head_width=1.5,layer=False,zorder=None,color=colors)#derecho
f.show_circles(ra_deg,dec_deg,0.0010,layer=False,zorder=None,edgecolor=colors,linestyle='dashed')
f.show_arrows(ra_deg+0.025,dec_deg,-0.0235,0,width=0.5,head_width=1.5,layer=False,zorder=None,color=colors) #Izquierdo
f.show_arrows(ra_deg,dec_deg+0.0170,0,-0.016,width=0.5,head_width=1.5,layer=False,zorder=None,color=colors) #Superior
f.add_label(0.9,0.95,'('+ancho+'x'+largo+') arcmin',relative=True,color=colors)
f.add_label(0.2,0.88,'DSS2 I',relative=True,color=colors)
f.add_label(0.2,0.95,'CTIO-SMARTS 1.5 m telescope',relative=True,color=colors)
#f.add_label(0.2,0.92,'Created by: Jose Fernandez',relative=True,color=colors)
f.add_label(0.2,0.92,'Project: NGC5139',relative=True,color=colors)
f.add_label(0.2,0.82,ID,relative=True,color=colors)
f.save('findingChart'+ID+'.png')

os.system('rm salida.fits')

