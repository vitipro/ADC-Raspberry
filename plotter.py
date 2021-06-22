import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

num_plots = 1
file_name = "results.log"


def read_file(file_name):
    curr_directory = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(curr_directory, file_name)
    myfile = open(file_name, "r")
    mylines = myfile.readlines()

    x = []
    y = []
    for i in range(len(mylines) // 2):
        myline = str.replace(mylines[i * 2], '\n', '')
        voltatge_osc = myline.split(':')[1]
        voltatge_adc = str.replace(mylines[i * 2 + 1], '\n', '')
        x.append(voltatge_osc)
        y.append(voltatge_adc)
    myfile.close()
    return np.array(x).astype(np.float_), np.array(y).astype(np.float_)


# def

def plot():
    fig, ax1 = plt.subplots(1, num_plots, figsize=(10, 10))
    plt.sca(ax1)
    ax1.grid()

    ax1.set_xlabel('voltatge oscil·loscopi')
    ax1.set_ylabel('voltatge adc')

    data_x, data_y = read_file("results.log")

    slope, intercept, r, p, std_err = stats.linregress(data_x, data_y)
    def myfunc(x):
        return slope * x + intercept
    mymodel = list(map(myfunc, data_x))

    plt.plot(data_x, mymodel, 'b-')
    ax1.scatter(data_x, data_y, color='r')
    ax1.set_title("Linealitat de l'ADC: R=" + str(r))
    fig.savefig('./plot.png')
    plt.show()


plot()
# print(read_file("results.log"))