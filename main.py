"""Command-line interface for the Inventory Knapsack Optimizer."""
import argparse
import os

from inventory import fractional_knapsack, knapsack_01_dp, load_products
from inventory.benchmark import run_benchmark, save_chart, save_csv
from inventory.knapsack import greedy_01


def show(result):
    print(f"\n=== {result.method} ===")
    print(f"{'Product':<22}{'Weight':>8}{'Profit':>8}{'Taken':>8}")
    for p, frac in result.selected:
        taken = "100%" if frac == 1.0 else f"{frac * 100:.1f}%"
        print(f"{p.name:<22}{p.weight:>8}{p.profit:>8}{taken:>8}")
    print(f"Total profit : {result.total_profit:.2f}")
    print(f"Storage used : {result.total_weight:.2f} / {result.capacity} "
          f"({result.utilization:.1f}%)")


def cmd_solve(args):
    products = load_products(args.file)
    print(f"Loaded {len(products)} products, warehouse capacity = {args.capacity}")
    frac = fractional_knapsack(products, args.capacity)
    dp = knapsack_01_dp(products, args.capacity)
    whole = greedy_01(products, args.capacity)
    for r in (frac, whole, dp):
        show(r)
    print("\n=== Comparison ===")
    print(f"Fractional greedy (upper bound, items may be split): {frac.total_profit:.2f}")
    print(f"Greedy, whole items only                           : {whole.total_profit:.2f}")
    print(f"DP 0/1 (true optimum for whole items)              : {dp.total_profit:.2f}")
    gap = dp.total_profit - whole.total_profit
    if gap > 0:
        print(f"-> Plain greedy loses {gap:.0f} profit vs. DP on this input.")


def cmd_benchmark(args):
    rows = run_benchmark()
    print(f"{'items':>6}{'cap':>7}{'greedy ms':>12}{'dp ms':>12}"
          f"{'greedy $':>11}{'dp $':>9}")
    for r in rows:
        print(f"{r['items']:>6}{r['capacity']:>7}{r['greedy_ms']:>12.4f}"
              f"{r['dp_ms']:>12.4f}{r['greedy_profit']:>11.1f}{r['dp_profit']:>9}")
    os.makedirs("results", exist_ok=True)
    save_csv(rows, "results/benchmark.csv")
    print("\nSaved results/benchmark.csv")
    if save_chart(rows, "results/benchmark.png"):
        print("Saved results/benchmark.png")
    else:
        print("(Install matplotlib to also generate results/benchmark.png)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("solve", help="Select products for a given capacity")
    s.add_argument("--file", default="data/products.csv")
    s.add_argument("--capacity", type=int, default=50)
    s.set_defaults(func=cmd_solve)
    b = sub.add_parser("benchmark", help="Compare Greedy vs DP performance")
    b.set_defaults(func=cmd_benchmark)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
