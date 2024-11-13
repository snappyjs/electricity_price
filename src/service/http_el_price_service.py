from logging import Logger
import requests
from datetime import datetime
from .el_price_service import ElPriceService

# https://www.elprisetjustnu.se/api/v1/prices/2024/11-08_SE3.json


class ElprisetJustNuService(ElPriceService):

    def __init__(self, logger: Logger):
        self.logger = logger

    def get_price(self, date: datetime, area: str) -> float:
        assert isinstance(date, datetime), "date must be a datetime object"
        assert isinstance(area, str), "area must be a string"

        self.logger.info(f"Fetching electricity price for {date} in area {area}.")
        url = self.__generate_link(date, area)
        self.logger.info(f"Fetching electricity price from {url}.")
        current_hour = date.strftime("%H:00:00")
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch electricity price from API. url: {url}")
            raise Exception(f"Failed to fetch electricity price from API. url: {url}")

        data = response.json()
        assert isinstance(data, list), "data must be a list"
        for entry in data:
            if entry["time_start"].endswith(current_hour + "+01:00"):
                price = entry["SEK_per_kWh"]
                self.logger.info(
                    f"Got electricity price for {date} and for current hour: {current_hour}, price is {price}"
                )
                return price

        self.logger.error(
            f"Failed to find the electricity price for the current hour. {current_hour}"
        )
        raise Exception(
            f"Failed to find the electricity price for the current hour. {current_hour}"
        )

    def __generate_link(self, date: datetime, area: str) -> str:
        current_date = date.strftime("%Y/%m-%d")
        return f"https://www.elprisetjustnu.se/api/v1/prices/{current_date}_{area}.json"
