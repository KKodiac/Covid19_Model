import requests 
import csv 
import matplotlib.pyplot as plt
import os
from typing import Dict, List

DATA = "https://covid19.who.int/WHO-COVID-19-global-data.csv"

try:
    os.makedirs("Data/")
except FileExistsError:
    pass

class Collect:
        
    def getText(self):
        data = requests.get(DATA)
        
        with open("WHO-COVID-19-global-data.csv", 'w+') as file:
            file.write(data.text)
            file.close()

        return data.text

    @staticmethod
    def __parse_data(l: list, dr: Dict, key: str) -> List:
        for row in dr:
            if(row[key] not in l):
                l.append(row[key])
        
        return l


    def parseData(self):
        data = {
            " Country": [],
            " Country_code": [],
            " WHO_region": [],

            " Data_reported": [],
            " New_cases": [],
            " Cumulative_cases": [],
            " New_deaths": [],
        }
        
        res = [key for key in data.keys()]
        print(res)
        with open("WHO-COVID-19-global-data.csv") as file:
            dict_reader = csv.DictReader(file)
            for row in dict_reader:
                
            file.close()
        
        print(data)
        

a = Collect()
a.parseData()