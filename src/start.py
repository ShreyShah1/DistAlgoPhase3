import da
import sys
from scirpt import Config
import os
import logging
from Server import Server
from Client import Client
from Master import Master

def main():
    logger = logging.getLogger(str(os.getpid()))
    hdlr = logging.FileHandler((str(os.getpid()) + '.log'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    i = 0
    da.api.config(channel='fifo')
    file_name = sys.argv[1]
    config_parameter = Config(file_name)
    total_number_of_banks = config_parameter.bank_count
    total_number_of_client = config_parameter.client_count
    client_access_details = config_parameter.client_access_details
    request_packet = config_parameter.request_packet
    no_of_servers = config_parameter.no_of_servers
    timeout = config_parameter.timeout
    retry = config_parameter.retry
    lifetime_counts = config_parameter.lifetime_counts
    failureUponfailure = config_parameter.failureUponfailure
    extend = config_parameter.extend
    sleepbetweenrequests = config_parameter.sleepbetweenrequests
    simulatepacketloss = config_parameter.simulatepacketloss
    ps_master = da.api.new(Master, num=1)
    all_server_details = dict()
    head_tail_details = dict()
    ps_server_list = list()
    logger.info(('Total number of Banks ' + str(total_number_of_banks)))
    for (key, value) in no_of_servers.items():
        logger.info(('Initializing for bank ' + str(key)))
        logger.info(('The number of servers ' + str(value)))
        ps_server = da.api.new(Server, num=value)
        ps_list = list(ps_server)
        print(
        len(ps_list))
        ps_server_list.extend(ps_list)
        head_tail_details[key] = {'Head': '', 'Tail': ''}
        all_server_details[key] = {}
        servers_list = list()
        alive_count = list()
        all_server_details[key]['Servers'] = servers_list
        all_server_details[key]['Alive_Count'] = alive_count
        all_server_details[key]['Extend_Delay'] = extend[key]['Delay']
        all_server_details[key]['Extend_Flag'] = extend[key]['Flag']
        all_server_details[key]['Extend_FailureUponFailue'] = extend[key]['FailureUponFailue']
        for j in range(len(ps_list)):
            lifetime = lifetime_counts[key][j]
            failure = failureUponfailure[key][j]
            all_server_details[key]['Servers'].append(ps_list[j])
            all_server_details[key]['Alive_Count'].append(0)
            if (j == 0):
                da.api.setup(ps_list[j], [None, ps_list[(j + 1)], key, ps_master, j, lifetime, failure, simulatepacketloss])
                head_tail_details[key]['Head'] = ps_list[j]
            elif (j == (len(ps_list) - 1)):
                da.api.setup(ps_list[j], [ps_list[(j - 1)], None, key, ps_master, j, lifetime, failure, 0])
                head_tail_details[key]['Tail'] = ps_list[j]
            else:
                da.api.setup(ps_list[j], [ps_list[(j - 1)], ps_list[(j + 1)], key, ps_master, j, lifetime, failure, 0])
    ps_client = da.api.new(Client, num=total_number_of_client)
    logger.info(('Total Number of client ' + str(total_number_of_client)))
    ps_client_list = list(ps_client)
    for (key, value) in client_access_details.items():
        details = value
        da.api.setup(ps_client_list[i], [
        int(key), head_tail_details, details, request_packet, timeout, retry, sleepbetweenrequests])
        i = (i + 1)
    da.api.setup(ps_master, [all_server_details, ps_client_list])
    da.api.start(ps_master)
    da.api.start(ps_client)
    da.api.start(ps_server_list)
