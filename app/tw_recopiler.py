''' 
Este Script recopila los 3200 tuits mas recientes de un target y genera:
1. user_info.txt file - Toda la información disponible de contacto
2. user_historial.csv file - Un csv con los tuits: fecha y texto.
'''

from dotenv import load_dotenv
import os, tweepy, csv, pytz
from datetime import datetime


def recopilar(target):
    #no hay bolivia :( pero es igual a Caracas
    local_timezone = pytz.timezone('America/Caracas')

    #load_dotenv('/home/ghost/Desktop/proyectos/tw/.env')
    load_dotenv('.env_tw')

    API_KEY = os.getenv('API_Key')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

    print('Iniciamos autentificación con Twitter API')
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Autentificación... sesión iniciada  ok!")
    except:
        print("No se logra iniciar sesión, ERROR!")


    # Dirección del usuario twitter @user
    print('El usuario a analizar: @',target)
    user = api.get_user(screen_name=target)

    with open('resultados/'+target+'_info.txt','w',encoding='utf-8') as txt:
        txt.write("User details:\n")
        #txt.write('id: ' + user.id)
        txt.write('id_str: '+user.id_str+'\n')
        txt.write('name: '+ user.name+'\n')
        txt.write('screen_name: ' +user.screen_name+'\n')
        txt.write('location: ' +user.location+'\n')
        #print('derived: ',user.derived)
        txt.write('url: '+str(user.url)+'\n')
        txt.write('description: '+user.description+'\n')
        txt.write('protected: '+ str(user.protected)+'\n')
        txt.write('verified: '+str(user.verified)+'\n')
        txt.write('followers_count: '+str(user.followers_count)+'\n')
        txt.write('friends_count: '+str(user.friends_count)+'\n')
        txt.write('listed_count: '+str(user.listed_count)+'\n')
        #txt.write('profile_banner_url: '+user.profile_banner_url+'\n')

        print('Archivo con información del user creado.')

        print('Recopilando todos los tuits')

        historial = []

        for status in tweepy.Cursor(api.user_timeline,screen_name=target,tweet_mode="extended",count=100).items():
            historial.append(status)

    with open('resultados/'+target+'.csv','w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['#user','date','text'])
        for tuit in historial:
            dtime = datetime.strptime(tuit._json['created_at'],'%a %b %d %H:%M:%S %z %Y')
            writer.writerow([tuit._json['user']['screen_name'],dtime.astimezone(local_timezone),tuit._json['full_text'].replace('\n',' ')])

    

    print('Finalizado! Se recopiló '+str(len(historial))+' tuits')

if __name__== '__main__':
    recopilar(input('Usuario a analizar: @'))
