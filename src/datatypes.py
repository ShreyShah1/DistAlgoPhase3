import da
from enum import Enum


class Request:

    def __init__(self, amount, accountNo, operationType, request_id, bank_name):
        self.amount = amount
        self.accountNo = accountNo
        self.operationType = operationType
        self.request_id = request_id
        self.bank_name = bank_name

    def printObject(self):
        print(('The request generated is for Account Number %s of balance %s with the value %s  ' % (self.accountNo, self.balance, self.values)))


class Reply:

    def __init__(self, request_id, outcome, balance, account_no):
        self.request_id = request_id
        self.outcome = outcome
        self.balance = balance
        self.account_no = account_no

    def printObject(self):
        print(('The reply generated is for Request Id %s with status %s of the bank_name %s  ' % (self.request_id, self.status, self.bank_name)))


class Account:

    def __init__(self, balance, account_no, bank_name, sequence):
        self.balance = balance
        self.account_no = account_no
        self.bank_name = bank_name
        self.sequence = sequence

    def printObject(self):
        print(('The Account is for  balance %s account_no %s of the bank_name %s  ' % (self.balance, self.account_no, self.bank_name)))
