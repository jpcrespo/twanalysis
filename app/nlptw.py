import stanza, re, operator, os 
import pandas as pd
import numpy as np
from collections import Counter,OrderedDict
from PIL import Image

from wordcloud import WordCloud
import warnings
import random
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams

#stanza.download('es')
nlp = stanza.Pipeline(lang='es');


def tokenizar(mensaje):
    ''' Al obtener una frase elimina numeros simbolos links
    palabras stop y articulos. solo devuelve las palabras sin
    articulos en una lista de strings'''
    doc = nlp(mensaje)
    #recuperamos todos los textos
    word_tokens = [token.text.lower() for sent in doc.sentences for token in sent.words]

    #ahora debemos limpiar simbolos, links, numeros.
    link = [re.sub('http\S+','',word) for word in word_tokens]
    signs =  '[/#@\'!"$%&()*+,-.:\;<=>?^_`{|}~]'
    link_signs = [re.sub(signs,'',word) for word in link]
    link_signs_num = [re.sub('\d+','',word) for word in link_signs]
    emoji_pattern = re.compile("["
        u"\U0001F49A-\U000E007F" "]+", flags=re.UNICODE)

    link_signs_num_e = [re.sub(emoji_pattern,'',word) for word in link_signs_num]

    clean=[]
    for i,word in enumerate(link_signs_num_e):
        if not word == '':
            clean.append(word)
    
    stopword = ['pasa','solo','como','sobre','esa','vez','cada',"algo","para","este","algún",'pero',"de",'alla','aún','cual','cuan','cuando','desde','donde','muy','otro','otra','pues','sino','tus','mis','este','esté','esta']

    aux1 = [word for word in clean if len(word)>3]
    aux2 = []
    for x in aux1:
        if not (x in stopword):
            aux2.append(x)

    return aux2


def date_historial(target):
    '''Devuelve la cantidad de palabras total de un usuario
    la cantidad promedio por tuit y finalmente las palabras y la cantidad de 
    veces usada
    '''
    dataset = pd.read_csv('resultados/'+target+'.csv')
#recupera los valores de interes (texto)
    tw_text = dataset.iloc[:,2].values
    long = 0
    aux1 = []
    words=[]
    for word in tw_text:
        aux = tokenizar(word)
        aux1.append(len(aux))
        long+=len(aux)
        words.extend(aux)

    w = Counter(words)
    top = sorted(w.items(),key=operator.itemgetter(1),reverse=True)

    return long,round(np.mean(np.array(aux1))),top

def graf(target):
    a,b,c=date_historial(target)
#calculamos el top de palabras
    words = []
    cnt = []
    for x in c[:10]:
        words.append(x[0])
        cnt.append(x[1])

    fpath = os.path.join('app/MonoLisa.ttf')
    prop = fm.FontProperties(fname=fpath)
    fname = os.path.split(fpath)[1]

    colores = [(48,48,48),             #color negro (fondo)
                (240,240,240),          #color letras 
                (152,152,152)]          #color semi blanco (2do fondo)
            
    for i in range(len(colores)):    
        r, g, b = colores[i]    
        colores[i] = (r / 255., g / 255., b / 255.)   


    fig = plt.figure(figsize=(6,6))
    ax = plt.axes()

    fig.patch.set_facecolor(colores[0])
    ax.patch.set_facecolor(colores[2])
    
    plt.barh(words[::-1],cnt[::-1],color='tomato',edgecolor='black')

    text_sets = {'color':  colores[1],'weight': 'normal','size': 16,'fontproperties':prop}
    plt.xlabel("\nRepeticiones\n",fontsize=17,fontdict=text_sets)
    plt.title('\nTop 10\npalabras más usadas\n',fontsize=35,fontdict=text_sets)

    plt.xticks(fontsize=10,fontproperties=prop,color=colores[1])
    plt.yticks(words,fontsize=15,fontproperties=prop,color=colores[1])
    plt.text(cnt[0]*1.1,words[3],'Cuenta:\n @'+target,fontsize=25,fontproperties=prop,color=colores[1])
    #plt.text(cnt[0]*1.2,words[7],'- '+str(a)+' Distintas\npalabras usadas\n',fontdict=text_sets)
    #plt.text(cnt[0]*1.1,words[8],'- Palabras\Tuit\npromedio: '+str(b),fontdict=text_sets)
    plt.savefig('resultados/'+target+'_words.png',bbox_inches='tight',dpi=100)
    plt.close(fig)

    mss = ''
    for x in c:
        mss+=x[0]
        mss=mss+' '

    fig = plt.figure(figsize=(7,7))   
    fig.patch.set_facecolor(colores[0])
    x, y = np.ogrid[:300, :300]
    mask = np.array(Image.open("app/test.png"))
    wc = WordCloud(max_words=140, mask=mask,margin=0,repeat=True, min_font_size=5,contour_width=1, contour_color='white').generate(mss)
    default_colors = wc.to_array()
    plt.axis("off")
    plt.title('WordCloud\npalabras más usadas\n@'+target,fontsize=25,fontdict=text_sets)
    plt.imshow(default_colors,interpolation='bilinear')
    plt.savefig('resultados/'+target+'_wordcloud.png',bbox_inches='tight',dpi=100)
    plt.close(fig)