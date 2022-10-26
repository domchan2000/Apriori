import sys
import time
import tracemalloc

import numpy as np


def createC1(path):
    res = []
    num = 0
    basket_size = 0
    with open(path, 'r') as data:
        for lines in data:
            basket = lines.strip().split(' ')
            basket = list(map(int, basket))
            basket_size += 1
            for item in basket:
                if not res:
                    res.insert(item, 1)
                    num += 1
                elif item >= num:
                    res.insert(item, 1)
                    num += 1
                elif item < num:
                    res[item] += 1
    return res, basket_size


def createL1(C1, minsup, length):
    L1_item = []
    item_occ = []
    l = len(C1)
    for item in range(0, l):
        if C1[item] / length >= minsup:
            L1_item.append(item)
            item_occ.append(C1[item])
    return L1_item, item_occ


def createC2_v4(keys, path):
    keys = list(keys)
    M_size = len(keys)
    C2 = np.zeros([M_size, M_size], dtype=int)
    with open(path, 'r') as data:
        for lines in data:
            basket = lines.strip().split(' ')
            basket = set(map(int, basket))
            for i in range(M_size):
                if keys[i] in basket:
                    for j in range(i + 1, M_size):
                        temp = {keys[i], keys[j]}
                        if temp.issubset(basket):
                            C2[j][i] += 1
    return C2


def createL2_v2(C2, L1_item, minsup, length):
    keys2_f = []
    L2_count = []
    for row in range(len(C2)):
        for col in range(row + 1, len(C2)):
            occ = C2[col][row]
            if occ / length >= minsup:
                keys2_f.append([L1_item[row], L1_item[col]])
                L2_count.append(occ)
    return keys2_f, L2_count


def print_table(L):
    print("itemset | Frequency")
    for i in range(len(L)):
        print("{} : {}".format(i, L[i]))
    print("\n\n")


tracemalloc.start()
start = time.time()
path = 'retail.dat.txt'
print('reading data')
C1, size = createC1(path)
# print(C1)
# print("C1 : ")
# print_table(C1)
# print(size)
minsup = 0.01
L1_item, L1_itemcount = createL1(C1, minsup, size)
# print(L1_item)
# print(L1_itemcount)
# print("itemset | Frequency")
# for i in range(len(L1_item)):
#     print("{} : {}".format(L1_item[i], L1_itemcount[i]))
# print("\n\n")
# print(sys.getsizeof(L1_item)+sys.getsizeof(L1_itemcount))
C2 = createC2_v4(L1_item, path)
# np.set_printoptions(threshold=sys.maxsize)
# print(C2)
# print(sys.getsizeof(C2))
# print("C2:")
# print("itemset | Frequency")
# for i in range(len(C2)):
#     for j in range(i + 1, len(C2)):
#         print("{} : {}".format([L1_item[i], L1_item[j]], C2[j][i]))
# print(sys.getsizeof(C2))
L2_item, L2_itemcount = createL2_v2(C2, L1_item, minsup, size)
print("L2:")
print("itemset | Frequency")
for i in range(len(L2_item)):
    print("{} : {}".format(L2_item[i], L2_itemcount[i]))
print("\n\n")
end = time.time()
print(end - start)

print("C1:")
print(sys.getsizeof(C1))

print("L1:")
print(sys.getsizeof(L1_item) + sys.getsizeof(L1_itemcount))

print('C2')
print(sys.getsizeof(C2))

print("L2:")
print(sys.getsizeof(L2_item) + sys.getsizeof(L2_itemcount))

print("Traced memory:")
print(tracemalloc.get_traced_memory())
