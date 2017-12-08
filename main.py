from random import randint
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

j = 0  # номер заявки
t = 0  # время
A = []  # [(j, i), ]  все заявки

while (t + x) <= interval:
    t += x
    j += 1
    A.append((j, t))
    x = randint(2, 8)

# REMOVE
#========================================
# import pickle
# pickle.dump(A, open("save4.p", "wb"))
# A = pickle.load(open("save3.p", "rb"))
# j = len(A)
# A_copy = list.copy(A)
#========================================

c1 = Channel(z)
c2 = Channel(z)
i = 0  # время

while i < interval:
    if N and X/N > b:
        c1.set_service_time(r)
        c2.set_service_time(r)
    else:
        c1.set_service_time(z)
        c2.set_service_time(z)

    if A and A[0][1] == i:
        c1.add(A[0])
        A.pop(0)

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

print(j, N, X, X/N, sep="; ")
