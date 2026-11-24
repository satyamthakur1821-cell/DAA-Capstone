"""Data model and input helpers."""
import csv
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    weight: int   # storage units the product occupies
    profit: int   # profit earned if the product is stocked

    @property
    def ratio(self) -> float:
        """Profit per unit of storage (used by the greedy approach)."""
        return self.profit / self.weight


def load_products(path: str) -> list[Product]:
    """Load products from a CSV file with columns: name,weight,profit."""
    products = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            w, p = int(row["weight"]), int(row["profit"])
            if w <= 0 or p < 0:
                raise ValueError(f"Invalid weight/profit for '{row['name']}'")
            products.append(Product(row["name"].strip(), w, p))
    if not products:
        raise ValueError("No products found in file")
    return products


def generate_products(n: int, seed: int = 42) -> list[Product]:
    """Generate n random products (reproducible via seed) for benchmarking."""
    rng = random.Random(seed)
    return [Product(f"Item-{i + 1}", rng.randint(1, 50), rng.randint(10, 500))
            for i in range(n)]
