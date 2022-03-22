''' En este script se proponen algunos análisis:

1. Temporales
   - Frecuencia de tuits por día (histograma)  #tuits vs hora
   - Frecuencia de tuits temporal (histórico)  #tuits vs fecha
2. Procesamiento de texto (tokenizado)
   - Frecuencia de palabras (obtener top10 palabras más usadas)
   - Longitud promedio tuits.
   - Análisis de Sentimientos.

'''

from turtle import color
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import matplotlib.dates as mdates

from datetime import datetime, timedelta
import locale, os

def frec_tw(target):

   locale.setlocale(locale.LC_TIME,'esp')
   # Leer un csv
   dataset = pd.read_csv('resultados/'+target+'.csv')
   #recupera los valores de interes (fechas)
   x_time = pd.to_datetime(dataset.iloc[:,1].values)

   x_time = [x.strftime('%Y/%m/%d') for x in x_time]
   date,cnt = np.unique(x_time,return_counts=True)  


   #date con las fechas de los tuits, cnt numero de tuits en esa fecha
   date = [datetime.strptime(i,'%Y/%m/%d') for i in date]

   #un vector con todas las fechas 
   inicio,fin = date[0], date[-1]
   date_all = [(date[0]+timedelta(days=d)) for d in range((date[-1]-date[0]).days + 1)] 


   fpath = os.path.join(r'MonoLisa.ttf')
   prop = fm.FontProperties(fname=fpath)
   fname = os.path.split(fpath)[1]

   tableau20 = [(48,48,48), (240,240,240), (59,170,6), (61,167,249),    
               (230,0,0),(105, 105, 105)]    
   
   # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
   for i in range(len(tableau20)):    
      r, g, b = tableau20[i]    
      tableau20[i] = (r / 255., g / 255., b / 255.)   


   fig = plt.figure(figsize=(21,7),constrained_layout=True)
   ax = plt.axes()



   #Color del fondo y fondo del gráfico.
   #alternativa mas personalizable que plt.style.use() 

   fig.patch.set_facecolor(tableau20[0])
   ax.patch.set_facecolor(tableau20[5])


   plt.title('\nFrecuencia Tuits - Serie temporal\n@'+target,fontsize=25,fontproperties=prop,color=tableau20[1])
   plt.ylabel('\nNúmero de Tuits\n',fontsize=20,fontproperties=prop,color=tableau20[1])
   plt.xlabel('\nFecha\n',fontsize=20,fontproperties=prop,color=tableau20[1])
   plt.plot(date_all,np.ones(len(date_all)),linewidth=0.01,color=tableau20[0])
   plt.plot(date,cnt,label='@'+target,linewidth=0.3,color=tableau20[3])
   plt.fill_between(date,cnt,0,alpha=0.12,color=tableau20[3])

   locator = mdates.AutoDateLocator(minticks=30, maxticks=35)
   formatter = mdates.ConciseDateFormatter(locator)
   ax.xaxis.set_major_locator(locator)
   ax.xaxis.set_major_formatter(formatter)

   leg = plt.legend(loc='upper left',fontsize=12)

   for legobj in leg.legendHandles:
      legobj.set_linewidth(2.0)

   plt.yticks(np.linspace(0,max(cnt),5,dtype = int, endpoint=True),fontsize=13,fontproperties=prop,color=tableau20[1])
   plt.xticks(fontsize=12,rotation=0,fontproperties=prop,color=tableau20[1])

   plt.annotate('Elecciones 2019', xy=(datetime(2019, 10, 20),10),xytext=(datetime(2019, 10, 25),16),fontsize=13,fontproperties=prop,color=tableau20[1],
               arrowprops=dict(facecolor='red', shrink=0.05))

   plt.xlim([inicio,fin])
   plt.ylim([1,max(cnt)+1])

   plt.gca().yaxis.grid(linestyle='--',linewidth=0.45,dashes=(5,15))
   plt.gca().xaxis.grid(linestyle='--',linewidth=0.6,dashes=(8,10))

   plt.axhline(np.mean(cnt),color=tableau20[2])  #horizontal line
   plt.text(date[-1],np.mean(cnt)+1,'  Promedio:\n  '+str(round(np.mean(cnt)))+' tuits/día',fontsize=11,fontproperties=prop,color=tableau20[1])
   plt.rc('axes',edgecolor='white')
   plt.gca().spines["top"].set_visible(True)    
   plt.gca().spines["bottom"].set_visible(True)    
   plt.gca().spines["right"].set_visible(True)    
   plt.gca().spines["left"].set_visible(True)
   plt.savefig('resultados/'+target+'_ts.png')



if __name__ == '__main__':
   frec_tw(input('Usuario a analizar: @'))