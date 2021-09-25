import pandas as pd

dfRC = pd.read_csv(r'./REDRC.csv', header=0)
dfDPS = pd.read_csv(r'./DSPatients.csv', header =0, encoding = 'cp1252')

dfRCTest = dfRC.head()
dfDPSTest = dfDPS.head()

print(dfRCTest)

#with open("./REDRC.csv") as f: 
    #print(f)

for ind, row in dfRCTest.iterrows(): 
    for dpsInd, dpsRow in dfDPSTest.iterrows():
        print(10000 + ind,row)
        print(2000 + dpsInd, dpsRow)
