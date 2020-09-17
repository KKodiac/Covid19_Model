import pandas as pd

tmpf = open("Data/Spain.txt")
fr = tmpf.readlines()[1]
datalen = len(fr.strip().split(' '))

with open('GyeonggiData/core_data.txt') as data:
    df = data.read()
    core = df.strip().split(' ')
    while(len(core)!=datalen):
        core.insert(0, '0')

    data.close()

with open('GyeonggiData/core_data.txt', 'w') as data:
    tmpstr = " ".join(core)
    data.write(tmpstr)
print(len(core))