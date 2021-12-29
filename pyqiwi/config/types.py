import typing
from pydantic import BaseModel


class Amount(BaseModel):
    currency: typing.Literal["RUB", "USD", "EUR", "KZT"]
    value: float

    class Config:
        orm_mode = True


class Customer(BaseModel):
    phone: str = None
    email: str = None
    account: str = None

    class Config:
        orm_mode = True


class CustomField(BaseModel):
    paySourcesFilter: typing.Literal["qw", "card", "mobile"] = None
    themeCode: str = None


class Status(BaseModel):
    value: str
    changedDateTime: str


class Bill(BaseModel):
    billId: str
    siteId: str
    amount: Amount
    status: Status
    comment: str = None
    creationDateTime: str
    payUrl: str
    expirationDateTime: str
    customer: Customer = None
    customFields: CustomField = None
