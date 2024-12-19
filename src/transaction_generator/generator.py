import polars as pl
import numpy as np
import uuid
from datetime import timedelta, date, datetime
from typing import Iterator, List
from pathlib import Path
from .data_model import Merchant, TransactionPattern

class TransactionGenerator:
    """
    Generates synthetic transaction data.
    """
    STATUSES = ['completed', 'pending', 'failed']
    STATUSES_PROBABILITIES = [0.85, 0.05, 0.1]
    TYPES = ['dine_in', 'takeaway', 'delivery']
    TYPES_PROBABILITIES = [0.5, 0.2, 0.3]
    PAYMENT_METHODS = ['cash', 'card', 'qr_code', 'e_wallet']
    PAYMENT_PROBABILITIES = [0.5, 0.1, 0.3, 0.1]

    def __init__(self, start_date: date, end_date: date, num_merchants: int, pattern: TransactionPattern, random_seed: int = 42):
        self.start_date = start_date
        self.end_date = end_date
        self.num_merchants = num_merchants
        self.pattern = pattern
        self.random_seed = random_seed
        self.merchants = self._generate_merchant_details()

    def _generate_merchant_details(self) -> List[Merchant]:
        """
        Generate random merchant transaction characteristics.
        """
        rng = np.random.default_rng(self.random_seed)

        return [
            Merchant(
                id=i+1,
                avg_transaction=self.pattern.base_transaction + rng.lognormal(3, 0.25),
                avg_amount=self.pattern.base_amount + rng.lognormal(9, 0.5),
                std_amount=rng.uniform(1_000, 3_000),
                weekend_factor=rng.uniform(1, self.pattern.max_weekend_factor)
            )
            for i in range(self.num_merchants)
        ]

    def generate_daily_transactions(self, current_datetime: datetime, num_day: int) -> Iterator[dict]:
        """
        Generate daily transactions of all merchants.
        """
        rng = np.random.default_rng(num_day)
        weekday = current_datetime.weekday()
        noise = rng.normal(1, 0.1)
        
        for merchant in self.merchants:
            # Calculate number of transactions
            daily_factor = self.pattern.get_daily_factor(num_day, weekday, merchant.weekend_factor, noise)
            num_transactions = int(round(merchant.avg_transaction * daily_factor))

            # Vectorized transaction details
            uuids = [str(uuid.uuid4()) for _ in range(num_transactions)]
            statuses = rng.choice(self.STATUSES, p=self.STATUSES_PROBABILITIES, size=num_transactions)
            types = rng.choice(self.TYPES, p=self.TYPES_PROBABILITIES, size=num_transactions)
            payment_methods = rng.choice(self.PAYMENT_METHODS, p=self.PAYMENT_PROBABILITIES, size=num_transactions)
            amounts = np.round(rng.normal(merchant.avg_amount, merchant.std_amount, size=num_transactions))
            timestamps = [
                current_datetime + timedelta(seconds=int(second)) 
                for second in sorted(rng.integers(0, 86_399, size=num_transactions))
            ]
            
            # Yield transactions  
            yield {
                'transaction_id': uuids,
                'merchant_id': merchant.id,
                'transaction_status': statuses,
                'transaction_type': types,
                'transaction_payment_method': payment_methods,
                'transaction_amount': amounts,
                'transaction_datetime': timestamps
            }
        
    def write_to_parquet(self, output_dir: str = 'output') -> None:
        """
        Write generated transactions to parquet with polars.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        delta_date = self.end_date - self.start_date
        num_days = delta_date.days + 1

        for day in range(num_days):
            current_date = self.start_date + timedelta(days=day)
            current_datetime = datetime.combine(current_date, datetime.min.time())
            transaction_generator = self.generate_daily_transactions(current_datetime, day)
            current_batch = pl.concat(pl.DataFrame(transaction) for transaction in transaction_generator)
            current_batch.write_parquet(output_path / f'transactions_{current_date}.parquet', compression='zstd')
            print(f'transactions_{current_date}.parquet written with {len(current_batch)} rows.')