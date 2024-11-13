from logging import Logger
import requests
from src.service.relay_service import RelayService

# turn off url: http://192.168.1.133/relay/0?turn=off
# turn on url: http://192.168.1.133/relay/0?turn=on


class ShellyRelayService(RelayService):
    def __init__(self, ip_address: str, logger: Logger):
        self.ip_address = ip_address
        self.logger = logger

    def turn_on(self):
        self.logger.info(f"Turning on the relay at IP address {self.ip_address}.")
        requests.get(f"http://{self.ip_address}/relay/0?turn=on", timeout=10)

    def turn_off(self):
        self.logger.info(f"Turning off the relay at IP address {self.ip_address}.")
        requests.get(f"http://{self.ip_address}/relay/0?turn=off", timeout=10)
