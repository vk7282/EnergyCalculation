# inbuilt libs
from datetime import datetime

# project libs
from tariff import BULB_TARIFF


def process_account_details(account_details, bill_date):
    """
    Returns the amount and usage for an account of a given bill date

    :param account_details: list of energy usage for electricity and gas of a member account
    :param bill_date: a given business date that we want to compute the bill for
    :return:
        total_amount: total amount consumed (in pence) for electricity and gas of a member account
        total_usage: total usage in kwh for a member account
    """
    electric_bill_amount = 0
    gas_bill_amount = 0
    electric_usage, gas_usage = 0, 0
    for energy_type in account_details:
        if "electricity" in energy_type:
            electric_bill_readings = energy_type.get("electricity")
            electric_bill_amount, electric_usage = calculate_energy_bills(electric_bill_readings,
                                                                          bill_date, "electricity")
        else:
            gas_bill_readings = energy_type.get("gas")
            gas_bill_amount, gas_usage = calculate_energy_bills(gas_bill_readings, bill_date, "gas")
    total_amount = electric_bill_amount + gas_bill_amount
    total_usage = electric_usage + gas_usage
    return total_amount, total_usage


def calculate_energy_bills(bill_readings, bill_date, energy_type):
    """
    Returns the amount and usage for specific energy type on a given bill date

    :param bill_readings: list of specific energy type readings (electricity or gas)
    :param bill_date: a given business date that we want to compute the bill for
    :param energy_type: electricity or gas
    :return:
        total_amount: total bill for specific energy type on a given bill date
        total_usage: total energy type usage in kwh for a given bill date

    If the bill date is the first readingDate from the readings.json dataset
    the bill is calculated on basis of 31 days and cumulative value
    """
    previous_usage, current_usage = 0, 0
    previous_date, current_date = None, None
    for bill in bill_readings:
        if check_billing_date(bill.get("readingDate"), bill_date):
            current_usage = bill.get("cumulative")
            current_date = bill.get("readingDate")
            break
        previous_usage = bill.get("cumulative")
        previous_date = bill.get("readingDate")

    # Checking if it is the first reading itself in readings.json
    previous_usage = 0 if previous_usage is None else previous_usage
    # get the total usage by difference of previous and current usage
    total_usage = current_usage - previous_usage

    # get the number of days from last reading else take 31 default
    if previous_date is not None:
        total_days = calculate_days(previous_date, current_date)
    else:
        total_days = 31

    # get the unit rate and standing charge of each energy type
    unit_rate = BULB_TARIFF.get(energy_type).get("unit_rate")
    standing_charge = BULB_TARIFF.get(energy_type).get("standing_charge")

    # calculate the total bill for the bill readings
    total_amount = (total_usage*unit_rate)+(total_days*standing_charge)

    return total_amount, total_usage


def calculate_days(previous_date, current_date):
    """
    Returns the total days for which bill is calculated from previous readings

    :param previous_date: date of the previous readings from the current bill date
    :param current_date: date of the current readings
    :return: total number of days for which bill is calculated
    """
    previous_date_obj = datetime.strptime(previous_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    bill_date_obj = datetime.strptime(current_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return (bill_date_obj-previous_date_obj).days


def check_billing_date(reading_date, billing_date):
    """
    Returns True or False if the bill date matches the reading date in json

    :param reading_date: reading date of a json object from readings.json file
    :param billing_date: bill date for which the bill is computed for
    :return: True or False
    """
    reading_date_obj = datetime.strptime(reading_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return str(reading_date_obj.date()) == billing_date
