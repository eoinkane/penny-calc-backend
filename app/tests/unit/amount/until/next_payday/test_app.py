import datetime
import decimal
from datetime import datetime as datetime_type
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from app.tests.utils.strip_milliseconds import strip_milliseconds
from app.src.amount.until.next_payday import app
import pytest


class TestServiceHandler:
    @pytest.fixture
    def event(self):
        return {}

    @pytest.fixture
    def context(self):
        return {}

    def test_lambda_handler(self, event, context):
        result = app.lambda_handler(event, context)
        assert result['statusCode'] == 200
        assert result['headers'] == {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS"
        }
        assert type(result['body']) == float


def test_make_todays_date():
    expected = datetime.datetime.today()
    expected_no_milliseconds = strip_milliseconds(expected)

    result = app.make_todays_date()
    result_no_milliseconds = strip_milliseconds(result)

    assert type(result) == datetime_type
    assert result_no_milliseconds == expected_no_milliseconds


def test_calc_next_month():
    today = datetime.datetime.now()
    expected = today + relativedelta(months=+1)
    expected_no_milliseconds = strip_milliseconds(expected)

    result = app.calc_next_month(today)
    result_no_milliseconds = strip_milliseconds(result)

    assert type(result) == datetime_type
    assert result_no_milliseconds == expected_no_milliseconds


def test_make_next_date():
    expected_day_number = 25
    today = app.make_todays_date()
    expected = datetime.datetime(today.year, today.month, expected_day_number)
    expected_no_milliseconds = strip_milliseconds(expected)

    result = app.make_next_date(today, expected_day_number)
    result_no_milliseconds = strip_milliseconds(result)

    assert type(result) == datetime_type
    assert result_no_milliseconds == expected_no_milliseconds


def test_calc_next_working_date_weekend():
    rs = rrule.rruleset()
    r = rrule.rrule(
                    rrule.DAILY,
                    byweekday=[
                        rrule.SU
                    ],
                    dtstart=app.make_todays_date())
    rs.rrule(r)
    next_sunday = rs[0]

    assert next_sunday.weekday() == 6
    expected = next_sunday + relativedelta(days=+1)
    expected_no_milliseconds = strip_milliseconds(expected)

    result = app.calc_next_working_date(next_sunday)
    result_no_milliseconds = strip_milliseconds(result)

    assert type(result) == datetime_type
    assert result_no_milliseconds == expected_no_milliseconds


def test_calc_next_working_date_weekday():
    rs = rrule.rruleset()
    r = rrule.rrule(
                    rrule.DAILY,
                    byweekday=[
                        rrule.MO
                    ],
                    dtstart=app.make_todays_date())
    rs.rrule(r)
    next_monday = rs[0]

    assert next_monday.weekday() == 0
    expected = next_monday
    expected_no_milliseconds = strip_milliseconds(expected)

    result = app.calc_next_working_date(next_monday)
    result_no_milliseconds = strip_milliseconds(result)

    assert type(result) == datetime_type
    assert result_no_milliseconds == expected_no_milliseconds


def test_calc_number_of_days():
    number_of_days = 1
    first_date = app.make_todays_date()
    second_date = first_date + relativedelta(days=+number_of_days)
    expected = number_of_days

    result = app.calc_number_of_days(first_date, second_date)

    assert type(result) == int
    assert result == expected


def test_calc_full_amount():
    number_of_days = 5
    daily_amount = 5.555

    expected = round(number_of_days * daily_amount, 2)
    expected_number_of_decimal_places = -2

    result = app.calc_full_amount(number_of_days, daily_amount)
    result_number_of_decimal_places = (
        decimal.Decimal(str(result)).as_tuple().exponent
    )

    assert type(result) == float
    assert result == expected
    assert result_number_of_decimal_places == expected_number_of_decimal_places


def test_process_response():
    expected = {
        "statusCode": 200,
        "body": 5.0,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS"
        }
    }

    result = app.process_response(200, 5.0)

    assert type(result) == dict
    assert result == expected
