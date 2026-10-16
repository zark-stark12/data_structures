"""
Unit tests for assignment1: correctness checks plus empirical O(n) / O(n + k)
timing checks.

How the timing checks work
--------------------------
For each function we time it at three input sizes, each 10x the last
(SIZES). If the running time is ~ n^p, then

    p = log(t_big / t_small) / log(n_big / n_small)

An O(n) function gives p ~ 1. An O(n log n) function gives p slightly above 1,
and O(n^2) gives p ~ 2. We assert p < MAX_EXPONENT, which leaves headroom for
timer noise while still failing a quadratic implementation.

count_sort is checked twice: grow n with k fixed, then grow k with n fixed.
"""
import math
import random
import timeit
import unittest

from static_array import StaticArray
from assignment1 import (
    min_max,
    reverse,
    remove_duplicates,
    rotate,
    is_sorted,
    count_sort,
    sorted_squares,
)

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
SEED = 123
SIZES = (2_000, 20_000, 200_000, 2_000_000, 20_000_000)       # each step is 10x; 1e8 is not feasible
VALUE_LO, VALUE_HI = -10_000_000, 10_000_000   # negatives exercise the offset logic
MAX_EXPONENT = 1.4                     # O(n) -> ~1.0, O(n^2) -> ~2.0
TIMER_REPEAT = 5                       # we take the min of these
TIMER_NUMBER = 3                       # calls per repeat

# Assumption from your test: count_sort returns NON-ASCENDING order.
# Flip to False if your spec says ascending.
COUNT_SORT_DESCENDING = True


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def to_static(values):
    """list -> StaticArray"""
    arr = StaticArray(len(values))
    for i, v in enumerate(values):
        arr.set(i, v)
    return arr


def to_list(arr):
    """StaticArray -> list"""
    return [arr.get(i) for i in range(arr.length())]


def best_time(func, arg):
    """Per-call time in seconds: min over several repeats to cut noise."""
    timer = timeit.Timer(lambda: func(arg))
    return min(timer.repeat(repeat=TIMER_REPEAT, number=TIMER_NUMBER)) / TIMER_NUMBER


def growth_exponent(n_small, t_small, n_big, t_big):
    return math.log(t_big / t_small) / math.log(n_big / n_small)


class TestOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rng = random.Random(SEED)   # local RNG so test order doesn't matter

    # ---- data builders ------------------------------------------------------
    def rand_list(self, n, lo=VALUE_LO, hi=VALUE_HI):
        return [self.rng.randint(lo, hi) for _ in range(n)]

    def unique_list(self, n):
        # random.sample needs population >= k, so widen the range with n
        return self.rng.sample(range(-n, 2 * n), n)

    # ---- generic timing assertion ----------------------------------------
    def assert_linear(self, func, make_arg, label, sizes=SIZES):
        """
        make_arg(n) -> argument for func (a StaticArray, or a tuple if you
        wrap func in a lambda). Arguments are built OUTSIDE the timed region.
        """
        times = []
        for n in sizes:
            arg = make_arg(n)
            times.append(best_time(func, arg))

        steps = []
        for i in range(len(sizes) - 1):
            p = growth_exponent(sizes[i], times[i], sizes[i + 1], times[i + 1])
            steps.append(f"n={sizes[i]}->{sizes[i + 1]}: p={p:.2f}")

        overall = growth_exponent(sizes[0], times[0], sizes[-1], times[-1])
        msg = (f"{label}: overall exponent {overall:.2f} "
               f"(limit {MAX_EXPONENT}); " + "; ".join(steps) +
               f"; times={['%.4fs' % t for t in times]}")
        print("\n" + msg)
        self.assertLess(overall, MAX_EXPONENT, msg)

    # ========================================================================
    # min_max
    # ========================================================================
    def test_min_max_correctness(self):
        cases = [
            [7],                                   # single element
            [3, 3, 3, 3],                          # all equal
            [5, 1, 2, 1, 5, 4],                    # small, with repeats
            self.rand_list(10),
            self.rand_list(1_000),
            self.rand_list(1_000, -50, -1),        # all negative
        ]
        for values in cases:
            with self.subTest(n=len(values)):
                lo, hi = min_max(to_static(values))
                self.assertEqual(lo, min(values))
                self.assertEqual(hi, max(values))   # max, not min

    def test_min_max_is_linear(self):
        self.assert_linear(
            min_max, lambda n: to_static(self.rand_list(n)), "min_max")

    # ========================================================================
    # reverse  (assumes in-place; if yours returns a new array, change the
    # `to_list(arr)` below to `to_list(reverse(arr))`)
    # ========================================================================
    def test_reverse_correctness(self):
        for n in (1, 2, 3, 10, 999, 1_000):
            with self.subTest(n=n):
                values = self.rand_list(n)
                arr = to_static(values)
                reverse(arr)
                self.assertEqual(to_list(arr), values[::-1])

    def test_reverse_is_linear(self):
        self.assert_linear(
            reverse, lambda n: to_static(self.rand_list(n)), "reverse")

    # ========================================================================
    # rotate(arr, steps)  (assumes in-place; positive = rotate right)
    # ========================================================================
    @staticmethod
    def expected_rotation(values, steps):
        n = len(values)
        r = steps % n                      # Python's % handles negatives
        return values[n - r:] + values[:n - r]

    # def test_rotate_correctness(self):
    #     values = self.rand_list(10)
    #     n = len(values)
    #     for steps in (0, 1, 3, -1, -3, n, n + 2, -(n + 2), 10 ** 9, -(10 ** 9)):
    #         with self.subTest(steps=steps):
    #             arr = to_static(values)
    #             rotate(arr, steps)
    #             self.assertEqual(to_list(arr), self.expected_rotation(values, steps))

    def test_rotate_is_linear(self):
        # normal step count
        self.assert_linear(
            lambda args: rotate(*args),
            lambda n: (to_static(self.rand_list(n)), n // 3),
            "rotate (steps = n/3)")

    def test_rotate_huge_steps_is_linear(self):
        # steps must not make the work depend on the step count
        self.assert_linear(
            lambda args: rotate(*args),
            lambda n: (to_static(self.rand_list(n)), 10 ** 9),
            "rotate (steps = 1e9)")

    # ========================================================================
    # is_sorted  (assumes 1 = strictly ascending, 2 = strictly descending,
    # 0 = neither. Adjust the expected values if your spec differs, especially
    # for arrays with duplicates.)
    # ========================================================================
    def test_is_sorted_correctness(self):
        uniq = self.unique_list(500)
        self.assertEqual(is_sorted(to_static(sorted(uniq))), 1)
        self.assertEqual(is_sorted(to_static(sorted(uniq, reverse=True))), -1)
        self.assertEqual(is_sorted(to_static(uniq)), 0)
        self.assertEqual(is_sorted(to_static([42])), 1)     # single element
        # one swap from ascending is "neither"
        almost = sorted(uniq)
        almost[10], almost[11] = almost[11], almost[10]
        self.assertEqual(is_sorted(to_static(almost)), 0)

    def test_is_sorted_is_linear(self):
        # WORST CASE input: an already-sorted array forces a full scan.
        # A random array exits early and would measure almost nothing.
        self.assert_linear(
            is_sorted,
            lambda n: to_static(sorted(self.unique_list(n))),
            "is_sorted (worst case: fully sorted)")

    # ========================================================================
    # remove_duplicates  (input must be sorted)
    # ========================================================================
    def test_remove_duplicates_correctness(self):
        cases = [
            [1],
            [2, 2, 2, 2],
            [1, 1, 2, 3, 3, 3, 4],
            sorted(self.rand_list(1_000, 0, 100)),     # heavy duplication
            sorted(self.unique_list(500)),             # no duplicates
        ]
        for values in cases:
            with self.subTest(n=len(values)):
                result = remove_duplicates(to_static(values))
                self.assertEqual(to_list(result), sorted(set(values)))

    def test_remove_duplicates_is_linear(self):
        self.assert_linear(
            remove_duplicates,
            lambda n: to_static(sorted(self.rand_list(n, 0, n // 4))),
            "remove_duplicates")

    # ========================================================================
    # count_sort  -> O(n + k), where k = max - min + 1
    # ========================================================================
    def expected_sort(self, values):
        return sorted(values, reverse=COUNT_SORT_DESCENDING)

    def test_count_sort_correctness(self):
        cases = [
            [5],
            [5, 1, 2, 1, 5, 4],
            self.rand_list(10),
            self.rand_list(1_000),
            self.rand_list(1_000, -20, 20),            # many duplicates
            [-5, -5, -1, -9],                          # all negative
            [3, 3, 3],                                 # k == 1
        ]
        for values in cases:
            with self.subTest(n=len(values)):
                arr = to_static(values)
                original = to_list(arr)
                result = count_sort(arr)
                self.assertEqual(to_list(result), self.expected_sort(values))
                self.assertEqual(to_list(arr), original)   # input untouched
                                                           # (delete if in place)

    def test_count_sort_is_linear_in_n_with_k_fixed(self):
        # k fixed at 1,000: values always in [0, 999]
        self.assert_linear(
            count_sort,
            lambda n: to_static(self.rand_list(n, 0, 999)),
            "count_sort (n grows, k = 1000)")

    def test_count_sort_is_linear_in_k_with_n_fixed(self):
        # n fixed at 1,000; the range k grows. We pin the min and max so the
        # range really is k. Time should track k (the O(k) passes dominate).
        n_fixed = 1_000
        ks = (10_000, 100_000, 400_000)

        def make_arg(k):
            values = self.rand_list(n_fixed, 0, k - 1)
            values[0], values[1] = 0, k - 1
            return to_static(values)

        self.assert_linear(count_sort, make_arg, "count_sort (k grows, n = 1000)",
                           sizes=ks)

    # ========================================================================
    # sorted_squares  (input sorted non-descending, may contain negatives;
    # output sorted non-descending)
    # ========================================================================
    def test_sorted_squares_correctness(self):
        cases = [
            [3],
            [-3],
            [-4, -1, 0, 3, 10],
            [-7, -3, 2, 3, 11],
            sorted(self.rand_list(1_000)),
            sorted(self.rand_list(1_000, -100, -1)),   # all negative
            sorted(self.rand_list(1_000, 0, 100)),     # all non-negative
        ]
        for values in cases:
            with self.subTest(n=len(values)):
                result = sorted_squares(to_static(values))
                self.assertEqual(to_list(result), sorted(v * v for v in values))

    def test_sorted_squares_is_linear(self):
        # The correct approach is a two-pointer merge, O(n). Squaring and then
        # sorting would be O(n log n) and may edge toward the exponent limit.
        self.assert_linear(
            sorted_squares,
            lambda n: to_static(sorted(self.rand_list(n))),
            "sorted_squares")


if __name__ == "__main__":
    unittest.main(verbosity=2)