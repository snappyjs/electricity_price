import time
from datetime import datetime

# https://www.elprisetjustnu.se/api/v1/prices/2024/11-08_SE3.json
MAXIMUM_PRICE = 0.15  # SEK per kWh
SLEEP_TIME = 120
IP = "192.168.1.133"

import logging

from src.service.http_el_price_service import ElprisetJustNuService
from src.service.http_relay_service import ShellyRelayService

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

el_priset_just_nu = ElprisetJustNuService(logging.getLogger("elprisetjustnu"))

relay_service = ShellyRelayService(IP, logging.getLogger("shelly_relay_service"))

logging.info(
    f"Starting the electricity price monitoring service. Maximum price: {MAXIMUM_PRICE} SEK/kWh"
)
while True:
    try:
        price = el_priset_just_nu.get_price(datetime.now(), "SE3")
        if price < MAXIMUM_PRICE:
            relay_service.turn_on()
        else:
            relay_service.turn_off()
        time.sleep(SLEEP_TIME)
    except Exception as e:
        logging.error(f"An unhandled error occurred: {e}")
