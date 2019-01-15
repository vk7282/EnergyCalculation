# project libs
import bill_utils
from load_readings import get_readings


def calculate_bill(member_id=None, account_id=None, bill_date=None):

    if member_id not in get_readings():
        print("No Member Id associated with {member}".format(member=member_id))
        exit()
    # get the data from readings.json file for a member
    member_accounts = get_readings().get(member_id)
    amount = 0
    kwh = 0
    for accounts in member_accounts:
        if account_id is not 'ALL' and account_id in accounts:
            account_details = accounts.get(account_id)
            total_amount, total_usage = bill_utils.process_account_details(account_details, bill_date)
            amount += total_amount
            kwh += total_usage
        else:
            for account in accounts.keys():
                account_details = accounts.get(account)
                total_amount, total_usage = bill_utils.process_account_details(account_details, bill_date)
                amount += total_amount
                kwh += total_usage

    return round(amount/100, 2), kwh


def calculate_and_print_bill(member_id, account, bill_date):
    """
    Calculate the bill and then print it to screen.
    Account is an optional argument - I could bill for one account or many.
    There's no need to refactor this function.
    """

    member_id = member_id or 'member-123'
    bill_date = bill_date or '2017-08-31'
    account = account or 'ALL'
    amount, kwh = calculate_bill(member_id, account, bill_date)
    print('Hello {member}!'.format(member=member_id))
    print('Your bill for {account} on {date} is £{amount}'.format(
        account=account,
        date=bill_date,
        amount=amount))
    print('based on {kwh}kWh of usage in the last month'.format(kwh=kwh))
