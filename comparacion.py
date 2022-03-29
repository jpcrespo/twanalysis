import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import matplotlib.dates as mdates

from datetime import datetime, timedelta
import locale, os



data1 = np.load('resultados/LuchoXBolivia.npy', allow_pickle=True)
data2 = np.load('resultados/LuisFerCamachoV.npy', allow_pickle=True)
data3 = np.load('resultados/tutoquiroga.npy', allow_pickle=True)
data4 = np.load('resultados/JeanineAnez.npy', allow_pickle=True)
data5 = np.load('resultados/carlosdmesag.npy', allow_pickle=True)

datos_in = [data1[0][0],data2[0][0],data3[0][0],data4[0][0]]
datos_out = [data1[0][-1],data2[0][-1],data3[0][-1],data4[0][-1]]
   #un vector con todas las fechas 
inicio,fin =min(datos_in),max(datos_out)
date_all = [(inicio+timedelta(days=d)) for d in range((fin-inicio).days + 1)] 


fpath = os.path.join('app/MonoLisa.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

colores = [(48,48,48),             #color negro (fondo)
            (240,240,240),          #color letras 
            (113, 125, 126),          #color semi blanco (2do fondo)
            (30,144,255),                      #colores 1,2,3,4,5 grafica
            (35, 155, 86),
            (241, 196, 15),
            (231, 76, 60),
            (23, 32, 42)]
            
for i in range(len(colores)):    
   r, g, b = colores[i]    

   colores[i] = (r / 255., g / 255., b / 255.)   


fig = plt.figure(figsize=(25,8),constrained_layout=True)
ax = plt.axes()

#Color del fondo y fondo del gráfico.
#alternativa mas personalizable que plt.style.use() 

fig.patch.set_facecolor(colores[0])
ax.patch.set_facecolor(colores[2])

text_sets = {'color':  colores[1],'weight': 'normal','size': 25,'fontproperties':prop}
    
plt.title('\nComparación en la Frecuencia Tuits\n',fontsize=35,fontdict=text_sets)
plt.ylabel('\nNúmero de Tuits\n',fontdict=text_sets)
plt.xlabel('\nFecha\n',fontdict=text_sets)
plt.plot(date_all,np.ones(len(date_all)),linewidth=0.01,color=colores[0])

plt.plot(data1[0],data1[1],linewidth=0.5,color=colores[3],label='@LuchoXBolivia',linestyle='dotted')
plt.fill_between(data1[0],list(data1[1]),0,alpha=0.8,color=colores[3])

plt.plot(data2[0],data2[1],linewidth=0.5,color=colores[4],label='@LuisFerCamachoV',linestyle='dotted')
plt.fill_between(data2[0],list(data2[1]),0,alpha=0.9,color=colores[4])

plt.plot(data3[0],data3[1],linewidth=0.5,color=colores[5],label='@tutoquiroga',linestyle='dotted')
plt.fill_between(data3[0],list(data3[1]),0,alpha=0.5,color=colores[5])

plt.plot(data4[0],data4[1],linewidth=0.5,color=colores[6],label='@JeanineAnez',linestyle='dotted')
plt.fill_between(data4[0],list(data4[1]),0,alpha=0.9,color=colores[6])

plt.plot(data5[0],data5[1],linewidth=0.5,color=colores[7],label='@carlosdmesag',linestyle='dotted')
plt.fill_between(data5[0],list(data5[1]),0,alpha=0.9,color=colores[7])


locator = mdates.AutoDateLocator(minticks=20, maxticks=30)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

leg = plt.legend(loc='upper left',fontsize=18)

for legobj in leg.legendHandles:
   legobj.set_linewidth(6.0)

plt.yticks(fontsize=13,fontproperties=prop,color=colores[1])
plt.xticks(fontsize=18,rotation=0,fontproperties=prop,color=colores[1])

plt.annotate('Elecciones\n2019', xy=(datetime(2019, 10, 20),10),xytext=(datetime(2019, 11, 20),16),fontsize=23,fontproperties=prop,color=colores[1],arrowprops=dict(facecolor='white', shrink=0.10))
plt.annotate('Elecciones\n2020', xy=(datetime(2020, 10, 18),10),xytext=(datetime(2020, 11, 18),16),fontsize=23,fontproperties=prop,color=colores[1],arrowprops=dict(facecolor='white', shrink=0.10))

plt.xlim([inicio,fin])
plt.ylim([1,60])

plt.gca().yaxis.grid(linestyle='--',linewidth=0.8,dashes=(5,15))
plt.gca().xaxis.grid(linestyle='--',linewidth=1,dashes=(8,10))

# plt.axhline(np.mean(cnt),color=tableau20[2])  #horizontal line
plt.text(data1[0][-1],10,'  Tuits recopilados \n   por cuenta: 3200',fontsize=20,fontproperties=prop,color=colores[1])
plt.rc('axes',edgecolor='white')
plt.gca().spines["top"].set_visible(True)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(True)    
plt.gca().spines["left"].set_visible(True)
plt.savefig('resultados/comparacion.png')


os.remove('resultados/LuchoXBolivia.npy')
os.remove('resultados/LuisFerCamachoV.npy')
os.remove('resultados/tutoquiroga.npy')
os.remove('resultados/JeanineAnez.npy')
os.remove('resultados/carlosdmesag.npy')