import unittest

import sys
sys.path.append("./src/")

from cpa_1464 import CPAFile, Transaction


class BasicTests(unittest.TestCase):
    def test_generates_4_lines(self):
        transactions = [Transaction('CREDIT', 100, '01023421', '023125523', 'bob'),
                        Transaction('CREDIT', 500, '01023421', '235235234', 'jill'),
                        Transaction('DEBIT', 100, '01023421', '394570233', 'zak'),
                        Transaction('DEBIT', 9000, '01023421', '23052353', 'matt')]

        cpa_file = CPAFile(file_number=1, transactions=transactions)
        content = cpa_file.generate_file()
        self.assertEquals(len(content.split("\n")), 4)
