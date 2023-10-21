from datetime import datetime
from pytz import timezone

class CommonHelper:

    def get_timezone_now(self, format='%Y-%m-%d %H:%M:%S'):
        return datetime.now(timezone('US/Eastern')).strftime(format)
