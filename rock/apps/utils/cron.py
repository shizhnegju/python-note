from croniter import croniter
from datetime import datetime, timedelta
import pytz


def cron_validate(cron):
    return croniter.is_valid(cron)


def parse_cron(cron):
    now = datetime.now()
    iter = croniter(cron, now + timedelta(minutes=2))
    timezone = pytz.timezone("Asia/Shanghai")
    return timezone.localize(iter.get_next(datetime))
