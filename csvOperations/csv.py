import pandas as pd

dfRC = pd.read_csv(r'./REDRC.csv', header=0)
dfDPS = pd.read_csv(r'./DSPatients.csv', header =0)

dfRCTest = dfRC.head()
dfDPSTest = dfDPS.head()