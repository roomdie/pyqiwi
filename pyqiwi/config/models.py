import typing


class CustomerCls:
    def __init__(self, phone: str = None, email: str = None, account: str = None):
        self.phone = phone
        self.email = email
        self.account = account


class AmountCls:
    def __init__(self, currency: typing.Literal["RUB", "USD", "EUR", "KZT"], value: float):
        self.currency = currency
        self.value = value
