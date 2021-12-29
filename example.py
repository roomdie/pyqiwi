from pyqiwi import types, api, models

# how to get secret key https://developer.qiwi.com/ru/p2p-payments/#auth
SECRET_KEY = ""
BILL_ID = 1

# create config
bill = api.Bill(secret_key=SECRET_KEY, bill_id=BILL_ID)

amount = models.AmountCls(
    currency="RUB",
    value=12
)

user = models.CustomerCls(
    phone="78710009999",
    email="test@tester.com",
    account="454678"
)

response: types.Bill = bill.create(
    amount=amount,
    expiration_date_time=10,
    comment="My first Qiwi bill2!",  # optional field
    customer=user,  # optional field
    custom_fields={     # optional field
        "paySourcesFilter": "qw",
        "themeCode": "Yvan-YKaSh",
    }
)

# Payment Form URL
print(response.payUrl)

