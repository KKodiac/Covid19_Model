from data_collect import *
from models import *
from preprocessing import load, labeling, train_test_split
import train
from predict import *
import options as opt
import joblib
from numpy import reshape


if __name__ == "__main__":
    pre_dat = data_collect()
    pre_dat.getData()

    data = load()
    x, y = labeling(data, sight=opt.SIGHT, y_n=opt.Y_N)
    x = x.reshape((-1, opt.SIGHT, 1))
    xtrain, xtest, ytrain, ytest = train_test_split(x,y, test_size=opt.TEST_SIZE)
    joblib.dump([xtrain, xtest, ytrain, ytest], 'traintest.joblib')  # 저장
    # shape shown of x and y processed datasets
    print(xtrain.shape)
    print(ytrain.shape)
    print(xtest.shape)
    print(ytest.shape)

    train.train()

    model = build_model()
    model.load_weights('weights.h5')

    x,y, full_x, full_y = load_korea_data()

    preds = model.predict(full_x)

    if(opt.POS >= 0):
        opt.POS -= len(x)
    forecast_x = np.append(x[opt.POS][-opt.SIGHT+opt.Y_N:], y[opt.POS][:])
    forecast_result = forecast(forecast_x, days=opt.DAYS)  # 'forecast' 예측

    # 시각화
    plt.plot(full_y, color='b')  # 'real data'
    plt.plot(np.arange(opt.SIGHT, opt.SIGHT+len(preds)), [i[0] for i in preds.reshape(-1, opt.Y_N)], 'r:')  # 'predict'

    last_x = len(x)+opt.SIGHT+opt.Y_N+1+opt.POS+opt.DAYS
    dates = get_dates(last_x)
    plt.plot(range(len(x)+opt.SIGHT+opt.Y_N+opt.POS, last_x),
             np.append([y[opt.POS][-1]], forecast_result), color='g', alpha=0.7)  # 'forecast'

    plt.title('COVID19 KR Predict')
    plt.xlabel('Date')
    plt.ylabel('Cases')
    plt.xticks(range(0, last_x, 40), dates)  # x축 Date
    plt.legend(['real data', 'predict', 'forecast'], prop={'size': 12})
    plt.grid(True, alpha=0.5, linestyle='-', linewidth=1)
    plt.show()
