import stanza, re, csv, os
import pandas as pd
from pysentimiento import create_analyzer

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
import matplotlib.dates as mdates
from datetime import datetime, timedelta



nlp = stanza.Pipeline(lang='es');

analyzer = create_analyzer(task="sentiment", lang="es");


def tokenizar(mensaje):
    ''' Al obtener una frase elimina numeros simbolos links
    SOLO devúelve el mensaje limpio'''
    doc = nlp(mensaje);
    #recuperamos todos los textos
    word_tokens = [token.text.lower() for sent in doc.sentences for token in sent.words]

    #ahora debemos limpiar simbolos, links, numeros.
    link = [re.sub('http\S+','',word) for word in word_tokens]
    signs =  '[/#@\'!"$%&()*+,-.:\;<=>?^_`{|}~]\\...'
    link_signs = [re.sub(signs,'',word) for word in link]
    link_signs_num = [re.sub('\d+','',word) for word in link_signs]
    emoji_pattern = re.compile("["
        u"\U0001F49A-\U000E007F" "]+", flags=re.UNICODE)

    link_signs_num_e = [re.sub(emoji_pattern,'',word) for word in link_signs_num]

    clean=[]
    for i,word in enumerate(link_signs_num_e):
        if not word == '':
            clean.append(word)
    
    return clean


def data_sentiment(target):
   dataset = pd.read_csv('resultados/'+target+'.csv')
   tw_text = dataset.iloc[:,2].values
   x_time = pd.to_datetime(dataset.iloc[:,1].values)
   x_time = [x.strftime('%Y/%m/%d') for x in x_time]
   x_time = [datetime.strptime(x,'%Y/%m/%d') for x in x_time]
   sentiment = []
    
   for text in tw_text:
      token = tokenizar(text)
      mss=''
      for x in token:
         mss+=x
         mss=mss+' ' 

      resp = analyzer.predict(mss)
      if(resp.output == 'NEG'):
         sentiment.append(1+resp.probas[resp.output])
      elif(resp.output == 'POS'):
         sentiment.append(1-resp.probas[resp.output])
      else: sentiment.append(1)

   with open('resultados/'+target+'_sent.csv','w',newline='\n') as file:
      spw = csv.writer(file, delimiter=',')
      spw.writerow(['fecha','dato'])
      for x in zip(x_time[::-1],sentiment[::-1]):
         spw.writerow(x)

   df1=pd.read_csv('resultados/'+target+'_sent.csv',sep=',').sort_values(by='fecha').set_index('fecha')
   #cnt1 = df1.rolling(7,min_periods=1).mean()
   cnt  = df1.rolling(28,min_periods=7).mean().iloc[:,:].values   
   #date = df1.index.values
   x_time = pd.to_datetime(dataset.iloc[:,1].values)
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
   plt.text(date[-13],0.75,'Sentimiento\nNeutro',fontsize=13,fontproperties=prop,color='black')

   plt.text(date[5],1.75,'Sentimiento\nPositivo',fontsize=13,fontproperties=prop,color='green')
   plt.text(date[5],0.25,'Sentimiento\nNegativo',fontsize=13,fontproperties=prop,color='red')
   plt.savefig('resultados/'+target+'_sent.png')
   #os.remove('resultados/'+target+'_sent.csv')
   