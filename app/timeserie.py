''' En este script se proponen algunos análisis:
1. Temporales
   - Frecuencia de tuits por día (histograma)  #tuits vs hora
   - Frecuencia de tuits temporal (histórico)  #tuits vs fecha
2. Procesamiento de texto (tokenizado)
   - Frecuencia de palabras (obtener top10 palabras más usadas)
   - Longitud promedio tuits.
   - Análisis de Sentimientos.
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import locale, os



def timeserie(target):
   locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
   # Leer un csv
   dataset = pd.read_csv('resultados/'+target+'/recopile_tw.csv')
   #recupera los valores de interes (fechas)
   x_time = pd.to_datetime(dataset.iloc[:,0].values)

   x_time = [x.strftime('%Y/%m/%d') for x in x_time]
   date,cnt = np.unique(x_time,return_counts=True)  

   #date con las fechas de los tuits, cnt numero de tuits en esa fecha
   date = [datetime.strptime(i,'%Y/%m/%d') for i in date]

   #un vector con todas las fechas 
   inicio,fin = date[0], date[-1]
   date_all = [(inicio+timedelta(days=d)) for d in range((fin-inicio).days + 1)] 

   fpath = os.path.join('app/MonoLisa.ttf')
   prop = fm.FontProperties(fname=fpath)
   fname = os.path.split(fpath)[1]

   colores = [(48,48,48),               #0 fondo
               (240,240,240),            #1 letras
               (105,105,105),            #2 fondo 2 
               (32,178,170),            #3 color bars
               (50,205,50),              #4 color linea
               (105, 105, 105)]    
   
   # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
   for i in range(len(colores)):    
      r, g, b = colores[i]    
      colores[i] = (r / 255., g / 255., b / 255.)   

   fig = plt.figure(figsize=(21,7),constrained_layout=True)
   ax = plt.axes()

   #Color del fondo y fondo del gráfico.
   #alternativa mas personalizable que plt.style.use() 
   fig.patch.set_facecolor(colores[0])
   ax.patch.set_facecolor(colores[2])

   plt.title('\nFrecuencia Tuits - Serie temporal\n@'+target+'\n',fontsize=25,fontproperties=prop,color=colores[1])
   plt.ylabel('\nNúmero de Tuits\n',fontsize=20,fontproperties=prop,color=colores[1])
   plt.xlabel('\nFecha\n',fontsize=20,fontproperties=prop,color=colores[1])

   plt.plot(date_all,np.zeros(len(date_all)),linewidth=0.01,color=colores[2])
   plt.plot(date,cnt,label='@'+target,color=colores[3])
   plt.fill_between(date,cnt,0,alpha=0.2,color=colores[3])

   locator = mdates.AutoDateLocator(minticks=30,maxticks=1)
   
   formatter = mdates.ConciseDateFormatter(locator)
   ax.xaxis.set_major_locator(locator)
   ax.xaxis.set_major_formatter(formatter)

   leg = plt.legend(loc='upper left',fontsize=15)

   for legobj in leg.legendHandles:
      legobj.set_linewidth(1.8)

   plt.yticks(np.linspace(0,max(cnt),5,dtype = int, endpoint=True),fontsize=13,fontproperties=prop,color=colores[1])
   plt.xticks(fontsize=12,rotation=0,fontproperties=prop,color=colores[1])

   plt.annotate('Elecciones\n2019', xy=(datetime(2019, 10, 13),np.max(cnt)/2),xytext=(datetime(2019, 11, 20),np.max(cnt)/1.5),fontsize=15,fontproperties=prop,color=colores[1],
               arrowprops=dict(facecolor='red', shrink=0.05))

   plt.annotate('Elecciones\n2020', xy=(datetime(2020, 10, 11),np.max(cnt)/2),xytext=(datetime(2020, 11, 18),np.max(cnt)/1.5),fontsize=15,fontproperties=prop,color=colores[1],
               arrowprops=dict(facecolor='red', shrink=0.05))
               
   plt.xlim([inicio,fin])
   plt.ylim([1,max(cnt)+1])

   plt.gca().yaxis.grid(linestyle='--',linewidth=0.45,dashes=(5,15))
   plt.gca().xaxis.grid(linestyle='--',linewidth=0.6,dashes=(8,10))

   plt.axhline(np.mean(cnt),color=colores[4])  #horizontal line
   plt.text(date[-1],np.mean(cnt)+1,'  Promedio:\n  '+str(round(np.mean(cnt)))+' tuits/día  ',fontsize=13,fontproperties=prop,color=colores[1])
   plt.rc('axes',edgecolor='white')
   plt.gca().spines["top"].set_visible(True)    
   plt.gca().spines["bottom"].set_visible(True)    
   plt.gca().spines["right"].set_visible(True)    
   plt.gca().spines["left"].set_visible(True)
   plt.savefig('resultados/'+target+'/timeserie.png')
#guardando datos para comparaciones
   np.save('resultados/'+target+'/datecnt.npy',(date,cnt))

