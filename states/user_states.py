from aiogram.fsm.state import StatesGroup, State

class WithdrawState(StatesGroup):
    amount = State()

class DepositState(StatesGroup):
    amount = State()
    waiting_receipt = State()

class CalculateState(StatesGroup):
    amount = State()
    mode = State()  # 'to_g' or 'to_tenge'
