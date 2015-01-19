from __future__ import print_function

__version__ = '0.1'

from datetime import date
import StringIO
import uuid


class CPAFile():

    ORIGINATOR_ID = '0000000000'
    DATA_CENTRE = '00000'
    SHORT_NAME = "MATT"
    LONG_NAME = "MATT WARREN"
    CLIENT_SUNDRY = "investing in the future"

    # file_number = ''
    record_count = 0

    total_debit_amount = 0
    total_debit_count = 0
    total_credit_amount = 0
    total_credit_count = 0

    def __init__(self, **kwargs):
        # global file_number
        self.file_number = self.format_number(kwargs['file_number'], 4)
        self.today = self.format_date(date.today())
        self.transactions = kwargs['transactions']
        self.debit_transaction_code = '450'

    def format_date(self, d):
        return d.strftime("0%y%j")

    def format_number(self, n, width):
        return "{0:>{1}}".format(n, width)

    def format_alpha(self, s, width):
        return "{0:<{1}}".format(s, width)

    def header_record(self):
        self.record_count += 1
        return ''.join(['A',
                        self.format_number(self.record_count, 9),
                        self.format_alpha(self.ORIGINATOR_ID, 10),
                        self.format_number(self.file_number, 4),
                        self.today,
                        self.format_number(self.DATA_CENTRE, 5),
                        " " * 20,
                        'CAD',
                        " " * 1406,
                        "\n"])

    def footer_record(self):
        self.record_count += 1
        return ''.join(['Z',
                        self.format_number(self.record_count, 9),
                        self.format_alpha(self.ORIGINATOR_ID, 10),
                        self.format_number(self.file_number, 4),
                        self.format_number(self.total_debit_amount, 14),
                        self.format_number(self.total_debit_count, 8),
                        self.format_number(self.total_credit_amount, 14),
                        self.format_number(self.total_credit_count, 8),
                        "0" * 1396,  # error corrections not yet implemented
                        "\n"])

    def debit_credit_records(self, transaction_type):
        all_records = []
        lr = ""
        for transaction in [r for r in self.transactions if r.transaction_type == transaction_type]:
            assert(len(lr) <= 1464)
            if len(lr) == 1464:
                all_records.append(lr + "\n")
                lr = ''
            if len(lr) == 0:
                self.record_count += 1
                lr = ''.join([transaction_type[0],
                              self.format_number(self.record_count, 9),
                              self.format_alpha(self.ORIGINATOR_ID, 10),
                              self.file_number])
            segment = ''.join((self.format_alpha(self.debit_transaction_code, 3),
                               self.format_number(transaction.amount, 10),
                               self.format_date(transaction.date),
                               self.format_number(transaction.routing_number, 9),
                               self.format_alpha(transaction.account_number, 12),
                               "0" * 25,
                               self.format_alpha(self.SHORT_NAME, 15),
                               self.format_alpha(transaction.customer_name, 30),
                               self.format_alpha(self.LONG_NAME, 30),
                               self.format_alpha(self.ORIGINATOR_ID, 10),
                               self.format_alpha(transaction.customer_number, 19),
                               "0" * 9,
                               " " * 12,
                               self.format_alpha(self.CLIENT_SUNDRY, 15),
                               " " * 35))

            if transaction_type == 'DEBIT':
                self.total_debit_amount += transaction.amount
                self.total_debit_count += 1
            elif transaction_type == 'CREDIT':
                self.total_credit_amount += transaction.amount
                self.total_credit_count += 1
            lr = lr + segment

        while len(lr) < 1464:
            lr = lr + ('0' * 340)
        all_records.append(lr + "\n")

        return ''.join(all_records)

    def generate_file(self):
        self.record_count = 0
        self.total_debit_amount = 0
        self.total_debit_count = 0
        self.total_credit_amount = 0
        self.total_credit_count = 0

        f = StringIO.StringIO()
        f.write(self.header_record())
        f.write(self.debit_credit_records('DEBIT'))
        f.write(self.debit_credit_records('CREDIT'))
        f.write(self.footer_record())
        return f.getvalue()


class Transaction:
    def __init__(self, transaction_type, amount_cents, routing_number, account_number, customer_name):
        self.transaction_type = transaction_type
        self.amount_cents = amount_cents
        self.routing_number = routing_number
        self.account_number = account_number
        self.customer_name = customer_name

    @property
    def amount(self):
        return self.amount_cents

    @property
    def date(self):
        return date.today()

    @property
    def customer_number(self):
        return str(uuid.uuid1()).split('-')[-1]


if __name__ == '__main__':
    transactions = [Transaction('CREDIT', 100, '01023421', '023125523', 'bob'),
                    Transaction('CREDIT', 500, '01023421', '235235234', 'jill'),
                    Transaction('DEBIT', 100, '01023421', '394570233', 'zak'),
                    Transaction('DEBIT', 9000, '01023421', '23052353', 'matt')]

    cpa_file = CPAFile(file_number=1, transactions=transactions)
    print(cpa_file.generate_file())
