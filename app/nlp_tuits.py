
import stanza
import re

#stanza.download('es')
nlp = stanza.Pipeline(lang='es');

def tokenizar(mensaje):

    doc = nlp(mensaje)
    #recuperamos todos los textos
    word_tokens = [token.text.lower() for sent in doc.sentences for token in sent.words]

    #ahora debemos limpiar simbolos y links

    link = [re.sub('http\S+','',word) for word in word_tokens]
    signs =  '[/#@\'!"$%&()*+,-.:\;<=>?^_`{|}~]'
    link_signs = [re.sub(signs,'',word) for word in link]
    link_signs_num = [re.sub('\d+','',word) for word in link_signs]

    from collections import OrderedDict
    aux = list(OrderedDict.fromkeys(link_signs_num))

    for i,word in enumerate(aux):
        if word=='':
            aux.pop(i)
    return aux


if __name__=='__main__':
    a = tokenizar('que hijos de mil putas #bolivia')
    print(type(a))