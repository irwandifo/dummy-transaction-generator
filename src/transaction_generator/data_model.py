from dataclasses import dataclass

@dataclass
class Merchant:
    """
    Defines basic attributes of merchant transactions.
    """
    id: int
    avg_transaction: float
    avg_amount: float
    std_amount: float
    weekend_factor: float

@dataclass
class TransactionPattern:
    """
    Defines transaction pattern.
    """
    base_amount: int
    base_transaction: int
    trend_factor: float
    max_weekend_factor: float

    def get_daily_factor(self, day_number: int, weekday: int, weekend_factor: float, noise: float) -> float:
        """
        Calculate daily multiplier based on trend, weekend seasonality, and random noise.
        """
        trend = 1 + (self.trend_factor * day_number)
        seasonality = weekend_factor if weekday >= 5 else 1
        return trend * seasonality * noise