import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from typing import Dict, List
DATA = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
DATF = "WHO-COVID-19-global-data.csv"

def get_data(country):
    # 특정 country의 코로나 신규 확진자 데이터를 크롤링한다.
    # 사이트 : WHO COVID19 dashboard - DATA
    req = requests.get(DATA)

    with open(DATF, 'w+') as file:
        file.write(req.text)
        file.close()

def __get_country_list() -> List:
    csv_file = open(DATF)
    reader = csv.DictReader(csv_file)
    buffer = []
    for row in reader:
        if(row[" Country"] not in buffer):
            buffer.append(row[" Country"])

    return buffer


def __get_code_list() -> List:
    csv_file = open(DATF)
    reader = csv.DictReader(csv_file)
    buffer = []
    for row in reader:
        if(row[" Country_code"] not in buffer):
            buffer.append(row[" Country_code"])

    return buffer


def __get_region_list() -> List:
    csv_file = open(DATF)
    reader = csv.DictReader(csv_file)
    buffer = []
    for row in reader:
        if(row[" WHO_region"] not in buffer):
            buffer.append(row[" WHO_region"])

    return buffer


def parse_data():
    df = pd.read_csv(DATF, sep=',')
    country = __get_country_list()
    for name in country:
        f = open("Data/%s.txt" % name, 'w+')
        for row in df.values:
            if(row[2] == name):
                # Negative # to 0
                if(row[4]<0):
                    tmp = 0
                else:
                    tmp = row[4]
                f.write('{} '.format(str(tmp)))
            
        
        
    
parse_data()

def upper_half(a):
    # 두 반환값의 합이 a가 되도록 한다.
    half = a // 2
    if a % 2 == 0:
        return half, half
    return half, half + 1


def moving_average(data, size=2):
    # 이동 평균을 계산하여 반환한다.
    result = []
    size = upper_half(size)
    for i in range(len(data)):
        result.append(np.mean(data[i-size[0]:i+size[1]]))
    return result


def rescale(data, crit, measure="mean", cutratio=0.):
    # data를 crit과 비슷한 값으로 rescaling한다.
    if measure == "max":
        # 최댓값이 비슷해지도록 rescaling한다.
        crit = crit ** np.random.uniform(1.05, 1.07)
        measure_fun = lambda data, crit: np.linalg.norm(max(data) - max(crit))
    elif measure == "median":
        # 최댓값이 비슷해지도록 rescaling한다.
        # 단, crit의 앞 부분은 무시하고 최댓값을 구한다.
        crit = crit ** 1.1
        measure_fun = lambda data, crit: np.linalg.norm(max(data) - max(crit[75:]))

    w = min([[measure_fun(data * i, crit), i] for i in np.arange(0, 4, 0.0001)])[1]
    return data * w


# # 크롤링할 국가들 목록
# countries = ['us', 'brazil', 'india', 'russia', 'south-africa', 'peru', 'mexico', 'colombia', 'spain', 'chile', 'iran',
#              'argentina', 'uk', 'saudi-arabia', 'bangladesh', 'pakistan', 'italy', 'turkey', 'france', 'germany',
#              'iraq', 'philippines', 'indonesia', 'canada', 'qatar', 'bolivia', 'ecuador', 'ukraine', 'kazakhstan',
#              'israel', 'egypt', 'dominican-republic', 'panama', 'sweden', 'oman', 'belgium', 'kuwait', 'romania',
#              'belarus', 'guatemala', 'united-arab-emirates', 'netherlands', 'poland', 'japan', 'singapore', 'portugal',
#              'honduras', 'morocco', 'nigeria', 'bahrain', 'ghana', 'kyrgyzstan', 'armenia', 'algeria', 'ethiopia',
#              'switzerland', 'venezuela', 'uzbekistan', 'afghanistan', 'azerbaijan', 'costa-rica', 'moldova', 'kenya',
#              'nepal', 'serbia', 'ireland', 'austria', 'australia', 'el-salvador', 'czech-republic', 'state-of-palestine',
#              'cameroon', 'bosnia-and-herzegovina', 'cote-d-ivoire', 'denmark', 'bulgaria', 'madagascar', 'macedonia',
#              'paraguay', 'senegal', 'sudan', 'lebanon', 'zambia', 'libya', 'norway']

# # 대한민국부터 크롤링
# kr_data = get_data('south-korea')

# # countries의 국가들 차례대로 크롤링
# for country in countries:
#     print('country:', country)

#     cur_data = get_data(country)  # 신규 확진자 데이터 크롤링

#     result = []

#     cur_data2 = rescale(cur_data, kr_data, measure="median")  # 최댓값 기준으로 rescaling (y축 rescaling)
#     cur_data2 = moving_average(cur_data2, size=4)  # 이동 평균 -> 들락날락한 데이터 제거
#     result.append(cur_data2)

#     cur_data = rescale(cur_data, kr_data, measure="max")  # 최댓값 기준으로 rescaling (y축 rescaling)
#     cur_data = resize(cur_data.reshape((-1, 1)), (int(len(cur_data)*0.7), 1)).reshape(-1)  # x축 rescaling
#     cur_data = moving_average(cur_data, size=4)  # 이동 평균 -> 들락날락한 데이터 제거
#     result.append(cur_data)

#     # 데이터 저장
#     if not os.path.isdir('data'):
#         os.mkdir('data')
#     with open('data/%s_data.txt' % country, 'w', encoding='utf8') as f:
#         f.write('\n'.join([' '.join(map(str, i)) for i in result]))

# # 가장 마지막 국가의 데이터 시각화
# plt.plot(kr_data, color='b')
# plt.plot(cur_data, color='r')
# plt.plot(cur_data2, color='g')
# plt.legend(['korea', country + '(median)', country + '(max)'])
# plt.show()
