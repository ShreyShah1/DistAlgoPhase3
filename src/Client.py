import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('Failure'), da.pat.FreePattern('key'), da.pat.FreePattern('Server'), da.pat.FreePattern('str')])
PatternExpr_1 = da.pat.TuplePattern([da.pat.ConstantPattern('Extend'), da.pat.FreePattern('key'), da.pat.FreePattern('newServer')])
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('Response'), da.pat.FreePattern('rep')])
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('CLIENT_NEVER_TERMINATE'), da.pat.FreePattern(None)])
import sys
import time
import os
import logging
from threading import Thread
from datatypes import Request
from datatypes import Reply


class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ClientReceivedEvent_2 = []
        self._ClientReceivedEvent_3 = []
        self._events.extend([
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_0, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_0]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_1, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_1]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_2, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_3', PatternExpr_4, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def main(self):
        self.InitializeLogger(
        str(
        os.getpid()))
        self.logger.info(('Log File for client no ' + str(self.client_no)))
        self.threaded_function(5)

        def ExistentialOpExpr_1():
            for (_, _, (_ConstantPattern31_, _)) in self._ClientReceivedEvent_3:
                if (_ConstantPattern31_ == 'CLIENT_NEVER_TERMINATE'):
                    if True:
                        return True
            return False
        _st_label_101 = 0
        while (_st_label_101 == 0):
            _st_label_101+=1
            if ExistentialOpExpr_1():
                _st_label_101+=1
            else:
                super()._label('_st_label_101', block=True)
                _st_label_101-=1

    def setup(self, client_no, head_tail_details, client_access_list, requests, timeout, retry, sleepbetweenrequests):
        self.retry = retry
        self.requests = requests
        self.client_no = client_no
        self.client_access_list = client_access_list
        self.timeout = timeout
        self.sleepbetweenrequests = sleepbetweenrequests
        self.head_tail_details = head_tail_details
        self.sequence_no = 0
        print('Initializing Client ', client_no)
        self.client_no = client_no
        self.client_server_details = dict()
        self.client = None
        self.logger = None
        self.responses = set()
        self.set_server_details()

    def set_server_details(self):
        for (key, value) in self.client_access_list.items():
            attributes_client = {'AccountNo': '', 'Head': '', 'Tail': ''}
            self.client_server_details[key] = attributes_client
            if (key in self.head_tail_details):
                self.client_server_details[key]['Head'] = self.head_tail_details[key]['Head']
                self.client_server_details[key]['Tail'] = self.head_tail_details[key]['Tail']
            self.client_server_details[key]['AccountNo'] = value

    def outcome_mapping(self, outcome):
        if (0 == outcome):
            return 'Processed'
        elif (1 == outcome):
            return 'Inconsistent  with history'
        elif (2 == outcome):
            return 'Insufficient Funds'
        else:
            return 'Unknown Operation'

    def MakeUniqueRequest(self, bank_name, account_no, sequence_no):
        unique_Id = ((((bank_name + '.') + str(self.client_no)) + '.') + str(sequence_no))
        return unique_Id

    def SendRequest(self, bank_name, operationType, account_no, amount, sequence_no):
        request_id = self.MakeUniqueRequest(bank_name, account_no, sequence_no)
        req = Request(amount, account_no, operationType, request_id, bank_name)
        self.SendPacket(bank_name, req)
        return request_id

    def SendPacket(self, bank_name, request):
        if (request.operationType == 2):
            tail = self.client_server_details[bank_name]['Tail']
            self.logger.info('Sending query to the tail')
            self._send(('Request', self.client, request), tail)
        else:
            head = self.client_server_details[bank_name]['Head']
            self.logger.info('Sending Update request to head')
            self._send(('Request', self.client, request), head)

    def InitializeLogger(self, Name):
        self.logger = logging.getLogger(Name)
        hdlr = logging.FileHandler((Name + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def operation_type(self, operation):
        if (operation == 0):
            return 'Withdraw'
        elif (operation == 1):
            return 'Deposit'
        elif (operation == 2):
            return 'Query'
        else:
            return 'Unknown Operation'

    def threaded_function(self, arg):
        request = self.requests[self.client_no]
        for (key, value) in request.items():
            no_of_retries = self.retry
            bank_name = value['bank_name']
            accountNo = int(value['accountNo'])
            operation_Type = int(value['operation_Type'])
            amount = int(value['amount'])
            self.sequence_no = int(value['sequence_no'])
            self.logger.info(((((((((('Sending Request Packet ' + bank_name) + ' AccountNo = ') + str(accountNo)) + ' Operation Type = ') + self.operation_type(operation_Type)) + ' Amount = ') + str(amount)) + ' SequenceNo = ') + str(self.sequence_no)))
            request_id = self.SendRequest(bank_name, operation_Type, accountNo, amount, self.sequence_no)
            while (not (no_of_retries == 0)):
                rep = None

                def ExistentialOpExpr_0():
                    nonlocal rep
                    for (_, _, (_ConstantPattern19_, rep)) in self._ClientReceivedEvent_2:
                        if (_ConstantPattern19_ == 'Response'):
                            if (rep.request_id == request_id):
                                return True
                    return False
                _st_label_88 = 0
                self._timer_start()
                while (_st_label_88 == 0):
                    _st_label_88+=1
                    if ExistentialOpExpr_0():
                        self.logger.info('Finally Sent and Got response')
                        self.logger.info(((((((('Received Response  Request = ' + rep.request_id) + ' Account No = ') + str(rep.account_no)) + ' Outcome = ') + self.outcome_mapping(rep.outcome)) + ' New_Balance = ') + str(rep.balance)))
                        no_of_retries = self.retry
                        time.sleep(self.sleepbetweenrequests)
                        break
                        _st_label_88+=1
                    elif self._timer_expired:
                        self.logger.warning((('Timeout happened for ' + str(request_id)) + ' so resending the request'))
                        no_of_retries-=1
                        request_id = self.SendRequest(bank_name, operation_Type, accountNo, amount, self.sequence_no)
                        _st_label_88+=1
                    else:
                        super()._label('_st_label_88', block=True, timeout=self.timeout)
                        _st_label_88-=1
                else:
                    if (_st_label_88 != 2):
                        continue
                if (_st_label_88 != 2):
                    break

    def _Client_handler_0(self, Server, key, str):
        if (str == 'Head'):
            self.logger.info('Setting New Head for client ')
            self.client_server_details[key]['Head'] = Server
        elif (str == 'Tail'):
            self.logger.info('Setting New Tail for Client')
            self.client_server_details[key]['Tail'] = Server
    _Client_handler_0._labels = None
    _Client_handler_0._notlabels = None

    def _Client_handler_1(self, newServer, key):
        self.logger.info((' Got info Extension info in client new tail ' + str(newServer)))
        self.client_server_details[key]['Tail'] = newServer
    _Client_handler_1._labels = None
    _Client_handler_1._notlabels = None
