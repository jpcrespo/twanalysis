import stanza, re, csv, os
import pandas as pd
from pysentimiento import create_analyzer
from datetime import datetime




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


def data_sent(target):
   dataset = pd.read_csv('resultados/'+target+'/recopile_tw.csv')
   tw_text = dataset.iloc[:,2].values
   x_time = pd.to_datetime(dataset.iloc[:,0].values)
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

   with open('resultados/'+target+'/sent.csv','w',newline='\n') as file:
      spw = csv.writer(file, delimiter=',')
      spw.writerow(['fecha','dato'])
      for x in zip(x_time[::-1],sentiment[::-1]):
         spw.writerow(x)