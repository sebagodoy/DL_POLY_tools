#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Plotea archivo ZDNDAT')
print(' generado por \'zden i\'')
print('------------------------------------------------------------------')


##################################################################################
# Entrada
iFile = input('\n    > Archivo (def=ZDNDAT) : ')
if iFile == '':
	iFile = 'ZDNDAT'

with open(iFile, 'r') as f:
	content = f.readlines()
	f.close()

print('    Archivo hallado, recoge data', end=' . . .')

zDat=[]; denDat=[]
iLine = 3
while iLine < len(content)-1:
	ThisLine = content[iLine].split()
	zDat.append(float(ThisLine[0]))
	denDat.append(float(ThisLine[1]))
	iLine+=1
print('Listo!')

zIni = zDat[0]; zFin = zDat[len(zDat)-1]
print('    Desde ')


##################################################################################
# Tools
import numpy as np



##################################################################################
# Plot

print('------------------------------------------------------------------')

print('\n    Ploteando . . . ', end='. . . hecho!\n')
import matplotlib.pyplot as plt

plt.plot(zDat, denDat, linewidth=0.5)
plt.show()



print('    Bye!\n')









