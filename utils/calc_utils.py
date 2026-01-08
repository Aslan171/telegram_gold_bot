# Курс: 5.5 тенге = 1 G
EXCHANGE_RATE = 5.5

def tenge_to_gold(tenge: float) -> float:
    """
    Конвертирует тенге в голду
    """
    return round(tenge / EXCHANGE_RATE, 2)

def gold_to_tenge(gold: float) -> float:
    """
    Конвертирует голду в тенге
    """
    return round(gold * EXCHANGE_RATE, 2)

