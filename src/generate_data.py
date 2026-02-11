"""
Sales Data Generator
Generates realistic sample sales data for the Sales Insights project.
Creates 4 CSV files: customers, products, markets, and sales_transactions.
"""

import csv
import random
import os
from datetime import datetime, timedelta

# Seed for reproducibility
random.seed(42)

# Output directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def generate_customers():
    """Generate 50 customer records."""
    customer_types = ["Brick & Mortar", "E-Commerce"]
    company_prefixes = [
        "Atlas", "Beacon", "Crest", "Delta", "Eagle", "Frontier", "Global",
        "Harbor", "Infinity", "Jade", "Keystone", "Liberty", "Metro",
        "Noble", "Omega", "Pioneer", "Quest", "Ridge", "Summit", "Titan",
        "Unity", "Valor", "Western", "Apex", "Bright", "Crown", "Drake",
        "Elite", "Falcon", "Grand", "Horizon", "Icon", "Jupiter", "Kingsway",
        "Landmark", "Maple", "Nexus", "Orbit", "Prime", "Royal", "Silver",
        "Terra", "Urban", "Vista", "Zenith", "Ace", "Bold", "Core", "Dune", "Echo"
    ]
    company_suffixes = [
        "Electronics", "Stores", "Mart", "Retail", "Trading Co.", "Supplies",
        "Distributors", "Enterprises", "Solutions", "Market"
    ]

    customers = []
    for i in range(50):
        code = f"CUS{str(i + 1).zfill(3)}"
        name = f"{company_prefixes[i]} {random.choice(company_suffixes)}"
        ctype = random.choices(customer_types, weights=[65, 35])[0]
        customers.append([code, name, ctype])

    filepath = os.path.join(DATA_DIR, "customers.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_code", "customer_name", "customer_type"])
        writer.writerows(customers)

    print(f"Generated {len(customers)} customers -> {filepath}")
    return customers


def generate_products():
    """Generate 20 product records."""
    products_data = [
        ("PRD001", "USB-C Charging Cable", "Own Brand"),
        ("PRD002", "Wireless Mouse", "Own Brand"),
        ("PRD003", "Bluetooth Speaker", "Distribution"),
        ("PRD004", "LED Desk Lamp", "Own Brand"),
        ("PRD005", "Phone Screen Protector", "Distribution"),
        ("PRD006", "Laptop Stand", "Own Brand"),
        ("PRD007", "Portable Power Bank", "Distribution"),
        ("PRD008", "HDMI Cable 6ft", "Own Brand"),
        ("PRD009", "Webcam HD 1080p", "Distribution"),
        ("PRD010", "Keyboard Wrist Rest", "Own Brand"),
        ("PRD011", "Ethernet Adapter", "Own Brand"),
        ("PRD012", "Wireless Earbuds", "Distribution"),
        ("PRD013", "Monitor Riser", "Own Brand"),
        ("PRD014", "USB Hub 4-Port", "Own Brand"),
        ("PRD015", "Smart Plug", "Distribution"),
        ("PRD016", "Cable Management Kit", "Own Brand"),
        ("PRD017", "Noise Cancelling Headphones", "Distribution"),
        ("PRD018", "Surge Protector", "Own Brand"),
        ("PRD019", "Tablet Stand", "Distribution"),
        ("PRD020", "External SSD 500GB", "Distribution"),
    ]

    filepath = os.path.join(DATA_DIR, "products.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_code", "product_name", "product_type"])
        writer.writerows(products_data)

    print(f"Generated {len(products_data)} products -> {filepath}")
    return products_data


def generate_markets():
    """Generate 10 market records."""
    markets_data = [
        ("MKT001", "New York", "East"),
        ("MKT002", "Los Angeles", "West"),
        ("MKT003", "Chicago", "Central"),
        ("MKT004", "Houston", "South"),
        ("MKT005", "Phoenix", "West"),
        ("MKT006", "Philadelphia", "East"),
        ("MKT007", "Dallas", "South"),
        ("MKT008", "Atlanta", "South"),
        ("MKT009", "Seattle", "West"),
        ("MKT010", "Denver", "Central"),
    ]

    filepath = os.path.join(DATA_DIR, "markets.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["market_code", "market_name", "zone"])
        writer.writerows(markets_data)

    print(f"Generated {len(markets_data)} markets -> {filepath}")
    return markets_data


def generate_transactions(customers, products, markets):
    """Generate ~5000 sales transactions from 2019 to 2023."""

    # Base prices for each product (used to calculate sales_amount)
    base_prices = {
        "PRD001": 12.99, "PRD002": 24.99, "PRD003": 49.99, "PRD004": 34.99,
        "PRD005": 8.99, "PRD006": 44.99, "PRD007": 29.99, "PRD008": 9.99,
        "PRD009": 59.99, "PRD010": 19.99, "PRD011": 14.99, "PRD012": 39.99,
        "PRD013": 54.99, "PRD014": 22.99, "PRD015": 24.99, "PRD016": 16.99,
        "PRD017": 89.99, "PRD018": 27.99, "PRD019": 32.99, "PRD020": 69.99,
    }

    # Cost multipliers (cost as fraction of price) by product type
    cost_multipliers = {"Own Brand": 0.45, "Distribution": 0.65}

    # Seasonal weights (index 0 = Jan, 11 = Dec)
    seasonal_weights = [0.7, 0.6, 0.8, 0.85, 0.9, 1.0, 0.95, 0.9, 1.0, 1.1, 1.3, 1.5]

    # Year-over-year growth factors
    year_growth = {2019: 1.0, 2020: 0.85, 2021: 1.1, 2022: 1.25, 2023: 1.35}

    # Market weights (some markets have more activity)
    market_weights = [20, 18, 15, 12, 8, 10, 11, 9, 7, 5]

    # Top customers get more transactions
    customer_weights = [max(1, 10 - i // 5) for i in range(len(customers))]

    start_date = datetime(2019, 1, 1)
    end_date = datetime(2023, 12, 31)
    total_days = (end_date - start_date).days

    transactions = []
    transaction_id = 1

    for _ in range(5000):
        # Random date
        rand_day = random.randint(0, total_days)
        date = start_date + timedelta(days=rand_day)

        year = date.year
        month = date.month

        # Apply seasonal and yearly factors to decide if transaction happens
        seasonal_factor = seasonal_weights[month - 1]
        yearly_factor = year_growth[year]

        # Random customer, product, market (weighted)
        customer = random.choices(customers, weights=customer_weights)[0]
        product = random.choices(products)[0]
        market = random.choices(markets, weights=market_weights)[0]

        product_code = product[0]
        product_type = product[2]

        # Quantity influenced by seasonal and yearly factors
        base_qty = random.randint(1, 25)
        quantity = max(1, int(base_qty * seasonal_factor * yearly_factor))

        # Price with slight random variation (+/- 10%)
        base_price = base_prices[product_code]
        price_variation = random.uniform(0.90, 1.10)
        unit_price = round(base_price * price_variation, 2)

        sales_amount = round(unit_price * quantity, 2)
        cost_price = round(unit_price * cost_multipliers[product_type] * quantity, 2)
        profit = round(sales_amount - cost_price, 2)

        transactions.append([
            f"TXN{str(transaction_id).zfill(5)}",
            date.strftime("%Y-%m-%d"),
            customer[0],
            product_code,
            market[0],
            quantity,
            sales_amount,
            cost_price,
            profit
        ])
        transaction_id += 1

    # Sort by date
    transactions.sort(key=lambda x: x[1])

    filepath = os.path.join(DATA_DIR, "sales_transactions.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "transaction_id", "date", "customer_code", "product_code",
            "market_code", "quantity", "sales_amount", "cost_price", "profit"
        ])
        writer.writerows(transactions)

    print(f"Generated {len(transactions)} transactions -> {filepath}")
    return transactions


if __name__ == "__main__":
    print("=" * 50)
    print("Sales Data Generator")
    print("=" * 50)

    customers = generate_customers()
    products = generate_products()
    markets = generate_markets()
    transactions = generate_transactions(customers, products, markets)

    print("=" * 50)
    print("Data generation complete!")
    print(f"Files saved to: {DATA_DIR}")
