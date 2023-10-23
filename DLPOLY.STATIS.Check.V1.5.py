#!/usr/bin/env python3

print('------------------------------------------------------------------')
print(' Analiza archivos STATIS de DL_POLY_4')


##########################################################
# Versiones
#
# V1.4 añade debug file, muestra avance en lectura
#      de datos
# V1.5 añade opciones para plotear en tiempo, step y
#      entrada de registro, util para comparar con
#      history
#
#
##########################################################


##################################################################################
# Entrada
iFile = input('\n    > Archivo (def=STATIS) : ')
if iFile == '':
	iFile = 'STATIS'

QuyDebug = input('    > Debug archivo (y/def=n) : ')

with open(iFile, 'r') as f:
	content = f.readlines()
	f.close()

DataInBlockIni = int(content[2].split()[2])
IniStep = int(content[2].split()[0])
IniTime = float(content[2].split()[1])
print('\n    Detecta inicialmente '+str(DataInBlockIni)+' entradas por bloque (puede variar) \n\
    Colectando data . . . ', end='\n')

Data = []
iLine = 2
while iLine < len(content)-1:
	tmpLine =[]
	tmpStep = int(content[iLine].split()[0])
	tmpTime = float(content[iLine].split()[1])
	
	if QuyDebug == 'y':
		print('   Leyendo entrada de step '+str(tmpStep)+' : ', end='')

	DataInBlock = int(content[iLine].split()[2])
	if DataInBlock != DataInBlockIni:
		print('        Cambia a '+str(DataInBlock)+' entradas por bloque en step '+str(tmpStep))
		DataInBlockIni = DataInBlock

	tmpDataInclude = []
	tmpNumDataInclude = 0.

	while tmpNumDataInclude < float(DataInBlock):
		iLine+=1
		ThisLine = content[iLine].split()
		for i in ThisLine:
			tmpDataInclude.append(float(i))
			tmpNumDataInclude+=1.

	Data.append([tmpStep, tmpTime, tmpDataInclude])

	if QuyDebug == 'y':
		print(' Ok')
	iLine+=1
		
FinalStep = tmpStep
FinalTime = tmpTime
print('    Listo!\n')
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
	QuPlotX = input("    > Plot by time (def=1), step (2) or by entry (3) : ") or "1"
	if QuPlotX == "1":
		plotx = []
		for iLine in DataPurga:
			plotx.append(iLine[1])
		x_label = "time (ps)"

	elif QuPlotX == "2":
		plotx = []
		for iLine in DataPurga:
			plotx.append(iLine[0])
		x_label = "step #"

	elif QuPlotX == "3":
		plotx = range(len(DataUsoX))
		x_label = "registry entry #"

	print('\n    Ploteando . . . ', end='. . . hecho!')
	import matplotlib.pyplot as plt
	plt.plot(plotx, DataUsoY, '.-', linewidth=0.5)
	plt.xlabel(x_label)

	Titulos = ['Energía', 'Temperatura', 'E configuracional', 'E corto rango', 'E electrostatica',\
		'E enlace', '', '', '', 'Entalpia', \
		'', '', '', '', '',\
		'', '', '', 'Volumen','',\
		'', '', '', '', '',\
		'', 'Presion']
	plt.title(Titulos[index])
	plt.show()
print('    Bye!')









