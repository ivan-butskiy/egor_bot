from dataclasses import dataclass


@dataclass(frozen=True)
class StartKbCommands:
    # common
    to_the_head: str = '🚪 На головну'
    orders: str = '📋 Замовлення'
    suppliers: str = '🚚 Постачальники'

    # compatible to admin
    users: str = '🫡 Користувачі'

    # # compatible to manager
    # create_order: str = ' Створити замовлення'
    # order_history: str = 'Історія замовлень'
