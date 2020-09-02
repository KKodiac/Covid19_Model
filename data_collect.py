import requests
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas
from os import makedirs
from typing import Dict, List

class data_collect:
    def __init__(self,
        DAT_F="WHO-COVID-19-global-data.csv",
        DAT_L="https://covid19.who.int/WHO-COVID-19-global-data.csv"
    ):
        self.datf = DAT_F
        self.datl = DAT_L
        self.dr = csv.DictReader(open(self.datf, 'w+',encoding='utf-8'))
        self.pdF = open("csvData.csv", encoding='utf-8')
        self.pdDict = csv.DictReader(self.pdF)
        self.country_data = []

    
    def get_country_list(self) -> List:
        tmp = [] 
        for row in self.dr:
            if(row[" Country"] not in tmp):
                tmp.append(row[" Country"])
        
        return tmp

    def scrapeData(self):
        req = requests.get(self.datl)
        with open(self.datf, 'w+') as file:
            file.write(req.text)
            file.close()

    def getData(self):
        try:
            makedirs("Data/")
        except FileExistsError:
            pass
        
        self.scrapeData()
        
        country_list = self.get_country_list()
        df = pandas.read_csv(self.datf)
        for country in country_list:
            f = open("Data/{}.txt".format(country), 'w+', encoding='utf-8')
            tmp_data = []
            for row in df.values:
                if(row[2] == country):
                    if(row[4]<0):
                        tmp = 0
                    else:
                        tmp = row[4]
                    tmp_data.append(tmp)

            # Write in data before processing
            for i in tmp_data:
                f.write('{} '.format(i))
            f.write('\n')
            # Write in data after processing 
            othdata = self.getOtherData(tmp_data, df, country)
            if(othdata==0):
                othdata = tmp_data
            
            for i in othdata:
                f.write("{} ".format(str(i)))
            f.close()

    
    def resize(self, krdata: list, krdatlen: int, b_data: list, country: str) -> List:
        kr_density = 511.6175
        a_data = []
        if(len(b_data)<krdatlen):
            while(len(b_data)<krdatlen):
                b_data.insert(0,0)
        elif(len(b_data)>krdatlen):
            b_data = b_data[(len(b_data)-krdatlen):] 
        pd = csv.DictReader(open("csvData.csv", encoding='utf-8'))
        
        # print(country, b_data)
        for row in pd:
            if((row['country'] == country)):
                # print(row['country'], country)
                population_density = int(float(row['density']))
                break
            elif(row['country'] in country):
                population_density = int(float(row['density']))
                break
            elif(country in row['country']):
                population_density = int(float(row['density']))
                break
            else:
                # print("Country doesn't exist in File {}".format(country))
                population_density = 0
        try:
            for i in b_data:
                a_data.append((kr_density*i)/(population_density))
        except ZeroDivisionError:
            return 0
        
        return a_data


    def getOtherData(self, b_data, df, country):
        othdata = self.resize(self.getKrData(df), len(self.getKrData(df)), b_data, country)
        # print("a_getOtherData() : {} ".format(othdata))
        return othdata

    def getKrData(self,df):
        krdata = []
        
        for row in df.values:
            # print(row)
            if(row[2] == "Republic of Korea"):
                krdata.append(row[4])
        
        return krdata

    def getKrDateSpectrum(self, df):
        krdata = []
        
        for row in df.values:
            # print(row)
            if(row[2] == "Republic of Korea"):
                krdata.append(row[0])
        
        return krdata

    def showData(self):
        # country_list = self.get_country_list()
        
        # for country in country_list:
        #     f = open("Data/{}.txt".format(country), encoding='utf-8')
        #     data = f.readlines()[1]
        #     dl = data.split(' ')
        #     plt.plot(dl)
        df = pandas.read_csv(self.datf)
        list_date = self.getKrDateSpectrum(df)
        f = open("Data/Republic of Korea.txt", encoding='utf-8')
        data = f.readlines()[1]
        
        plt.plot(list_date,data.split(' ')[:len(list_date)])
        plt.show()

dc = data_collect()

dc.getData()
dc.showData()