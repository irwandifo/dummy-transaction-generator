# Dummy Transaction Generator

Generates realistic synthetic transaction data for testing and development purposes.

## Features

- Generate realistic SME merchant transactions.
- Customize transaction details with various options.
- Simulate trend, seasonality, and random noise.
- Parquet output with date partitioning.
- Memory-efficient data generation.

## Installation

### Direct Installation

```bash
pip install git+https://github.com/irwandifo/dummy-transaction-generator.git
```

### Clone and Install

```bash
git clone https://github.com/irwandifo/dummy-transaction-generator.git
cd transaction-generator
pip install -e .
```

## Quick Start

```python
from transaction_generator import TransactionGenerator, TransactionPattern
from datetime import date

# Defines transaction pattern assumption
pattern = TransactionPattern(
    base_amount = 20_000,
    base_transaction = 80,
    trend_factor = 0.001, #0.1% daily increase
    max_weekend_factor = 1.5, #max 50% weekend increase
)

# Defines transaction generator config
generator = TransactionGenerator(
    start_date = date(2024, 10, 1),
    end_date = date(2024, 10, 2),
    num_merchants = 10_000,
    pattern = pattern
)

# Write to parquet
generator.write_to_parquet()
```


## Data Dictionary

| Column | Description | Example |
| --- | --- | --- |
| `transaction_id` | Unique identifer of the transaaction | c980a587-9ee2-4f40-82ab-28ae8309d870 |
| `merchant_id` | Unique identifer of the merchant | 1, 2, 3|
| `transaction_status` | Status of this transaction | completed, pending, failed |
| `transaction_type` | Order type of this transaction | dine_in, takeaway, delivery |
| `transaction_payment_method` | Payment method of this transaction | cash, card, qr_code, e_wallet |
| `transaction_amount` | Amount of sales for this transaction | 2000, 26050 |
| `transaction_datetime` | The timestamp when this transaction is created | 2024-10-01T00:00:00.000Z |