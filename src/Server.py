import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('Request'), da.pat.FreePattern('parameter'), da.pat.FreePattern('req')])
PatternExpr_1 = da.pat.FreePattern('client')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('Acknowledgment'), da.pat.FreePattern('req')])
PatternExpr_3 = da.pat.TuplePattern([da.pat.ConstantPattern('Failure'), da.pat.FreePattern('server'), da.pat.FreePattern('str')])
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('SentArray'), da.pat.FreePattern('sentarray')])
PatternExpr_5 = da.pat.FreePattern('server')
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('CorrectedSentArray'), da.pat.FreePattern('tempsentarray')])
PatternExpr_7 = da.pat.TuplePattern([da.pat.ConstantPattern('YourPredeccesor'), da.pat.FreePattern('predeccesor_server')])
PatternExpr_8 = da.pat.TuplePattern([da.pat.ConstantPattern('GiveMeYourState')])
PatternExpr_9 = da.pat.FreePattern('server')
PatternExpr_10 = da.pat.TuplePattern([da.pat.ConstantPattern('Extend'), da.pat.FreePattern('key'), da.pat.FreePattern('newServer')])
PatternExpr_11 = da.pat.FreePattern('master')
PatternExpr_12 = da.pat.TuplePattern([da.pat.ConstantPattern('ForwardState'), da.pat.FreePattern('account_no'), da.pat.FreePattern('account'), da.pat.FreePattern('Temporary_Transaction_Processed'), da.pat.FreePattern('j'), da.pat.FreePattern('length'), da.pat.FreePattern('previous_sent')])
PatternExpr_13 = da.pat.FreePattern('server')
import sys
import os
import logging
import time
from threading import Thread
from time import sleep
from datatypes import Request
from datatypes import Reply


class Server(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_0]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_1', PatternExpr_2, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_1]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_2', PatternExpr_3, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_2]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_3', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_3]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_4', PatternExpr_6, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_4]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_5', PatternExpr_7, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_5]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_6', PatternExpr_8, sources=[PatternExpr_9], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_6]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_7', PatternExpr_10, sources=[PatternExpr_11], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_7]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_8', PatternExpr_12, sources=[PatternExpr_13], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_8])])

    def main(self):
        self.InitializeLogger(
        str(
        os.getpid()))
        self.logger.info(((((((('Log File for Server for bank ' + str(self.bank_name)) + 'With Id ') + str(self.id)) + ' Lifetime ') + str(self.lifetime)) + ' Failure ') + str(self.failureUponfailure)))
        self.log_head_tail()
        thread = Thread(target=self.threaded_function, args=(4,))
        thread.start()
        _st_label_25 = 0
        while (_st_label_25 == 0):
            _st_label_25+=1
            if ((self.NoOfMessagesSent == self.lifetime) or (self.flag == 1)):
                _st_label_25+=1
            else:
                super()._label('_st_label_25', block=True)
                _st_label_25-=1
        self.logger.info((' ## Message limit might have reached till now  or flag = 1 ## ' + str(self.NoOfMessagesSent)))
        self.logger.info(' EXITING')

    def setup(self, predeccesor, succesor, bank_name, master, server_number, lifetime, failureUponfailure, simulatepacketloss):
        self.predeccesor = predeccesor
        self.master = master
        self.bank_name = bank_name
        self.simulatepacketloss = simulatepacketloss
        self.succesor = succesor
        self.server_number = server_number
        self.lifetime = lifetime
        self.failureUponfailure = failureUponfailure
        self.AllInfo = dict()
        self.logger = None
        self.Transaction_Processed = dict()
        self.bank_name = bank_name
        self.sent = dict()
        self.NoOfMessagesSent = 0
        self.flag = 0

    def threaded_function(self, arg):
        while 1:
            self._send(('HeartBeat', self.id, self.bank_name), self.master)
            time.sleep(1)

    def FixSentArrayForTail(self):
        self.logger.info('  ######## Stabilizing the tail by clearing its sent array  ##########')
        for (key, value) in self.sent.items():
            req = value['RequestObject']
            clientToSend = value['Client']
            self.logger.info((' Sending response For key ' + str(key)))
            reply = self.Transaction_Processed[key]['Reply']
            self._send(('Response', reply), clientToSend)
            self._send(('Acknowledgment', req), self.predeccesor)

    def FixSentArray(self, key, sentarray):
        req = sentarray['RequestObject']
        clientToSend = sentarray['Client']
        if ((not (key in self.sent)) and (not (key in self.Transaction_Processed))):
            self.logger.info((' This key not there so adding ' + str(key)))
            self.FixProcessRequest(req, clientToSend)
        else:
            self.logger.info((' Ignoring this request since already there ' + str(key)))

    def SendCorrectedSentArrayToSuccessor(self, sentarray, successor_server):
        tempSentArray = dict()
        for (key, value) in self.sent.items():
            if (not (key in sentarray)):
                self.logger.info((((' This key not there so adding  key= ' + str(key)) + ' value = ') + str(value)))
                tempSentArray[key] = value
        self.logger.info('** Learnt which elements to send **')
        if (self.failureUponfailure == 0):
            self.logger.info(('Sending to successor ' + str(successor_server)))
            self._send(('CorrectedSentArray', tempSentArray), successor_server)
        else:
            self.flag = 1
            self.logger.info(' Failure Flag one going out')

    def UpdateSuccessorSentArray(self, tempsentArray):
        for (key, value) in tempsentArray.items():
            req = value['RequestObject']
            clientToSend = value['Client']
            if (not (key in self.Transaction_Processed)):
                self.logger.info((' Not there in transaction Proccesed ' + str(key)))
                self.FixProcessRequest(req, clientToSend)
            else:
                self.logger.info((' Was there in Trasaction Processed so sending Acknowlegment ' + str(key)))
                self._send(('Acknowledgment', req), self.predeccesor)

    def FixProcessRequest(self, req, clientToSend):
        rep = self.process_request(req)
        if (self.succesor == None):
            self.logger.info('Sending Reply for update operation')
            self._send(('Response', rep), clientToSend)
            self.logger.info(('Sending Acknowledgment from tail to predeccesor with object' + str(req)))
            self._send(('Acknowledgment', req), self.predeccesor)
        else:
            self._send(('Request', clientToSend, req), self.succesor)
            self.sent[req.request_id] = {'RequestObject': req, 'Client': clientToSend}

    def SendMiddleServerSentRequests(self):
        for (key, value) in self.sent.items():
            self.logger.info(('### Sending ### key =  ' + str(key)))
            self._send(('SentArray', key, self.sent[key]), self.succesor)

    def SendSentArrayToPredecceesor(self, predeccesor_server):
        self.logger.info(('Sending to Predeccesor the Sent Array  ' + str(predeccesor_server)))
        self._send(('SentArray', self.sent), predeccesor_server)

    def ForwardState(self, server):
        self.logger.info(((' ## Forwarding the state to = ' + str(server)) + ' ### '))
        length = len(self.AllInfo)
        self.logger.info((' Self.Info length = ' + str(length)))
        j = 0
        for accout_no in self.AllInfo:
            account = self.AllInfo[accout_no]
            self.logger.info((((' Sending for account = ' + str(accout_no)) + ' Value = ') + str(account)))
            Temporary_Transaction_Processed = dict()
            for request_id in self.Transaction_Processed:
                if (accout_no == self.Transaction_Processed[request_id]['account_no']):
                    Temporary_Transaction_Processed[request_id] = self.Transaction_Processed[request_id]
            j = (j + 1)
            self._send(('ForwardState', accout_no, account, Temporary_Transaction_Processed, j, length, self.sent), server)
        self.logger.info('  ### State Forwarded ###  ')

    def create_and_initialize_account(self, account_no, initial_balance, bank_name):
        Account = {'balance': initial_balance, 'bank_name': bank_name}
        self.AllInfo[account_no] = Account

    def withdraw(self, account_no, balance):
        account = self.AllInfo[account_no]
        if (account['balance'] < balance):
            print('In sufficient balance for account_no = ', account_no)
            return 0
        self.logger.info(((('Withdrawing for accountno = ' + str(account_no)) + ' balance = ') + str(balance)))
        account['balance'] = (account['balance'] - balance)
        return 1

    def deposit(self, account_no, amount):
        self.logger.info(((('Depositing for accountno = ' + str(account_no)) + ' balance = ') + str(amount)))
        account = self.AllInfo[account_no]
        account['balance'] = (account['balance'] + amount)
        return account['balance']

    def query(self, account_no):
        self.logger.info(('Querying for accountno = ' + str(account_no)))
        account = self.AllInfo[account_no]
        return account['balance']

    def get_balance(self, account_no):
        account = self.AllInfo[account_no]
        return account['balance']

    def log_head_tail(self):
        if ((self.predeccesor == None) and (self.succesor == None)):
            self.logger.info('Extending Server')
        elif (self.predeccesor == None):
            self.logger.info('Head Server')
        elif (self.succesor == None):
            self.logger.info('Tail Server')
        else:
            self.logger.info('Middle Server')

    def process_request(self, request):
        if (self.AllInfo.get(request.accountNo) == None):
            self.logger.info('Account was not there.. So initializing ')
            self.create_and_initialize_account(request.accountNo, 0, request.bank_name)
        self.logger.info(('Current Request  ' + request.request_id))
        if (request.request_id in self.Transaction_Processed):
            if ((request.accountNo == self.Transaction_Processed[request.request_id]['account_no']) and (request.operationType == self.Transaction_Processed[request.request_id]['operation_Type']) and (request.amount == self.Transaction_Processed[request.request_id]['amount'])):
                self.logger.info((('Request Already there ' + str(request.request_id)) + ' So sending the previous reply '))
                res = self.Transaction_Processed[request.request_id]['Reply']
                return res
            else:
                self.logger.info(('Inconsistent with history ' + str(request.request_id)))
                return Reply(request.request_id, 1, request.amount, request.accountNo)
        if (request.operationType == 0):
            ret = self.withdraw(request.accountNo, request.amount)
            new_balance = self.get_balance(request.accountNo)
            if (ret == 1):
                res = Reply(request.request_id, 0, new_balance, request.accountNo)
                self.Transaction_Processed[request.request_id] = {'Reply': res, 'account_no': request.accountNo, 'operation_Type': request.operationType, 'amount': request.amount}
                return res
            else:
                self.logger.info(('Insufficient Funds for request_Id ' + str(request.request_id)))
                res = Reply(request.request_id, 2, new_balance, request.accountNo)
                return res
        elif (request.operationType == 1):
            new_balance = self.deposit(request.accountNo, request.amount)
            res = Reply(request.request_id, 0, new_balance, request.accountNo)
            self.Transaction_Processed[request.request_id] = {'Reply': res, 'account_no': request.accountNo, 'operation_Type': request.operationType, 'amount': request.amount}
            return res
        elif (request.operationType == 2):
            actual_balance = self.query(request.accountNo)
            res = Reply(request.request_id, 0, actual_balance, request.accountNo)
            return res
        else:
            return None

    def InitializeLogger(self, Name):
        self.logger = logging.getLogger(Name)
        hdlr = logging.FileHandler((Name + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def _Server_handler_0(self, parameter, client, req):
        self.NoOfMessagesSent = (self.NoOfMessagesSent + 1)
        if (self.simulatepacketloss == 0):
            rep = self.process_request(req)
            if (self.predeccesor == None):
                parameter = client
            clientToSend = parameter
            if (self.succesor == None):
                if (req.operationType == 2):
                    self.logger.info('Sending Reply for query operation')
                    self._send(('Response', rep), client)
                else:
                    self.logger.info('Sending Reply for update operation')
                    self._send(('Response', rep), parameter)
                    self.logger.info(('Sending Acknowledgment from tail to predeccesor with object' + str(req)))
                    self._send(('Acknowledgment', req), self.predeccesor)
            else:
                self._send(('Request', parameter, req), self.succesor)
                self.sent[req.request_id] = {'RequestObject': req, 'Client': clientToSend}
        elif (self.simulatepacketloss == 1):
            self.simulatepacketloss = 0
    _Server_handler_0._labels = None
    _Server_handler_0._notlabels = None

    def _Server_handler_1(self, req):
        self.sent.pop(req.request_id)
        if (self.predeccesor == None):
            self.logger.info((' Request removed from all sents ' + str(req.request_id)))
        else:
            self._send(('Acknowledgment', req), self.predeccesor)
        self.logger.info((' Sent list after the deleting      ' + str(self.sent)))
    _Server_handler_1._labels = None
    _Server_handler_1._notlabels = None

    def _Server_handler_2(self, server, str):
        if (str == 'Head'):
            self.logger.info(' ### This is the New Head  ### ')
            self.predeccesor = None
        elif (str == 'Tail'):
            self.logger.info(' ### This is the New Tail ### ')
            self.succesor = None
            self.FixSentArrayForTail()
        elif (str == 'Successor'):
            self.succesor = server
            self.logger.info('  ###  New predeccesor with succesor  ###')
        elif (str == 'Predeccesor'):
            self.predeccesor = server
            self.logger.info(' ### New succesor with predeccesor ### ')
            self.SendSentArrayToPredecceesor(server)
        elif (str == 'ThisIsNewTail'):
            self.logger.info(' Got this is the new tail message')
            self.predeccesor = server
            self._send(('GiveMeYourState',), server)
        else:
            self.logger.info(' ## got nothing ##')
    _Server_handler_2._labels = None
    _Server_handler_2._notlabels = None

    def _Server_handler_3(self, sentarray, server):
        self.logger.info((' Got sent array of successor ' + str(server)))
        self.logger.info(' #######################')
        self.logger.info(('Received array ' + str(sentarray)))
        self.logger.info(('Current Sent Array ' + str(self.sent)))
        self.logger.info(' #######################')
        self.SendCorrectedSentArrayToSuccessor(sentarray, server)
    _Server_handler_3._labels = None
    _Server_handler_3._notlabels = None

    def _Server_handler_4(self, tempsentarray):
        self.logger.info((' Got Corrected Sent Array  ' + str(tempsentarray)))
        self.logger.info('** Learnt from predeccesor what to proccess and what not to **')
        if (self.failureUponfailure == 0):
            self.UpdateSuccessorSentArray(tempsentarray)
        else:
            self.flag = 1
            self.logger.info(' Failure Flag one going out')
    _Server_handler_4._labels = None
    _Server_handler_4._notlabels = None

    def _Server_handler_5(self, predeccesor_server):
        self.logger.info((' In extending server got predeccesor_server = ' + str(predeccesor_server)))
        self._send(('GiveMeYourState',), predeccesor_server)
    _Server_handler_5._labels = None
    _Server_handler_5._notlabels = None

    def _Server_handler_6(self, server):
        self.logger.info((' Got Give me Your State from = ' + str(server)))
        if (self.failureUponfailure == 0):
            self.ForwardState(server)
            self.succesor = server
        else:
            self.flag = 1
            self.logger.info('failureUponfailure = 1 setting Flag = 1 and exiting ')
    _Server_handler_6._labels = None
    _Server_handler_6._notlabels = None

    def _Server_handler_7(self, key, master, newServer):
        self.logger.info('Got Extendng Making this as middle server')
        self.succesor = newServer
    _Server_handler_7._labels = None
    _Server_handler_7._notlabels = None

    def _Server_handler_8(self, previous_sent, server, account_no, Temporary_Transaction_Processed, length, account, j):
        self.logger.info((' Got Previous Tails State for account_no ' + str(account_no)))
        self.logger.info((((' Got Account ' + str(account)) + ' Transaction Proccessed ') + str(Temporary_Transaction_Processed)))
        self.AllInfo[account_no] = account
        for request_id in Temporary_Transaction_Processed:
            self.Transaction_Processed[request_id] = Temporary_Transaction_Processed[request_id]
        if (length == j):
            self.logger.info('############## This is the new tail  #############')
            self.logger.info((' New Transaction_Proccessed ' + str(self.Transaction_Processed)))
            self.logger.info((' New All Info ' + str(self.AllInfo)))
            self.logger.info((' New Sent ' + str(self.sent)))
            self.logger.info(('SETTING THE PREDECCESOR ' + str(server)))
            self.predeccesor = server
            if (self.failureUponfailure == 0):
                self.logger.info('SENDING TO THE MASTER ')
                self._send(('ExtensionComplete', self.bank_name), self.master)
            else:
                self.logger.info(' Failure Upon Failue  = 1 and setting flag = 1 and exiting')
                self.flag = 1
    _Server_handler_8._labels = None
    _Server_handler_8._notlabels = None
