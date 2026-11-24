"""Performance comparison of Greedy vs DP across input sizes."""
import csv
import time

from .knapsack import fractional_knapsack, knapsack_01_dp
from .models import generate_products


def _time(fn, *args, repeats=3):
    best = float("inf")
    result = None
    for _ in range(repeats):
        t = time.perf_counter()
        result = fn(*args)
        best = min(best, time.perf_counter() - t)
    return result, best


def run_benchmark(sizes=(10, 50, 100, 200, 400), capacity_factor=10, seed=42):
    """Capacity scales with n so the DP table grows with the problem."""
    rows = []
    for n in sizes:
        products = generate_products(n, seed)
        cap = n * capacity_factor
        g, gt = _time(fractional_knapsack, products, cap)
        d, dt = _time(knapsack_01_dp, products, cap)
        rows.append({
            "items": n, "capacity": cap,
            "greedy_profit": round(g.total_profit, 2),
            "dp_profit": d.total_profit,
            "greedy_ms": round(gt * 1000, 4),
            "dp_ms": round(dt * 1000, 4),
            "greedy_util_%": round(g.utilization, 1),
            "dp_util_%": round(d.utilization, 1),
        })
    return rows


def save_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def save_chart(rows, path):
    """Optional: needs matplotlib. Silently skipped if unavailable."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    n = [r["items"] for r in rows]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(n, [r["greedy_ms"] for r in rows], "o-", label="Greedy")
    ax[0].plot(n, [r["dp_ms"] for r in rows], "s-", label="DP")
    ax[0].set(xlabel="Number of items", ylabel="Time (ms)", title="Execution time")
    ax[0].legend()
    ax[1].plot(n, [r["greedy_profit"] for r in rows], "o-", label="Greedy (fractional)")
    ax[1].plot(n, [r["dp_profit"] for r in rows], "s-", label="DP (0/1)")
    ax[1].set(xlabel="Number of items", ylabel="Total profit", title="Profit achieved")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return True
