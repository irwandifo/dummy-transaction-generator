# Dummy Transaction Generator

Generates realistic synthetic transaction data for testing and development purposes.

## Features

- Generate realistic SME merchant transactions.
- Customize transaction details with various options.
- Simulate trend, seasonality, and random noise.
- Parquet output with date partitioning.
- Memory-efficient generation.

## Data Dictionary

| Column | Description | Example |
| --- | --- | --- |
| `transaction_id` | Unique identifer of the transaaction | c980a587-9ee2-4f40-82ab-28ae8309d870 |
| `merchant_id` | Unique identifer of the merchant | 1, 2, 3 , etc |
| `transaction_status` | Status of this transaction | completed, pending, failed |
| `transaction_type` | Order type of this transaction | dine_in, takeaway, delivery |
| `transaction_payment_method` | Payment method of this transaction | cash, card, qr_code, e_wallet |
| `transaction_amount` | Amount of sales for this transaction | 2000, 26050, etc |
| `transaction_datetime` | The timestamp when this transaction is created | 2024-10-01T00:00:00.000Z |