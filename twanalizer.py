from app.extract import recopilar
from app.timeserie import timeserie
from app.nlptw import date_historial, graf
from app.sentiment import data_sent




#targets = ['','LuisFerCamachoV','tutoquiroga']
targets = ['carlosdmesag',]


for t in targets:
  recopilar(t)
  timeserie(t)
  graf(t)
  data_sent(t)


