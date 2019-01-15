# inbuilt libs
import unittest

# project libs
import bill_member


class TestBillMember(unittest.TestCase):

    def test_calculate_bill_for_august(self):
        amount, kwh = bill_member.calculate_bill(member_id='member-123',
                                                 account_id='ALL',
                                                 bill_date='2017-08-31')
        self.assertEqual(amount, 27.57)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
