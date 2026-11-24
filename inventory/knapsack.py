"""Greedy (Fractional) and Dynamic Programming (0/1) knapsack solvers."""
from dataclasses import dataclass, field

from .models import Product


@dataclass
class KnapsackResult:
    method: str
    total_profit: float
    total_weight: float
    capacity: int
    # (product, fraction_taken) -- fraction is 1.0 for whole items
    selected: list[tuple[Product, float]] = field(default_factory=list)

    @property
    def utilization(self) -> float:
        return 100.0 * self.total_weight / self.capacity if self.capacity else 0.0


def fractional_knapsack(products: list[Product], capacity: int) -> KnapsackResult:
    """Greedy: take items by best profit/weight ratio, splitting the last one.

    Time: O(n log n) (sorting).  Space: O(n).
    Optimal for the *fractional* problem; an upper bound for 0/1.
    """
    remaining = capacity
    profit = weight = 0.0
    chosen = []
    for p in sorted(products, key=lambda x: x.ratio, reverse=True):
        if remaining <= 0:
            break
        if p.weight <= remaining:
            chosen.append((p, 1.0))
            remaining -= p.weight
            profit += p.profit
            weight += p.weight
        else:
            frac = remaining / p.weight
            chosen.append((p, frac))
            profit += p.profit * frac
            weight += remaining
            remaining = 0
    return KnapsackResult("Greedy (Fractional)", profit, weight, capacity, chosen)


def knapsack_01_dp(products: list[Product], capacity: int) -> KnapsackResult:
    """Dynamic programming 0/1 knapsack with item reconstruction.

    dp[i][w] = best profit using the first i items with capacity w.
    Time: O(n * W).  Space: O(n * W) (full table kept to backtrack).
    """
    n = len(products)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, pr = products[i - 1].weight, products[i - 1].profit
        row, prev = dp[i], dp[i - 1]
        for w in range(capacity + 1):
            row[w] = prev[w]
            if wt <= w and prev[w - wt] + pr > row[w]:
                row[w] = prev[w - wt] + pr

    # Backtrack to find which items were picked
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append((products[i - 1], 1.0))
            w -= products[i - 1].weight
    chosen.reverse()
    total_w = sum(p.weight for p, _ in chosen)
    return KnapsackResult("Dynamic Programming (0/1)", dp[n][capacity],
                          total_w, capacity, chosen)


def greedy_01(products: list[Product], capacity: int) -> KnapsackResult:
    """Greedy by ratio but WITHOUT splitting items (shows why greedy fails 0/1)."""
    remaining, profit, weight, chosen = capacity, 0, 0, []
    for p in sorted(products, key=lambda x: x.ratio, reverse=True):
        if p.weight <= remaining:
            chosen.append((p, 1.0))
            remaining -= p.weight
            profit += p.profit
            weight += p.weight
    return KnapsackResult("Greedy (whole items only)", profit, weight, capacity, chosen)
