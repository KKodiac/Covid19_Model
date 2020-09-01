from data_collect import data_collect

dc = data_collect()

dc.getData()

krf = open("Data/Republic of Korea.txt")
kr = krf.read()
print(kr.split(" "))
othf = open("Data/France.txt")
oth = othf.read()
print(oth.split(" "))