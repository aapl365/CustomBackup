from datetime import datetime, time

import pytz

class Scheduler:
    """
    Determines what times network traffic is low/high.
    """

    _LOW_TRAFFIC_START_ISO = '02:00:00'
    _LOW_TRAFFIC_END_ISO = '05:00:00'

    @staticmethod
    def is_low_traffic_time(timezone_str: str='US/Pacific') -> bool:
        tz = pytz.timezone(timezone_str)
        time_now = datetime.now(tz).time()
        low_traffic_start = time.fromisoformat(Scheduler._LOW_TRAFFIC_START_ISO)
        low_traffic_end = time.fromisoformat(Scheduler._LOW_TRAFFIC_END_ISO)
        return low_traffic_start < time_now < low_traffic_end
