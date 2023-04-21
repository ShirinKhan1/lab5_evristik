import numpy as np
import pandas as pd
import random

M = 8
N = 3
T1 = 10
T2 = 20
O_count = 3
O = []
best_copy = 5
p_cros = 0.5
p_mut = 0.15
# M, N = int(input('M= ')), int(input('N= '))
# T1, T2 = int(input('Tmin= ')), int(input('Tmax= '))
# O_count = int(input('O_count = '))
# best_copy = int(input('кол-во повторений = '))
vector = np.array([10, 12, 16, 18, 17, 10, 13, 19])


# p_cros = int(input('p_cros = '))
# p_mut = int(input('p_mut = '))


def create_O():
    O_new = [random.randint(0, int(255 / O_count))]
    [O_new.append(random.randint(0, 255)) for _ in vector[1:]]
    O.append(O_new)


def print_O(d):
    # print(vector)
    for i in d:
        print(i)


[create_O() for _ in range(O_count)]
print(vector)
print_O(O)


# из генотипа в фенотип

def fenotype(genotype):
    f = {}
    start = 255 // O_count
    finish = 255
    step = 255 // O_count
    for j in range(start, finish, step):
        f[j] = []
    if len(f.keys()) < O_count:
        f[255] = []
    for i in range(len(genotype)):
        value = genotype[i]
        for j in list(f.keys()):
            if value <= j:
                f[j].append(vector[genotype.index(value)])
                break
    sum_f = []
    [sum_f.append(sum(f.get(i))) for i in f]
    return max(sum_f)


def cross(O_parrent, second=None):
    O_new = []
    i = random.randint(0, O_count - 1)
    if second is None:
        while O[i] == O_parrent:
            i = random.randint(0, O_count - 1)
        second = O[i]
    i = random.randint(1, M)
    for j in range(0, i):
        O_new.append(O_parrent[j])
    for j in range(i, M):
        O_new.append(second[j])
    return O_new, second


def mutation(O_cros):
    i = random.randint(0, M - 1)
    number = bin(O_cros[i])[2:]
    zeros = []
    [zeros.append(0) for _ in range(7 - len(number))]
    zeros = ''.join(map(str, zeros))
    number = zeros + number
    j = random.randint(0, len(number) - 1)
    number = list(number)
    number[j] = 1 if number[j] == 0 else 0
    number = ''.join(map(str, number))
    number = int(number, 2)
    O_cros[i] = number
    return O_cros


# mutation(O[0])

best_count = 0
best_individual = -1
# def minmax():
#     list_forminmax = []
#     [list_forminmax.append(fenotype(i)) for i in O]
#     best_minmax = max(list_forminmax) - min(list_forminmax)


while best_count < best_copy:
    # выбираем лучшую особь
    for cur in O:
        if best_individual == -1:
            best_individual = fenotype(cur)
        elif best_individual > fenotype(cur):
            best_individual = fenotype(cur)
    print(best_individual)
    print('=========================================================================================')
    new_O = []
    print('Данное поколоние ->')
    print_O(O)
    print()
    for cur, itearte in zip(O, range(1, len(O) + 1)):
        # index_cross = O.index(cur)
        # while index_cross == O.index(cur):
        #     index_cross = random.randint(0, len(O) - 1)
        # o_cross = O[index_cross]
        new_1, O_second = cross(cur)
        if random.random() < p_cros:
            new_1 = cur
        if random.random() > p_mut:
            new_1 = mutation(new_1)
        print(f"1-ый потомок -> {new_1}")
        new_2, _ = cross(O_second, cur)
        if random.random() < p_cros:
            new_2 = cur
        if random.random() > p_mut:
            new_2 = mutation(new_2)
        print(f"2-ый потомок -> {new_2}")
        dic = {
            fenotype(new_1): new_1,
            fenotype(new_2): new_2,
            fenotype(cur): cur
        }
        minmax = min([fenotype(new_1), fenotype(new_2), fenotype(cur)])
        print(f"\nидёт в новое поколение -> {dic[minmax]} - {minmax}\n"
              f"{itearte}----------------------------------------------------------------{itearte}")

        new_O.append(dic[minmax])
    O = new_O
    minmax = min([fenotype(O[0]), fenotype(O[1]), fenotype(O[2])])
    if best_individual <= minmax:
        best_count += 1
    else:
        best_count = 0

minmax = min([fenotype(O[0]), fenotype(O[1]), fenotype(O[2])])
dic = {
    fenotype(O[0]): O[0],
    fenotype(O[1]): O[1],
    fenotype(O[2]): O[2]
}
print(minmax)
print(dic[minmax])
