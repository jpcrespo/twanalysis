from dotenv import load_dotenv
import os, tweepy, csv, pytz
from datetime import datetime

#no hay bolivia :( pero es igual a Caracas
local_timezone = pytz.timezone('America/Caracas')

#load_dotenv('/home/ghost/Desktop/proyectos/tw/.env')
load_dotenv('.env_tw')

API_KEY='DJahAj7JknAaTJwYKWpMpEcNu'
API_SECRET_KEY='J8haVuXvGQ0CZ88PHirrDy3eWPm7jIG0W3Phj8Ba0xE754MhdD'
ACCESS_TOKEN='1416223413052530696-YEza71GQ3gdULb0FZfZb5Czcz1C2tU'
ACCESS_TOKEN_SECRET='kwzyXSqEhfFXCd39YBppQMBCwDXeC3oLMmacMtDuOawdl'

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
target='carlosdmesag'

print('El usuario a analizar: ',target)
user = api.get_user(screen_name=target)

with open(target+'.txt','w',encoding='utf-8') as txt:
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
   txt.write('profile_banner_url: '+user.profile_banner_url+'\n')

print('Archivo con información del user creado.')

print('Recopilando todos los tuits')

historial = []

for status in tweepy.Cursor(api.user_timeline,screen_name=target,tweet_mode="extended",count=100).items():
    historial.append(status)

with open(target+'_historial.csv','w',newline='',encoding='utf-8') as file:
   writer = csv.writer(file)
   writer.writerow(['#user','date','text'])
   for tuit in historial:
       dtime = datetime.strptime(tuit._json['created_at'],'%a %b %d %H:%M:%S %z %Y')
       writer.writerow([tuit._json['user']['screen_name'],dtime.astimezone(local_timezone),tuit._json['full_text'].replace('\n',' ')])

   





