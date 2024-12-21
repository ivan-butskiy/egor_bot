from dataclasses import dataclass


@dataclass(frozen=True)
class StartKbCommands:
    # compatible to admin
    orders: str = 'Замовлення'
    suppliers: str = 'Постачальники'

    # compatible to manager
    create_order: str = 'Створити замовлення'
    order_history: str = 'Історія замовлень'
