import csv
import pandas as pd
from VideoGame import *

def saveVideoGame(f, oC):
    with open(f, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([oC.ID, oC.name, oC.platform, oC.hours, oC.progress, oC.posFile])

#def modifyVideoGame(f,oC):

def readVideoGame(f, lC):
    df = pd.read_csv(f)
    l = df.values.tolist()
    for custo in l:
        lC.append(VideoGame(custo[0], custo[1], custo[2], custo[3], custo[4], -1))

