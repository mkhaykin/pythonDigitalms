"""
Дан массив целых чисел nums и целое число target.
Необходимо вернуть индексы двух чисел таких, чтобы их сумма равна target.
Имеется ровно одно решение.
Один и тот же элемент нельзя использовать дважды.
Результат можно вернуть в любом порядке.

По памяти: O(n) - на словарь с дельтами.
По времени: O(n) - формирование словаря и один проход по исходным данным, поиск в словаре О(1)
"""


def solve(nums: list[int], target: int) -> list[int]:
    delta = {target - n: i for i, n in enumerate(nums)}
    for i, n in enumerate(nums):
        if n in delta and i != delta[n]:
            return [i, delta[n]]

    raise Exception("Ошибка входных")
