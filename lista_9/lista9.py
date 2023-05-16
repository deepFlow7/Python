import matplotlib.pyplot as plt
import json
import requests
import math

# cena złota i kurs Euro w latach 2020, 2021

def date_to_string(month, year, day):
    return str(year) + '-' + ('0' if month < 10 else '') + str(month) + '-' + ('0' if day < 10 else '') + str(day)

def last_day_in_month(year, month):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        else:
            return 28
    if month < 8:
        return 30 + month % 2
    return 31 - month % 2

def average_monthly_gold_rate(month, year):
    startDate = date_to_string(month, year, 1)
    endDate = date_to_string(month, year, last_day_in_month(year, month))
    url = 'http://api.nbp.pl/api/cenyzlota/' + startDate + '/' + endDate
    response = requests.get(url).text
    response_info = json.loads(response)
    sum = 0
    for id in range (0, len(response_info)):
        sum += response_info[id]['cena']
    return round(sum / len(response_info), 2)

def monthly_euro_exchange_rate(month, year):
    startDate = date_to_string(month, year, 1)
    endDate = date_to_string(month, year, last_day_in_month(year, month))
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/EUR/' + startDate + '/' + endDate
    response = requests.get(url).text
    response_info = json.loads(response)
    sum = 0
    for id in range (0, len(response_info)):
        sum += response_info['rates'][0]['mid']
    return round(sum * 50 / len(response_info), 2)

def predict_rates(ys1, ys2, n):
    res = []
    res.append(ys2[n - 1] * ys2[n - 1] / ys2[n - 2]) # zakładam, że ostatnia tenedencja listopad-grudzień utrzyma się do stycznia, żeby 
    for i in range (1, n):
        delt1 = ys1[i] / ys1[i - 1]
        delt2 = ys2[i] / ys2[i - 1]
        delt3 = math.sqrt(delt2 * delt1)  # przyjmuję, że różnica między kolejnymi miesiącami wzrasta / maleje tyle samo razy co średnio w poprzednich latach
        res.append(res[i - 1] * delt3) 
    return res

fig, (ax2020, ax2021, ax2022) = plt.subplots(3,1)
fig.suptitle("Cena złota i Euro w latach 2020-2022")
fig.tight_layout(pad=2.0)
labels = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']

xs = [ n for n in range(1, 13) ]

ys_2020_1 = [ average_monthly_gold_rate(i, 2020) for i in xs ]
ys_2020_2 = [ monthly_euro_exchange_rate(i, 2020) for i in xs ]

ys_2021_1 = [ average_monthly_gold_rate(i, 2021) for i in xs ]
ys_2021_2 = [ monthly_euro_exchange_rate(i, 2021) for i in xs ]

ys_2022_1 = predict_rates(ys_2020_1, ys_2021_1, 12)
ys_2022_2 = predict_rates(ys_2020_2, ys_2021_2, 12)

ax2020.set_title('2020')
ax2021.set_title('2021')
ax2022.set_title('2022 (przewidywane)')

for ax, ys1, ys2 in zip([ax2020, ax2021, ax2022], [ys_2020_1, ys_2021_1, ys_2022_1], [ys_2020_2, ys_2021_2, ys_2022_2]):
    ax.set_xlabel('[miesiąc]')
    ax.set_ylabel('[zł]')
    ax.plot(labels, ys1)
    ax.plot(labels, ys2)
    ax.legend(["kurs złota", "cena za 50 Euro"])
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

plt.show()

