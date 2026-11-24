import itertools
import unittest

from inventory import (Product, fractional_knapsack, generate_products,
                       knapsack_01_dp)
from inventory.knapsack import greedy_01


def brute_force(products, cap):
    best = 0
    for r in range(len(products) + 1):
        for combo in itertools.combinations(products, r):
            if sum(p.weight for p in combo) <= cap:
                best = max(best, sum(p.profit for p in combo))
    return best


class KnapsackTests(unittest.TestCase):
    def test_classic_example(self):
        items = [Product("A", 10, 60), Product("B", 20, 100), Product("C", 30, 120)]
        self.assertEqual(knapsack_01_dp(items, 50).total_profit, 220)
        self.assertAlmostEqual(fractional_knapsack(items, 50).total_profit, 240)

    def test_dp_matches_brute_force(self):
        for seed in range(15):
            items = generate_products(10, seed)
            cap = 60
            self.assertEqual(knapsack_01_dp(items, cap).total_profit,
                             brute_force(items, cap))

    def test_dp_selection_is_consistent(self):
        items = generate_products(20, 7)
        r = knapsack_01_dp(items, 100)
        self.assertEqual(sum(p.profit for p, _ in r.selected), r.total_profit)
        self.assertLessEqual(r.total_weight, 100)

    def test_fractional_is_upper_bound(self):
        for seed in range(15):
            items = generate_products(15, seed)
            self.assertGreaterEqual(fractional_knapsack(items, 80).total_profit + 1e-9,
                                    knapsack_01_dp(items, 80).total_profit)

    def test_greedy_whole_can_be_suboptimal(self):
        items = [Product("A", 1, 2), Product("B", 10, 15)]  # ratios 2.0, 1.5
        self.assertEqual(greedy_01(items, 10).total_profit, 2)
        self.assertEqual(knapsack_01_dp(items, 10).total_profit, 15)

    def test_edge_cases(self):
        items = [Product("A", 5, 10)]
        self.assertEqual(knapsack_01_dp(items, 0).total_profit, 0)
        self.assertEqual(knapsack_01_dp(items, 4).total_profit, 0)
        self.assertEqual(fractional_knapsack(items, 0).total_profit, 0)
        self.assertAlmostEqual(fractional_knapsack(items, 4).total_profit, 8)


if __name__ == "__main__":
    unittest.main()
