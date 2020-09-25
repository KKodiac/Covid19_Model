import csv

tmpf = open("../Data/Spain.txt")
fr = tmpf.readlines()[1]
datalen = len(fr.strip().split(' '))


with open('1-1_data.csv', encoding='utf-16') as c:
    gdata = []
    creader = csv.reader(c)
    for i in creader:
        gdata.append(i[0])
    gdata.reverse()
    c.close()

with open('core_data.txt', 'w') as data:
    while(len(gdata)!=datalen):
        gdata.insert(0, '0')
    core = " ".join(gdata)
    data.write(core)
    data.close()
