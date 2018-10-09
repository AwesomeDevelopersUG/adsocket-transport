from .broker import BaseBroker
from .exceptions import ADSocketException
from .message import Message
from . utils import import_driver

__all__ = [
    'ADSocketTransport'
]


class ADSocketTransport:
    """

    """
    _broker = None
    """
    :var broker.BaseBroker: Broker instance
    """

    def __init__(self, driver, driver_options):
        self._initialize_broker(driver, driver_options)

    def _initialize_broker(self, driver, driver_options):
        try:
            driver_class = import_driver(driver)
        except (ImportError, AttributeError) as e:
            raise ADSocketException("Could not import broker driver "
                                    "in broker folder")

        if not issubclass(driver_options, BaseBroker):
            raise ADSocketException("Broker class must be subclass of "
                                    "adsocket_transport.broker.BaseBroker")

        driver_options = driver_options or {}
        broker = driver_class(**driver_options)
        self._broker = broker

    def send_data(self, data, channels, message_type='publish'):
        """

        :param data: Data to be send to WebSocket broker
        :type data: str, dict, list
        :param channels: To which channel(s) should be message published to
        :type channels: str, list, tuple
        :param message_type: which command should be executed to
                            WebSocket part. Default is `publish`
        :type message_type: str
        :return: void
        :rtype: void
        """
        if not isinstance(channels, (list, tuple)):
            channels = [channels]

        for channel in channels:
            if isinstance(channel, (list, tuple, dict)):
                if len(channel) != 2:
                    raise ADSocketException(
                        f"Unknown channel data {channel}. "
                        f"I except list or tuple in format "
                        f"[channel_name, channel_id] "
                        f"or dict {'name': name, 'id': id}")

            self.send(Message(
                type=message_type,
                data=data,
                channel=channel['name'],
                channel_id=channel['id']
                )
            )

    def send(self, message: Message):
        """
        Publish message to broker

        :param message: Message instance to be send
        :type message: Message
        :return: void
        :rtype: void
        """
        if not isinstance(message, Message):
            raise ADSocketException(
                "Message must be adsocket_`transport.Message` instance. "
                "If you want to send raw data use `send_data` method")

        self._broker.publish(message)
