import pandas as pd
import os


import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import matplotlib.dates as mdates
from datetime import datetime, timedelta


target = 'carlosdmesag'

df1=pd.read_csv('resultados/'+target+'/sent.csv',sep=',')

cnt  = df1.rolling(28,min_periods=1).mean().iloc[:,:].values   
x_time = pd.to_datetime(df1.iloc[:,0].values)
x_time = [x.strftime('%Y/%m/%d') for x in x_time]
date = [datetime.strptime(i,'%Y/%m/%d') for i in x_time]


fpath = os.path.join('app/MonoLisa.ttf')
prop = fm.FontProperties(fname=fpath)
fname = os.path.split(fpath)[1]

colores = [(192, 192, 192),          #color (fondo)
               (0,0,0),                 #color letras 
               (230,230,230),          #color semi blanco (2do fondo)
               (25,25,112)]          #color graf



for i in range(len(colores)):    
   r, g, b = colores[i]    
   colores[i] = (r / 255., g / 255., b / 255.)   


fig = plt.figure(figsize=(21,7),constrained_layout=True)
ax = plt.axes()

fig.patch.set_facecolor(colores[0])
ax.patch.set_facecolor(colores[2])

text_sets = {'color':  colores[1],'weight': 'normal','size': 25,'fontproperties':prop}
   
plt.title('\nAnálisis sentimiento en el tiempo\n',fontsize=35,fontdict=text_sets)
plt.ylabel('\nSentimiento\n',fontdict=text_sets)
plt.xlabel('\nFecha\n',fontdict=text_sets)

plt.plot(date,cnt,linewidth=2,color=colores[3])

locator = mdates.AutoDateLocator(minticks=20, maxticks=30)
formatter = mdates.ConciseDateFormatter(locator)

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.yticks(fontsize=15,fontproperties=prop,color=colores[1]);
plt.xticks(fontsize=18,rotation=0,fontproperties=prop,color=colores[1]);
 #plt.gca().yaxis.grid(linestyle='--',linewidth=0.8,dashes=(5,15))
plt.gca().xaxis.grid(linestyle='--',linewidth=0.5,dashes=(8,10))
plt.text(date[-8],cnt[-1],' @'+target+' ',fontsize=20,fontproperties=prop,color=colores[3])
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(True)
plt.ylim([0,2])
plt.xlim([date[0],date[-1]])

plt.axhline(1,color='azure')  #horizontal line
ax.axhspan(0,1, facecolor='tomato', alpha=0.05)
ax.axhspan(1,2, facecolor='lime', alpha=0.05)
plt.text(date[5],1.75,'Sentimiento\nPositivo',fontsize=13,fontproperties=prop,color='green')
plt.text(date[5],0.25,'Sentimiento\nNegativo',fontsize=13,fontproperties=prop,color='red')
plt.savefig('resultados/'+target+'/sent.png')
   #os.remove('resultados/'+target+'_sent.csv')
   