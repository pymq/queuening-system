"""
В системе передачи цифровой информации передается речь в цифровом виде. Речевые пакеты передаются
через два транзитных канала, буферируясь в накопителях перед каждым каналом. Время передачи пакета
по каналу составляет 4 мс. Пакеты поступают через 5+-3мс. Пакеты, передававшиеся более 10 мс,
на выходе системы уничтожаются, так как их появление в декодере значительно снизит качество
передаваемой речи. Уничтожение более 27% пакетов недопустимо. При достижении такого уровня
система за счет ресурсов ускоряет передачу до 3 мс на канал. При снижении уровня до приемлемого
происходит отключение ресурсов.

Смоделировать 8 c работы системы. Определить частоту уничтожения пакетов и частоту подключения ресурса.
"""

from random import randint

import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.pylab
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator

from channel import Channel

interval = 8_000  # 8 sec
x = randint(2, 8)  # время генерации
n = 2  # количество каналов
z = 4  # время обслуживания
r = 3  # сниженное время обслуживания
m = 10  # максимальное время нахождения в системе
b = 0.27  # допустимый % потерь

N = 0  # кол-во переданных пакетов
X = 0  # кол-во уничтоженных пакетов
H = 0  # кол-во времени с включенным ускорением

j = 0  # номер заявки
t = 0  # время
A = []  # [(j, t), ...] - все заявки

while (t + x) <= interval:
    t += x
    j += 1
    A.append((j, t))
    x = randint(2, 8)

c1 = Channel(z)
c2 = Channel(z)

# ========================================
import pickle

# pickle.dump(A, open("save_.p", "wb"))
A = pickle.load(open("save1.p", "rb"))
j = len(A)
A_copy = list.copy(A)
# ========================================

new_requests = []
channel_one = []
channel_two = []
buffer_one = []
buffer_two = []
boost = []

i = 0  # время
while i < interval:
    if N and X / N > b:
        c1.set_service_time(r)
        c2.set_service_time(r)
        H += 1
        boost.append(2)
    else:
        c1.set_service_time(z)
        c2.set_service_time(z)
        boost.append(0)

    if A and A[0][1] == i:
        new_requests.append(2)
        c1.add(A[0])
        A.pop(0)
    else:
        new_requests.append(0)

    w1 = c1.work(i)
    if w1:
        c2.add(w1)

    w2 = c2.work(i)
    if w2:
        N += 1
        time_diff = w2[-1] - w2[1]  # время передачи пакета
        if time_diff > 10:
            X += 1
    i += 1
    channel_one.append(0 if c1.is_empty else 2)
    channel_two.append(0 if c2.is_empty else 2)
    buffer_one.append(c1.get_queue_count())
    buffer_two.append(c2.get_queue_count())


def make_plot():
    fontsize = 25
    linewidth = 3
    scale = 0.05
    count = int(len(new_requests) * scale) + 1
    majorLocator = MultipleLocator(10)
    minorLocator_y = AutoMinorLocator(n=2)
    majorFormatter = FormatStrFormatter('%d')

    fig, ax = plt.subplots(6, sharex='all', sharey='all', figsize=(34, 19))

    ax[0].plot(range(count), new_requests[:count], ls='steps', linewidth=linewidth)
    ax[0].set_title('Поступление пакетов', fontsize=fontsize)

    ax[1].plot(range(count), buffer_one[:count], ls='steps', linewidth=linewidth)
    ax[1].set_title('Первый буфер', fontsize=fontsize)

    ax[2].plot(range(count), channel_one[:count], ls='steps', linewidth=linewidth)
    ax[2].set_title('Первый канал', fontsize=fontsize)

    ax[3].plot(range(count), buffer_two[:count], ls='steps', linewidth=linewidth)
    ax[3].set_title('Второй буфер', fontsize=fontsize)

    ax[4].plot(range(count), channel_two[:count], ls='steps', linewidth=linewidth)
    ax[4].set_title('Второй канал', fontsize=fontsize)

    ax[5].plot(range(count), boost[:count], ls='steps', linewidth=linewidth)
    ax[5].set_title('Ускорение', fontsize=fontsize)

    for i in range(6):
        ax[i].xaxis.set_major_locator(majorLocator)
        ax[i].yaxis.set_minor_locator(minorLocator_y)
        ax[i].yaxis.set_minor_formatter(majorFormatter)
        ax[i].grid(True, which='major', color='grey', linestyle='dashed')
        ax[i].tick_params(which='both', labelsize=16)

    plt.xlabel('Время, мс', fontsize=fontsize)
    fig.subplots_adjust(hspace=0.6)
    matplotlib.pylab.xlim(0, count + 5)
    matplotlib.pylab.ylim(0, 5)
    fig.dpi = 150
    plt.savefig("plot.png")


print(f"Период моделирования: {interval / 1000} с")
print(f"Сгенерировано: {j} пакетов")
print(f"Передано: {N} пакетов")
print(f"Частота уничтожения пакетов: {X / N * 100:.2f}%")
print(f"Частота подключения ресурса: {H / interval * 100:.2f}%")
make_plot()
