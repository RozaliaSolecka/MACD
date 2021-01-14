import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def ema_function(period, current_day, data):
    one_minus_alpha = float(1 - (2 / (period + 1)))
    numerator = 0
    denominator = 0

    for i in range(0,period+1):  # od 0 do 26 lub od 0 do 12
        pow = float(one_minus_alpha ** i)
        numerator = float(numerator + (pow * data[current_day - i]))
        denominator = float(denominator + pow)
    return float(numerator / denominator)

def macd_function(current_day, data):

    return float(ema_function(12, current_day, data) - ema_function(26, current_day, data))

def rsi_function(period, current_day, data):
    a = 0
    a_counter = 0
    b = 0
    b_counter = 0
    rs = 0
    rsi = 0
    for i in range(period-1):
        if data[current_day-i] > data[current_day-i-1]:
            a = a + data[current_day-i] - data[current_day-i-1]
            a_counter = a_counter +1
        elif data[current_day-i] < data[current_day-i-1]:
            b = b + data[current_day - i - 1] - data[current_day - i]
            b_counter = b_counter +1
    a = a/a_counter
    b = b/b_counter
    rs = a/b
    rsi = 100 - (100/(1+rs))
    return rsi

def diagram(macd, signal, newlist, rsi, arguments):
    # diagram

    # #1 MACD, SIGNAL
    plt.plot(arguments, macd, label='macd')
    plt.plot(arguments, signal, label='signal')
    plt.title('MACD & SIGNAL')
    plt.legend(loc='best')
    plt.xlabel('day')
    plt.ylabel('value')
    plt.show()

    # #2 INPUT
    plt.plot(arguments, newlist, label='input')
    plt.title('INPUT')
    plt.legend(loc='best')
    plt.xlabel('day')
    plt.ylabel('value')
    plt.show()

    # #3 MACD, SIGNAL, INPUT
    fig, axs = plt.subplots(2, 1)  # 2 rows, 1 column
    axs[0].plot(arguments, macd, label='macd')
    axs[0].plot(arguments, signal, label='signal')
    axs[0].set_title('MACD & SIGNAL')
    axs[0].set_xlabel('day')
    axs[0].set_ylabel('value')
    axs[0].legend(loc='best')

    axs[1].plot(arguments, newlist, label='input')
    axs[1].set_title('INPUT')
    axs[1].set_xlabel('day')
    axs[1].set_ylabel('value')
    axs[1].legend(loc='best')

    fig.tight_layout(pad=1)
    plt.show()

    # #4 RSI
    plt.plot(arguments, rsi, label='rsi')
    plt.title('RSI')
    plt.legend(loc='best')
    plt.xlabel('day')
    plt.ylabel('value')
    plt.show()

# #3 MACD, SIGNAL, RSI
    fig, axs = plt.subplots(2, 1)  # 2 rows, 1 column
    axs[0].plot(arguments, macd, label='macd')
    axs[0].plot(arguments, signal, label='signal')
    axs[0].set_title('MACD & SIGNAL')
    axs[0].set_xlabel('day')
    axs[0].set_ylabel('value')
    axs[0].legend(loc='best')

    axs[1].plot(arguments, rsi, label='rsi')
    axs[1].set_title('RSI')
    axs[1].set_xlabel('day')
    axs[1].set_ylabel('value')
    axs[1].legend(loc='best')

    fig.tight_layout(pad=1)
    plt.show()

def BuyOrSell_1(buy_sell, macd, signal, closureValues):
    for i in range(36):
        buy_sell.append("none")  # 35

    for i in range(36, len(macd)):  # bo 35, ale jest [i-1] więc 36
        if macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
            buy_sell.append("sell")
        elif macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
            buy_sell.append("buy")
        else:
            buy_sell.append("none")

    return buy_sell

def BuyOrSell_2(buy_sell_2, macd, signal, closureValues):
    for i in range(36):
        buy_sell_2.append("none")  # 35

    for i in range(36, len(macd)):  # bo 35, ale jest [i-1] więc 36
        if macd[i - 1] > signal[i - 1] and macd[i] < signal[i] and macd[i] < 0:
            buy_sell_2.append("sell")
        elif macd[i - 1] < signal[i - 1] and macd[i] > signal[i] and macd[i] > 0:
            buy_sell_2.append("buy")
        else:
            buy_sell_2.append("none")

    return buy_sell_2

def algorithm_macd1(buy_sell, macd, signal, closureValues):

    moneyBeforeSimulation = 1000
    moneyAfterSimulation = 1000
    numberOfAction = 0
    for i in range(len(closureValues)):
        if buy_sell[i] == 'buy' and moneyAfterSimulation > 0:
            rate= moneyAfterSimulation/closureValues[i]
            moneyAfterSimulation = 0
            numberOfAction = numberOfAction +rate

        elif buy_sell[i] == 'sell' and numberOfAction !=0:
           moneyAfterSimulation = moneyAfterSimulation + (numberOfAction * closureValues[i])
           numberOfAction=0

    profit = round(((moneyAfterSimulation / moneyBeforeSimulation * 100 ) - 100),2)
    print("Algorithm 1 macd")
    print("Profit " + str(profit) + "%")
    print("Money after simulation " + str(round(moneyAfterSimulation, 2)))
    print("Value of shares after simulation " + str(round((numberOfAction*closureValues[999]),2)))  #koszt akcji po symulacji
    print("")


def algorithm_macd2(buy_sell_2, macd, signal, closureValues):

    moneyBeforeSimulation = 1000
    moneyAfterSimulation = 1000
    numberOfAction = 0
    for i in range(len(closureValues)):
        if buy_sell_2[i] == 'buy' and moneyAfterSimulation > 0:
            rate= moneyAfterSimulation/closureValues[i-4]
            moneyAfterSimulation = 0
            numberOfAction = numberOfAction +rate

        elif buy_sell_2[i] == 'sell' and numberOfAction !=0:
           moneyAfterSimulation = moneyAfterSimulation + (numberOfAction * closureValues[i-4])
           numberOfAction=0

    profit = round(((moneyAfterSimulation / moneyBeforeSimulation * 100 ) - 100),2)
    print("Algorithm 2 macd")
    print("Profit " + str(profit) + "%")
    print("Money after simulation " + str(round(moneyAfterSimulation, 2)))
    print("Value of shares after simulation " + str(round((numberOfAction*closureValues[999]),2)))  #koszt akcji po symulacji
    print("")


def algorithm_rsi3(buy_sell, macd, signal, rsi ,closureValues):
    moneyBeforeSimulation = 1000
    moneyAfterSimulation = 1000
    numberOfAction = 0
    for i in range(14, len(closureValues)):
        if  buy_sell[i] == 'buy' and rsi[i] <= 30 and moneyAfterSimulation > 0 :  #buy
            rate = moneyAfterSimulation / closureValues[i]
            moneyAfterSimulation = 0
            numberOfAction = numberOfAction + rate

        elif buy_sell[i] == 'sell' and rsi[i] >= 70 and numberOfAction !=0:  #sell
            moneyAfterSimulation = moneyAfterSimulation + (numberOfAction * closureValues[i])
            numberOfAction = 0

    profit = round(((moneyAfterSimulation / moneyBeforeSimulation * 100) - 100), 2)
    print("Algorithm 3 rsi ")
    print("Profit " + str(profit) + "%")
    print("Money after simulation " + str(round(moneyAfterSimulation, 2)))
    print("Value of shares after simulation " + str(round((numberOfAction*closureValues[999]),2)))  # koszt akcji po symulacji
    print("")

### main

my_list = pd.read_csv('wig20.csv', header=0, usecols=[4])  # zamkniecie
arguments = pd.read_csv('wig20.csv', header=0, usecols=[0], parse_dates=['Data'])   #daty
macd = []
signal = []
closureValues =[]   #zamkniecie
my_array = np.array(my_list)           # tymczasowa tablica
buy_sell = []                           #kupic_czy_sprzedac
buy_sell_2 = []                           #kupic_czy_sprzedac
rsi = []

for i in my_array:
    if i!= 'Data' and i != 'Zamkniecie':
        closureValues.append(float(i))

for i in range(len(closureValues)):

    if i >= 26:
        macd.append(macd_function(i, closureValues))
    else:
        macd.append(None)

for i in range(len(macd)):

    if i >= 35:
        signal.append((ema_function(9, i, macd)))
    else:
        signal.append(None)

for i in range(len(closureValues)):
    if i >= 13:
        rsi.append(rsi_function(14, i, closureValues))
    else:
        rsi.append(None)

diagram(macd, signal, closureValues, rsi, arguments)

BuyOrSell_1(buy_sell,macd, signal, closureValues)
algorithm_macd1(buy_sell, macd, signal, closureValues)

BuyOrSell_2(buy_sell_2,macd, signal, closureValues)
algorithm_macd2(buy_sell_2, macd, signal, closureValues)

algorithm_rsi3(buy_sell, macd, signal, rsi ,closureValues)
