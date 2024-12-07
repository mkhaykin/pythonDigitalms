from tasks.task1 import solve

assert sorted(solve([2, 7, 11, 15], 9)) == [0, 1]
assert sorted(solve([3, 2, 4], 6)) == [1, 2]
assert sorted(solve([3, 3], 6)) == [0, 1]
assert sorted(solve([-3, -2, -1, 3], 0)) == [0, 3]
