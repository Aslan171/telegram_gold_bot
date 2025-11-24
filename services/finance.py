from config import RATE_TENGE_PER_G

# Конвертация ₸ → G
def tenge_to_g(amount_tenge: float) -> float:
    return amount_tenge / RATE_TENGE_PER_G

# Конвертация G → ₸
def g_to_tenge(amount_g: float) -> float:
    return amount_g * RATE_TENGE_PER_G

# Рассчёт суммы для вывода с комиссией 20%
def withdraw_with_fee(amount_g: float, fee_percent: float = 20) -> float:
    return amount_g * (1 + fee_percent / 100)


