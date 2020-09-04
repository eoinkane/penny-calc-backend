import datetime
from datetime import datetime as datetime_type
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from typing import Union


def lambda_handler(event, context):
    today = make_todays_date()

    if (today.day >= 25):
        next_date_month = calc_next_month(today)
    else:
        next_date_month = today

    next_date = make_next_date(next_date_month, 25)

    next_working_date = calc_next_working_date(next_date)

    number_of_days = calc_number_of_days(today, next_working_date)

    amount_for_every_day = calc_full_amount(number_of_days, 3.66)

    return process_response(200, amount_for_every_day)


def make_todays_date() -> datetime_type:
    return datetime.datetime.today()


def calc_next_month(today: datetime_type) -> datetime_type:
    return today + relativedelta(months=+1)


def make_next_date(next_month: datetime_type,
                   day_number: int
                   ) -> datetime_type:
    return datetime.datetime(next_month.year, next_month.month, day_number)


def calc_next_working_date(next_date: datetime_type) -> datetime_type:
    # initialise a ruleset
    rs = rrule.rruleset()

    # create a rule that only matches week days starting from the next date
    r = rrule.rrule(
                    rrule.DAILY,
                    byweekday=[
                        rrule.MO,
                        rrule.TU,
                        rrule.WE,
                        rrule.TH,
                        rrule.FR
                    ],
                    dtstart=next_date)

    # attach week day rule to rule set
    rs.rrule(r)

    # first match of rule is the next working date after next_date
    return rs[0]


def calc_number_of_days(
                        first_date: datetime_type, second_date: datetime_type
                        ) -> int:
    return (second_date - first_date).days


def calc_full_amount(
                     number_of_days: int,
                     daily_amount: Union[int, float]
                     ) -> float:
    return round(number_of_days * daily_amount, 2)


def process_response(status_code: int, body: Union[str, dict, float]) -> dict:
    return {
        "statusCode": status_code,
        "body": body,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS"
        }
    }
