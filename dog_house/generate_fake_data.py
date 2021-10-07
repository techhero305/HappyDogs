import random
import string
from datetime import date, timedelta, datetime

import holidays

WEIGHT_FOR_US_HOLIDAY = 3
WEIGHT_FOR_SAT_FRI_DAY = 5
WEIGHT_FOR_NORMAL_DAY = 1

date_dict_fake_data = {}


def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


def get_all_dates_of_specific_day(days):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    d = date(currentYear, currentMonth, 1)
    d += timedelta(days=days - d.weekday())
    while d.year == currentYear:
        yield d
        d += timedelta(days=7)


def get_all_dates():
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    start_date = date(currentYear, currentMonth, 1)
    end_date = date(currentYear, 12, 31)

    delta = end_date - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        yield day


def get_dates_list():
    if 'us_holidays' not in date_dict_fake_data.keys():
        us_holiday_list = []
        for h_date, holiday in holidays.US(years=2021).items():
            if not h_date < date.today():
                h_date_before = h_date - timedelta(days=2)
                h_date_after = h_date + timedelta(days=2)
                us_holiday_list.append(h_date_before)
                if not h_date_after.year > datetime.now().year:
                    us_holiday_list.append(h_date_after)
        date_dict_fake_data['us_holidays'] = us_holiday_list
    if 'list_of_dates' not in date_dict_fake_data:
        date_dict_fake_data['list_of_dates'] = list(get_all_dates_of_specific_day(days=4)) + list(
            get_all_dates_of_specific_day(days=5))
    if 'list_of_all_date' not in date_dict_fake_data:
        date_dict_fake_data['list_of_all_date'] = list(get_all_dates())
    return date_dict_fake_data


def generate_fake_data():
    if not date_dict_fake_data:
        get_dates_list()
    us_holiday_list = date_dict_fake_data['us_holidays']
    list_of_required_dates = date_dict_fake_data['list_of_dates']
    all_dates = date_dict_fake_data['list_of_all_date']
    weights = []
    for data in all_dates:
        if data in list_of_required_dates and us_holiday_list:
            weights.append(WEIGHT_FOR_US_HOLIDAY * WEIGHT_FOR_SAT_FRI_DAY)
        elif data in us_holiday_list:
            weights.append(WEIGHT_FOR_US_HOLIDAY)
        elif data in list_of_required_dates:
            weights.append(WEIGHT_FOR_SAT_FRI_DAY)
        else:
            weights.append(WEIGHT_FOR_NORMAL_DAY)
    randomNumberList = []
    for data in range(0, 50):
        start_date = random.choices(all_dates, weights=weights, k=1)
        # assuming here that a dog can be in house for maximum of 7 days
        end_date = start_date[0] + timedelta(days=random.choice([0, 1, 2, 3, 4, 5, 6]))
        randomNumberList.append({'first_name': random_string_generator(4, string.ascii_letters),
                                 'last_name': random_string_generator(4, string.ascii_letters),
                                 'start_date': start_date[0],
                                 'end_date': end_date})
    return randomNumberList
