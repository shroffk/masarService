'''
Created on Jul 28, 2014

@author: shengb
'''
import time
import logging

import pymongo
if pymongo.version_tuple < (2.5):
    raise RuntimeError("Need pymongo version larger than 2.5")

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

__timesformat = "%a, %d %b %Y, %H:%M:%S %Z"


def _setup_masarservice_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    #handler = logging.StreamHandler()
    handler = logging.FileHandler('/var/tmp/masarservice.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

__logger = _setup_masarservice_logger("masarservice")


def conn(**kwds):
    """Connect MASAR Mongo DB server.
    
    :param host: MongoDB server name
    :type host: str
    
    :param port: MongoDB server port number
    :type port: Int
    
    :param db: MongoDB database name
    :type db: str
    
    :returns conn: Mongo DB connection object.
    
    :raises: ConnectionFailure if the connection cannot be made.
    """
    db = kwds.get("db", None)
    host = kwds.get("host", None)
    port = kwds.get("port", None)
    if port is not None:
        port = int(port)
    try:
        conn = MongoClient(host=host, port=port)
        # w=0: disables write acknowledgement
        # w=1: default, provides basic receipt acknowledgment.
        # w>1: Guarantees that write operations have propagated successfully 
        #      to the specified number of replica set members including the primary 
        # j:   confirms that the mongod instance has written the data to the on-disk journal
        conn.write_concern = {'w': 1, 'wtimeout': 1000, 'j': True}
    except ConnectionFailure:
        __logger.exception("MASAR MongoDB (host: %s, port: %s) connection failure on %s"
                           %(host, port, time.strftime(__timesformat)))
        raise
    # print "Open connection to %s on (host: %s, port %s)" % (db, host, port)
    return conn, db


def close(conn):
    if conn.alive():
        conn.close()

