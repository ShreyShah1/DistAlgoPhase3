import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('HeartBeat'), da.pat.FreePattern('id'), da.pat.FreePattern('key')])
PatternExpr_1 = da.pat.FreePattern('server')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('ExtensionComplete'), da.pat.FreePattern('key')])
PatternExpr_3 = da.pat.FreePattern('new_server')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('MASTER_NEVER_TERMINATE'), da.pat.FreePattern(None)])
import sys
import time
import os
import logging
from Server import Server
from threading import Thread


class Master(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._MasterReceivedEvent_2 = []
        self._events.extend([
        da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_0]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_1', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_1]), 
        da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_2', PatternExpr_4, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def main(self):
        self.InitializeLogger(
        str(
        os.getpid()))
        self.logger.info('Log File for Master ')
        for (key, value) in self.all_server_details1.items():
            for j in range(len(self.all_server_details1[key]['Servers'])):
                self.logger.info((((((' For key ' + str(key)) + ' process Id ') + str(value['Servers'][j])) + ' Alive count ') + str(value['Alive_Count'][j])))
        thread = Thread(target=self.ExtendTheChainFunction, args=(4,))
        thread.start()
        while True:
            _st_label_117 = 0
            self._timer_start()
            while (_st_label_117 == 0):
                _st_label_117+=1
                if False:
                    self.logger.info('Inside Await')
                    _st_label_117+=1
                elif self._timer_expired:
                    self.logger.info('Checking For Alive Count')
                    self.Check_Alive_Servers()
                    _st_label_117+=1
                else:
                    super()._label('_st_label_117', block=True, timeout=5)
                    _st_label_117-=1
            else:
                if (_st_label_117 != 2):
                    continue
            if (_st_label_117 != 2):
                break

        def ExistentialOpExpr_0():
            for (_, _, (_ConstantPattern19_, _)) in self._MasterReceivedEvent_2:
                if (_ConstantPattern19_ == 'MASTER_NEVER_TERMINATE'):
                    if True:
                        return True
            return False
        _st_label_121 = 0
        while (_st_label_121 == 0):
            _st_label_121+=1
            if ExistentialOpExpr_0():
                _st_label_121+=1
            else:
                super()._label('_st_label_121', block=True)
                _st_label_121-=1

    def setup(self, all_server_details, client_list):
        self.all_server_details = all_server_details
        self.client_list = client_list
        self.all_server_details1 = all_server_details
        self.logger = None
        self.extend = 0

    def Check_Alive_Servers(self):
        for (key, value) in self.all_server_details1.items():
            listofServers = self.all_server_details1[key]['Servers']
            listofAliveCount = self.all_server_details1[key]['Alive_Count']
            for j in range(len(listofServers)):
                if (listofAliveCount[j] > 0):
                    listofAliveCount[j] = 0
                else:
                    self.logger.info(((((('  ## Found Dead ##: For key ' + str(key)) + ' process Id ') + str(listofServers[j])) + ' Alive count ') + str(listofAliveCount[j])))
                    self.FixChain(key, j)

    def FixChain(self, key, j):
        listofSevers = self.all_server_details1[key]['Servers']
        listofAliveCount = self.all_server_details1[key]['Alive_Count']
        if ((self.extend == 0) or (self.all_server_details1[key]['Extend_FailureUponFailue'] == 1)):
            if (j == 0):
                self.logger.info(('Head Down for key ' + str(key)))
                self.SendServerFailure(listofSevers[(j + 1)], None, 'Head')
                self.SendAllClientsFailureNotice(key, listofSevers[(j + 1)], 'Head')
            elif (j == (len(listofSevers) - 1)):
                self.logger.info(('Tail Down for key ' + str(key)))
                self.SendServerFailure(listofSevers[(j - 1)], None, 'Tail')
                self.SendAllClientsFailureNotice(key, listofSevers[(j - 1)], 'Tail')
            else:
                self.logger.info(('Middle Down for key ' + str(key)))
                self.SendServerFailure(listofSevers[(j - 1)], listofSevers[(j + 1)], 'Middle')
            self.logger.info(('Previous List ' + str(listofSevers)))
            listofSevers.remove(listofSevers[j])
            self.logger.info(('New List ' + str(listofSevers)))
        elif (j == (len(listofSevers) - 2)):
            self.logger.info(('Special case Tail Down for key ' + str(key)))
            self.SendServerFailure(listofSevers[(j - 1)], None, 'Tail')
            self.SendAllClientsFailureNotice(key, listofSevers[(j - 1)], 'Tail')
            self.SendServerFailure(listofSevers[(j + 1)], listofSevers[(j - 1)], 'ThisIsNewTail')
            self.extend = 0
            self.logger.info(('Previous List ' + str(listofSevers)))
            listofSevers.remove(listofSevers[j])
            self.logger.info(('New List ' + str(listofSevers)))
        else:
            self.logger.info(' #### SOME PROBLEM ####')

    def SendAllClientsFailureNotice(self, key, Server, str):
        for j in range(len(self.client_list)):
            self._send(('Failure', key, Server, str), self.client_list[j])

    def SendServerFailure(self, server1, server2, str):
        if (str == 'Middle'):
            self._send(('Failure', server1, 'Predeccesor'), server2)
            self._send(('Failure', server2, 'Successor'), server1)
        elif (str == 'ThisIsNewTail'):
            self.logger.info(' Sending this is the NewTail to server')
            self._send(('Failure', server2, str), server1)
        else:
            self._send(('Failure', None, str), server1)

    def ExtendTheChain(self, key):
        self.logger.info('Here in extend')
        listofServers = self.all_server_details1[key]['Servers']
        listofAliveCount = self.all_server_details1[key]['Alive_Count']
        length = len(listofServers)
        new_server = da.api.new(Server, num=1)
        ps_server_list = list(new_server)
        da.api.setup(new_server, [None, None, key, self.id, length, 1011, self.all_server_details1[key]['Extend_FailureUponFailue'], 0])
        da.api.start(new_server)
        self.extend = 1
        listofServers.append(ps_server_list[0])
        listofAliveCount.append(0)
        self._send(('YourPredeccesor', listofServers[(length - 1)]), new_server)

    def SendServerExtendNotice(self, key, newServer, ServerToSend):
        self.logger.info('Sending for Extend ')
        self._send(('Extend', key, newServer), ServerToSend)

    def SendAllClientExtendNotice(self, key, newServer):
        self.logger.info(' Sending Extension notice to all Clients')
        for j in range(len(self.client_list)):
            self._send(('Extend', key, newServer), self.client_list[j])

    def InitializeLogger(self, Name):
        self.logger = logging.getLogger(Name)
        hdlr = logging.FileHandler((Name + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

    def ExtendTheChainFunction(self, args):
        for (key, value) in self.all_server_details1.items():
            if (self.all_server_details1[key]['Extend_Flag'] == 1):
                self.logger.info((' Extending for bank ' + str(key)))
                delay = self.all_server_details1[key]['Extend_Delay']
                self.logger.info((' Delay is ' + str(delay)))
                time.sleep(delay)
                self.ExtendTheChain(key)

    def _Master_handler_0(self, key, id, server):
        listofServers = self.all_server_details1[key]['Servers']
        listofAliveCount = self.all_server_details1[key]['Alive_Count']
        for j in range(len(listofServers)):
            if (server == listofServers[j]):
                listofAliveCount[j]+=1
    _Master_handler_0._labels = None
    _Master_handler_0._notlabels = None

    def _Master_handler_1(self, new_server, key):
        self.logger.info((' Extention complete from server ' + str(new_server)))
        listofServers = self.all_server_details1[key]['Servers']
        length = len(listofServers)
        self.SendServerExtendNotice(key, new_server, listofServers[(length - 2)])
        self.SendAllClientExtendNotice(key, new_server)
        self.logger.info(' EXTENTION COMPLETE ')
    _Master_handler_1._labels = None
    _Master_handler_1._notlabels = None
