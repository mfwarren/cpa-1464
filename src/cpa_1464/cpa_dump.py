#!/usr/bin/env python3
# imports go here
import sys
import pprint

#
# Free Coding session for 2015-01-24
# Written by Matt Warren
#

# all the numbers come from https://www.cdnpay.ca/imis15/pdf/pdfs_rules/standard_005.pdf


def substring(line, start, end=None, offset=0):
    """
    This is used to adjust the number to match what's in the specification
    """
    if end is None:
        return line[start-1+offset]
    return line[start-1+offset:end+offset]


def read_a_record(line):
    if substring(line, 1) != 'A':
        raise Exception("First line must be 'A' record")
    if substring(line, 2, 10) != '000000001':
        raise Exception("First line must be record 1")
    assert_line_length(line)
    return {
        'record type': substring(line, 1),
        'line number': substring(line, 2, 10),
        'originator id': substring(line, 11, 20),
        'file creation number': substring(line, 21, 24),
        'creation date': substring(line, 25, 30),
        'destination data centre': substring(line, 31, 35),
        'reserved customer-direct communcation area': substring(line, 36, 55),
        'currency': substring(line, 56, 58),
    }


def read_cd_segment(segment, offset=0):
    if substring(segment, 1, 2).strip() == '':
        return None
    return {
        'Transaction Type': substring(segment, 1, 3, offset),
        'Amount': substring(segment, 4, 13, offset),
        'Date Funds to be Available': substring(segment, 14, 19, offset),
        'Institutional Identification No.': substring(segment, 20, 28, offset),
        'Payee Account No.': substring(segment, 29, 40, offset),
        'Item Trace No.': substring(segment, 41, 62, offset),
        'Stored Transaction Type': substring(segment, 63, 65, offset),
        'Originator\'s Short Name': substring(segment, 66, 80, offset),
        'Payee Name': substring(segment, 81, 110, offset),
        'Originator\'s Long Name': substring(segment, 111, 140, offset),
        'Originating Direct Clearer\'s User\'s ID': substring(segment, 141, 150, offset),
        'Originator\'s Cross Reference No.': substring(segment, 151, 169, offset),
        'Institutional ID Number for Returns': substring(segment, 170, 178, offset),
        'Account No. for Returns': substring(segment, 179, 190, offset),
        'Originator\'s Sundry Information': substring(segment, 191, 205, offset),
        'Originator-Direct Clearer Settlement code': substring(segment, 228, 229, offset),
        'Invalid Data Element I.D.': substring(segment, 230, 240, offset)
    }


def read_cd_record(line):
    assert_line_length(line)
    if substring(line, 1) not in ['C', 'D']:
        raise Exception("Should start with C or D")
    transactions = [read_cd_segment(line, 23),
                    read_cd_segment(line, 263),
                    read_cd_segment(line, 503),
                    read_cd_segment(line, 743),
                    read_cd_segment(line, 983),
                    read_cd_segment(line, 1223)]
    transactions = [i for i in transactions if not None]
    if substring(line, 1) == 'C':
        transaction_type = 'credits'
    else:
        transaction_type = 'debits'
    return {
        'record type': substring(line, 1),
        'line number': substring(line, 2, 10),
        'Origination Control Data': substring(line, 11, 24),
        transaction_type: transactions
    }
    pass


def read_z_record(line):
    if substring(line, 1) != 'Z':
        raise Exception("Last line must be 'Z' record")
    assert_line_length(line)
    return {
        'record type': substring(line, 1),
        'line number': substring(line, 2, 10),
        'Origination Control Data': substring(line, 11, 24),
        'Total Value of Debit Transactions': substring(line, 25, 38),
        'Total Number of Debit Transactions': substring(line, 39, 46),
        'Total Value of Credit Transactions': substring(line, 47, 60),
        'Total Number of Credit Transactions': substring(line, 61, 68),
        'Total Value of Error Corrections "E"': substring(line, 69, 82),
        'Total Number of Error Corrections "E"': substring(line, 83, 90),
        'Total Value of Error Corrections "F"': substring(line, 91, 104),
        'Total Number of Error Corrections "F"': substring(line, 105, 112)
    }


def assert_line_length(line):
    if len(line) != 1465:  # includes newline
        print(len(line))
        raise Exception("Line length is not equal to 1464")


def main(filename):
    pp = pprint.PrettyPrinter(indent=4)
    with open(filename) as f:
        lines = f.readlines()

        pp.pprint(read_a_record(lines[0]))
        for line in lines[1:-1]:
            if substring(line, 1) == 'D' or substring(line, 1) == 'C':
                pp.pprint(read_cd_record(line))
        pp.pprint(read_z_record(line[-1]))


if __name__ == '__main__':
    main(sys.argv[1])
