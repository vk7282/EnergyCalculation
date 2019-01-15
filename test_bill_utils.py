# inbuilt libs
import unittest

# project libs
import bill_utils


class TestUtilsMethods(unittest.TestCase):

    def test_calculate_days(self):
        """
        Test calculate_days to return the difference between 2 given date
        """
        days = bill_utils.calculate_days('2017-07-31T00:00:00.000Z', '2017-08-31T00:00:00.000Z')
        self.assertEqual(days, 31)

    def test_check_billing_date(self):
        """
        Test check_billing_date to assert true or false for 2 given date
        """
        condition = bill_utils.check_billing_date('2017-08-31T00:00:00.000Z', '2017-08-31')
        self.assertTrue(condition)

    def test_calculate_energy_bills(self):
        """
        Test calculate_energy_bills to return amount and usage(kwh) for specific
        energy type on a given bill date from sample bill readings
        """
        sample_bill_readings = {"electricity": [
        {
          "cumulative": 18270,
          "readingDate": "2017-06-18T00:00:00.000Z",
          "unit": "kWh"
        },
        {
          "cumulative": 18453,
          "readingDate": "2017-07-31T00:00:00.000Z",
          "unit": "kWh"
        },
        {
          "cumulative": 18620,
          "readingDate": "2017-08-31T00:00:00.000Z",
          "unit": "kWh"
        }
        ]}
        amount, kwh = bill_utils.calculate_energy_bills(sample_bill_readings["electricity"],
                                                        '2017-08-31', 'electricity')
        self.assertEqual(round(amount/100,2), 27.57)
        self.assertEqual(kwh, 167)

    def test_process_account_details(self):
        """
        Test process_account_details to return amount and usage(kwh) for a member account on a given bill date
        :return:
        """
        sample_account_details = {"account-abc": [
            {
                "electricity": [
                    {
                      "cumulative": 17580,
                      "readingDate": "2017-03-28T00:00:00.000Z",
                      "unit": "kWh"
                    },
                    {
                      "cumulative": 18453,
                      "readingDate": "2017-07-31T00:00:00.000Z",
                      "unit": "kWh"
                    },
                    {
                      "cumulative": 18620,
                      "readingDate": "2017-08-31T00:00:00.000Z",
                      "unit": "kWh"
                    }
                ]
            }
        ]}

        amount, kwh = bill_utils.process_account_details(sample_account_details["account-abc"], '2017-08-31')
        self.assertEqual(round(amount/100,2), 27.57)
        self.assertEqual(kwh, 167)


if __name__ == '__main__':
    unittest.main()
