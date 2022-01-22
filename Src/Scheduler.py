
class Scheduler:
    """
    Determines what times network traffic is low/high.
    """

    _LOW_TRAFFIC_START = ''
    _LOW_TRAFFIC_END = ''

    @staticmethod
    def is_low_traffic_time() -> bool:
        return True
