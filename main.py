from time import sleep
import logging

import psutil
import requests

logging.basicConfig(filename='cybclient.log', level=logging.DEBUG)

SERVER_URL = 'http://127.0.0.1:5000'

class Client(object):
    def __init__(self):
        """Constructor for Client"""
        logging.info('Client object instantiating')
        self.main_loop()

    def retrieve_processes(self):
        """retrieve all running processes every 5 seconds, noting exceptions etc."""
        logging.info('Retrieving process information')
        processes = []
        for process in psutil.process_iter():
            # get all the processes information
            with process.oneshot():
                pid = process.pid
                if pid == 0:
                    # system idle process for WinNT
                    continue
                name = process.name()
                status = process.status()
                processes.append({
                    'pid': pid,
                    'name': name,
                    'status': status,
                })
        return processes

    def main_loop(self):
        """main loop for client program"""
        logging.info('Entering main loop')
        while(True):
            processes = self.retrieve_processes()
            try:
                r = requests.post(url=SERVER_URL, json=processes)
                if r.ok:
                    logging.debug('Successful post of process data')
                else:
                    logging.debug('Unsuccessful send error for broadcasting process data')
            except requests.exceptions.ConnectionError as e:
                logging.debug('Connection error: {}'.format(e))
            except requests.exceptions.HTTPError as e:
                logging.debug('HTTP Error: {}'.format(e))
            except requests.exceptions.Timeout as e:
                logging.debug('Timeout error: {}'.format(e))
            except requests.exceptions.RequestException as e:
                logging.debug('Unknown other requests error: {}'.format(e))
            finally:
                sleep(5)


if __name__ == '__main__':
    c = Client()