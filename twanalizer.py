from app.extract import recopilar
from app.timeserie import timeserie
from app.nlptw import graf
from app.sentiment import data_sentiment


targets = ['LuchoXBolivia','LuisFerCamachoV','tutoquiroga','JeanineAnez','carlosdmesag']

for t in targets:
#recopilar(t)
#timeserie(t)
#graf(t)
   data_sentiment(t)
