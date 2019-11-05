#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Analiza archivos STATIS de DL_POLY_4')


##################################################################################
# Entrada
iFile = input('\n    > Archivo (def=STATIS) : ')
if iFile == '':
	iFile = 'STATIS'

with open(iFile, 'r') as f:
	content = f.readlines()
	f.close()

DataInBlock = int(content[2].split()[2])
IniStep = int(content[2].split()[0])
IniTime = float(content[2].split()[1])
print('\n    Detecta '+str(DataInBlock)+' entradas por bloque \n    Colectando data . . . ', end='. . .')

Data = []
iLine = 2
while iLine < len(content)-1:
	tmpLine =[]

	tmpStep = int(content[iLine].split()[0])
	tmpTime = float(content[iLine].split()[1])

	tmpDataInclude = []
	tmpNumDataInclude = 0.

	while tmpNumDataInclude < float(DataInBlock):
		iLine+=1
		ThisLine = content[iLine].split()
		for i in ThisLine:
			tmpDataInclude.append(float(i))
			tmpNumDataInclude+=1.

	Data.append([tmpStep, tmpTime, tmpDataInclude])

	iLine+=1
		
FinalStep = tmpStep
FinalTime = tmpTime
print('Listo!')
print('    Recogió '+str(len(Data))+' bloques')
print('          inicia en step= '+str(IniStep)+' a tiempo='+str(IniTime)+' ps')
print('         termina en step= '+str(FinalStep)+' a tiempo='+str(FinalTime)+' ps')

##################################################################################
# Límites
print('------------------------------------------------------------------')
QueryLimit = input('\n    > Limita rango (~y/def=n)                : ')
if QueryLimit == '':
	QueryLimit = False
else:
#	QueryLimit =     input('        en paso (def=1) o tiempo(2)? : ')
#	if QueryLimit == '':
	QueryLimit = 1

#if not (QueryLimit == False or int(QueryLimit) == 1 or int(QueryLimit) == 2):
#	print('    ah?, adios'); exit()

if not QueryLimit == False:
	# min
	LimitMin = input('                          Inicio     :')
	if LimitMin == '' or float(LimitMin) < IniStep:
		LimitMin = IniStep
		print('        Usa mínimo '+str(IniStep))
	else:
		LimitMin = float(LimitMin)
	
	LimitMax = input('                          Fin        :')
	if LimitMax == '' or float(LimitMax) > FinalStep:
		LimitMax = FinalStep
		print('        Usa máximo '+str(FinalStep))
	elif float(LimitMax) < LimitMin+2:
		LimitMax = LimitMin+2
		print('        Usa máximo '+str(LimitMax))
	else:
		LimitMax = float(LimitMax)


ExcludeList = []
for Thisi in Data:
	if QueryLimit == False: # No test
		ExcludeList.append(True)

	else: # 1->0 test Paso; 2->1 test Time
		#print(Thisi[int(QueryLimit)-1], end=' - '); print(LimitMin, end=' - '); print(LimitMax)
		if LimitMin <= Thisi[int(QueryLimit)-1] and Thisi[int(QueryLimit)-1] <= LimitMax:
			ExcludeList.append(True)
		else:
			ExcludeList.append(False)			

##################################################################################
# Purga data

DataPurga = []
for i in range(len(ExcludeList)):
	if ExcludeList[i] == True:
		DataPurga.append(Data[i])
print('        Se consideran '+str(len(DataPurga))+' datos')

##################################################################################
# Index de data a tomar
indexList = input('    > Mostrar lista de indices? (y/def=n)    : ')
if indexList == 'y':
	print('        Index data:')
	print('        (0)E tot    (1) T            (2) E conf (3)E short range (4) E electrst')
	print('        (5)E bond   (6) E val°/3 bdy (7)        (8)              (9) Enthalpy')
	print('        (10)        (11)             (12)       (13)             (14)')
	print('        (15)        (16)             (17)       (18) Volumen     (19)')
	print('        (20)        (21)             (22)       (23)             (24)')
	print('        (25)PMF vir (26) Presion')


index = input('    > Index de parametro (def=0, E total)    : ')
if index == '':
	index = int(0)
elif  int(index) > DataInBlock:
	print('    Usa def= Energy');  index = 0
else:
	index=int(index)


##################################################################################
# Estadística
DataUsoX=[]; DataUsoY=[]
for iLine in DataPurga:
	DataUsoX.append(iLine[0])
	DataUsoY.append(iLine[2][index])

########
# Tools
import numpy as np

def FixNum(iNum, **kwargs):
	tmpNDec=str(kwargs.get('dec', 4))
	tmpMode=str(kwargs.get('mode', 'f'))
	tmpFormat = '{:.'+tmpNDec+tmpMode+'}'
	return tmpFormat.format(iNum)

def PromVect(inVect):
	sumCum = 0.
	for iNum in inVect:
		sumCum += iNum
	return sumCum/len(inVect)

def DesvEst(inVect, **kwargs):
	sumCum = 0.
	tmpProm = PromVect(inVect)
	for iNum in inVect:
		sumCum +=(iNum-tmpProm)**2

	Counter=len(inVect)
	mode = kwargs.get('mode', 'poblacional')
	if mode == 'muestral':
		Counter-=1
		
	return np.sqrt(sumCum/Counter)

def stdErrMedia(inVect):
	#Aproxima mediante desv est muestral
	return	DesvEst(inVect, mode='muestral')/np.sqrt(len(inVect))

print('------------------------------------------------------------------')
# Promedio
Prom = PromVect(DataUsoY)
if np.sqrt(Prom**2) < 9.9e5:
	print('    > Promedio            = '+str(FixNum(Prom, dec=6)))
else:
	print('    > Promedio            = '+str(FixNum(Prom, dec=6, mode='E')))


#Desv est muestral
print('    > Desv Est (pobl)     = '+str(FixNum(np.std(DataUsoY), dec=4)))
print('               (muestr)   = '+str(FixNum(DesvEst(DataUsoY, mode='muestral'), dec=4)))

#Error estandar de la media
print('    > Err std de la media = '+str(FixNum(stdErrMedia(DataUsoY), dec=6)))



##################################################################################
# Plot
print('------------------------------------------------------------------')
QueryPlot = input('    > Plot? (def=y/n~*) : ')

if QueryPlot == ''or QueryPlot == 'y':
	print('\n    Ploteando . . . ', end='. . . hecho!')
	import matplotlib.pyplot as plt
	plt.plot(DataUsoX, DataUsoY, linewidth=0.5)

	Titulos = ['Energía', 'Temperatura', 'E configuracional', 'E corto rango', 'E electrostatica',\
		'E enlace', '', '', '', 'Entalpia', \
		'', '', '', '', '',\
		'', '', '', 'Volumen','',\
		'', '', '', '', '',\
		'', 'Presion']
	plt.title(Titulos[index])
	plt.show()
print('    Bye!')









