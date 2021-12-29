import typing
import requests
from datetime import datetime

from pyqiwi import types, models
from pyqiwi.utils.random_hex import get_random_hex
from pyqiwi.utils.decorators import check_annotations, MinValue, serializing_json
from contextlib import contextmanager


class Bill:
    def __init__(self, secret_key: str, bill_id: typing.Union[int, str], without_hex: bool = False) -> None:
        self.__secret_key = secret_key
        random_hex = ""
        if without_hex:
            random_hex = get_random_hex(32)

        self.__bill_id = f"{bill_id}{random_hex}"
        self.__api_url = f"https://api.qiwi.com/partner/bill/v1/bills/{self.__bill_id}"

    @contextmanager
    def __session(self):
        session = requests.Session()
        session.headers["Accept"] = "application/json"
        session.headers["Content-Type"] = "application/json"
        session.headers["Authorization"] = f"Bearer {self.__secret_key}"
        yield session
        session.close()

    @serializing_json
    @check_annotations
    def create(self, amount: models.AmountCls, expiration_date_time: typing.Annotated[int, MinValue(10)] = 10,
               comment: str = None, customer: typing.Optional[models.CustomerCls] = None,
               custom_fields: dict = None
               ) -> types.Bill:

        with self.__session() as opened_session:
            bill_fields = dict(
                amount=amount,
                comment=comment,
                expirationDateTime=datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S-00:{expiration_date_time}"),
                customer=customer,
                customFields=custom_fields
            )
            response = opened_session.put(url=self.__api_url, json=bill_fields)

        return types.Bill(**response.json())

    def get(self) -> types.Bill:
        with self.__session() as opened_session:
            response = opened_session.get(url=self.__api_url)
        return types.Bill(**response.json())

    def cancel_unpaid(self) -> types.Bill:
        with self.__session() as opened_session:
            response = opened_session.post(
                "https://api.qiwi.com/partner/bill/v1/bills/" + self.__bill_id + "/reject")
        return types.Bill(**response.json())
