"""
Вы продукт-менеджер и в настоящее время возглавляете команду по разработке нового продукта.
К сожалению, последняя версия вашего продукта не прошла проверку качества.
Поскольку каждая версия разрабатывается на основе предыдущей версии,
все версии после сломанной версии тоже сломаны.
Предположим, у вас есть n версий [1, 2, ..., n] и вы хотите найти первую сломанную версию,
из-за которой все последующие будут сломаны.
Вам предоставляется bool API isBrokenVersion (версия), который возвращает,
является ли версия сломанной. Реализуйте функцию для поиска первой сломанной версии.
Вы должны свести к минимуму количество обращений к API.
"""

from is_broken import isBrokenVersion


def solve(n: int) -> int:
    li = 1
    ri = n
    while ri > li:
        mi = (li + ri) // 2
        if isBrokenVersion(mi):
            ri = mi
        else:
            li = mi + 1
    return li
