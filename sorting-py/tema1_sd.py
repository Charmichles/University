import random
import time


def randomlist(size, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(size)]


def bubblesort(arr):
    for i in range(len(arr)):
        pair_swapped = False
        for j in range(len(arr) - 1 - i):  # la fiecare trecere, cel putin un element ajunge in pozitia corecta
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                pair_swapped = True
        if not pair_swapped:  # daca nu se efectueaza nici o schimbare atunci vectorul este sortat
            break
    return arr


def countsort(arr):
    min_val, max_val = arr[0], arr[0]
    for num in arr:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num
    appearances_plus = [0 for _ in range(max_val + 1)]
    appearances_neg = [0 for _ in range(abs(min_val) + 1)]
    for num in arr:
        if num < 0:
            appearances_neg[abs(num)] += 1
        else:
            appearances_plus[num] += 1
    sorted_arr = []
    idx = len(appearances_neg) - 1
    while idx >= 0:
        for _ in range(appearances_neg[idx]):
            sorted_arr.append((-1) * idx)
        idx -= 1
    for num, freq in enumerate(appearances_plus):
        for _ in range(freq):
            sorted_arr.append(num)
    return sorted_arr


def radixsort(arr, dom=1):
    buckets = [[] for _ in range(10)]
    for num in arr:
        buckets[(abs(num) // dom) % 10].append(num)
    if len(arr) == len(buckets[0]):  # toate cifrele au fost folosite, deci vectorul este sortat
        negatives, positives = [], []
        for num in arr:
            if num >= 0:
                positives.append(num)
            else:
                negatives.append(num)
        negatives.reverse()
        return negatives + positives
    next_arr = [num for bucket in buckets for num in bucket]
    return radixsort(next_arr, dom * 10)


def mergesort(arr):
    def mergelists(list1, list2):
        i, j = 0, 0
        list3 = []
        while i < len(list1) and j < len(list2):
            if list1[i] <= list2[j]:
                list3.append(list1[i])
                i += 1
            else:
                list3.append(list2[j])
                j += 1
        list3.extend(list1[i:])
        list3.extend(list2[j:])
        return list3
    if len(arr) < 20:
        return bubblesort(arr)
    mid = len(arr) // 2
    left_arr = mergesort(arr[:mid])
    right_arr = mergesort(arr[mid:])
    return mergelists(left_arr, right_arr)


def quicksort(arr):
    if len(arr) < 20:
        return bubblesort(arr)
    piv = (random.choice(arr) + random.choice(arr) + random.choice(arr)) // 3
    lesser, equal, greater = [], [], []
    for num in arr:
        if num == piv:
            equal.append(num)
        elif num < piv:
            lesser.append(num)
        else:
            greater.append(num)
    return quicksort(lesser) + equal + quicksort(greater)


def test(arr, sort_funcs):
    def issorted(vec):
        if type(vec) != list:
            return vec
        for i in range(1, len(vec)):
            if vec[i] < vec[i - 1]:
                return "Array is not sorted"
        return "Array is sorted"
    out_file_time = open("test_output_time.txt", 'w')
    out_file_arr = open("test_output_arr.txt", 'w')
    out_file_arr.write("".join([str(num) + ' ' for num in arr]) + '\n')
    for sort in sort_funcs:
        st = time.time()
        res = sort[0](arr)
        et = time.time()
        out_file_time.write("{} ran for {} seconds. {}.".format(sort[1], et - st, issorted(res)) + '\n')
    out_file_arr.close()
    out_file_time.close()


sorts = [(mergesort, "Mergesort"), (quicksort, "Quicksort"), (radixsort, "Radixsort"), (countsort, "Countsort"), (sorted, "Python's standard sort")]

in_file = open("test_output_arr.txt", 'r')
test_arr = randomlist(10 ** 6, (-1) * 10 ** 4, 10 ** 4)
test(test_arr, sorts)
#test(list(map(int, in_file.read().split())), sorts)
in_file.close()
