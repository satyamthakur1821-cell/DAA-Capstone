# Intelligent Inventory Management Using Knapsack Optimization

A warehouse manager has limited storage space and many candidate products, each with a
**weight** (storage units) and a **profit**. This project selects the products that
**maximize total profit without exceeding the storage capacity**, using two approaches
and comparing them:

| Approach | Problem solved | Technique |
|---|---|---|
| Greedy | Fractional Knapsack (items can be split) | Sort by profit/weight ratio |
| Dynamic Programming | 0/1 Knapsack (items taken whole or not at all) | Bottom-up DP table + backtracking |

A third helper, *greedy with whole items only*, shows why plain greedy is **not** optimal for 0/1.

## Project structure

```
inventory-knapsack/
├── main.py                  # CLI: solve + benchmark
├── inventory/
│   ├── models.py            # Product, CSV loader, random data generator
│   ├── knapsack.py          # Greedy + DP algorithms
│   └── benchmark.py         # Timing, CSV and chart output
├── data/products.csv        # Sample inventory (12 products)
├── tests/test_knapsack.py   # Unit tests (incl. brute-force verification)
└── results/                 # benchmark.csv / benchmark.png
```

## How to run

Requires Python 3.9+. No dependencies are needed (matplotlib is optional, for the chart).

```bash
python main.py solve --capacity 27          # choose products for capacity 27
python main.py solve --file my.csv --capacity 100
python main.py benchmark                    # Greedy vs DP across input sizes
python -m unittest discover -s tests -v     # run tests
```

Input CSV format: `name,weight,profit` (weights are positive integers).

## Algorithms

### 1. Greedy – Fractional Knapsack
1. Compute ratio = profit / weight for each product.
2. Sort by ratio, descending.
3. Take whole items while they fit; take a fraction of the next item to fill the rest.

* **Time:** O(n log n) **Space:** O(n)
* **Optimal** for the fractional problem. For 0/1 it is only an **upper bound**.

### 2. Dynamic Programming – 0/1 Knapsack
`dp[i][w]` = best profit using the first `i` products with capacity `w`.

```
dp[i][w] = dp[i-1][w]                                   if weight_i > w
         = max(dp[i-1][w], dp[i-1][w - weight_i] + profit_i)   otherwise
```
The chosen products are recovered by backtracking through the table.

* **Time:** O(n · W) **Space:** O(n · W) (W = capacity). Pseudo-polynomial.
* **Optimal** for 0/1.

## Sample output (`--capacity 27`)

| Method | Total profit |
|---|---|
| Fractional greedy (upper bound) | 225.00 |
| Greedy, whole items only | 207 |
| **DP 0/1 (optimal)** | **222** |

Plain greedy loses 15 profit here because it commits to high-ratio items that leave
unusable gaps. DP finds the true best combination.

## Benchmark results

Random products (weight 1–50, profit 10–500), capacity = 10 × n, best of 3 runs:

| Items | Capacity | Greedy (ms) | DP (ms) | Greedy profit | DP profit |
|---|---|---|---|---|---|
| 10 | 100 | 0.0024 | 0.0702 | 1219.6 | 1150 |
| 50 | 500 | 0.0076 | 1.6181 | 9473.8 | 9463 |
| 100 | 1000 | 0.0150 | 7.6491 | 17317.8 | 17312 |
| 200 | 2000 | 0.0288 | 30.3137 | 34207.7 | 34205 |
| 400 | 4000 | 0.0671 | 126.6249 | 72244.5 | 72240 |

(Timings vary by machine; run `python main.py benchmark` to reproduce. See `results/benchmark.png`.)

### Observations
* **Speed:** Greedy grows roughly as n log n; DP grows with n × W, so it is far slower (about 1,900× at n = 400).
* **Profit:** Fractional greedy is always ≥ DP, since splitting items relaxes the problem. The gap is small for large inventories.
* **Whole items:** If products cannot be split (the usual warehouse case), DP is the correct choice. Greedy on whole items is fast but can be suboptimal.
* **Memory:** DP needs an n × W table. A 1-D rolling array cuts this to O(W), but then reconstructing the chosen items needs extra work.

## When to use which
* Products can be split or sold in bulk (grain, liquids): **Greedy**.
* Indivisible products (laptops, crates): **DP 0/1**.
* Huge capacity values: DP's O(n·W) becomes costly; consider approximation or branch and bound.

## Testing
Tests check the classic textbook case, DP against brute force on random inputs,
selection consistency, greedy ≥ DP, a case where whole-item greedy fails, and edge cases
(zero capacity, items too heavy).
