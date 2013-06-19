#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     re_connection.py
#
#     Copyright 2013 RoboEarth
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#     \author/s: Mayank Singh
#
#

import os
import unicodedata
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

# RoboEarth URL
DOMAIN = "http://localhost:8000/"
BINARY_ROOT = DOMAIN+"data"
# location of binary data
UPLOAD_DIR = "/home/marcus/hadoop"
# Hadoop name node
NAMENODE = "localhost"
NAMENODE_PORT = 9090
# reasoning server
SESAME_SERVER="http://localhost:8080/openrdf-sesame"
# java program to access the reasoning server
SESAME_CONNECTOR="SesameConnector"
SESAME_CONNECTOR_LIBS=".:/home/marcus/workspace/roboearth/SesameConnector:/home/marcus/workspace/roboearth/SesameConnector/lib/*"

# some pre-defined error types
ERROR_TYPES = {0 : "UNKNOWN ERROR",
               1 : "DATA NOT VALID ERROR",
               2 : "HADOOP ERROR",
               3 : "Sesame ERROR"}

# Path to user database
DB_PATH = '/home/marcus/workspace/py_re_comm/user.db'

# some pre-defined exceptions
class DBException(Exception):
    def __str__(self):
        return repr(self.args[0])

class DBWriteErrorException(Exception):
    def __str__(self):
        return repr(self.args[0])

class DBReadErrorException(Exception):
    def __str__(self):
        return repr(self.args[0])

class NoDBEntryFoundException(Exception):
    def __str__(self):
        return repr(self.args[0])


def openDBTransport():
    """
    Open trasport to access hbase by the Thrift interface
    """
    try:
        transport = TSocket.TSocket(NAMENODE, NAMENODE_PORT)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Hbase.Client(protocol)
        transport.open()
        return { 'client' : client, 'transport' : transport }
    except Exception, err:
        raise DBException("Hbase connection failed: " + err.__str__())


def closeDBTransport(transport):
    """
    Close hbase transport
    """

    transport['transport'].close()


def replace_unicode(string):

    string = string.replace(u'\xf6', 'oe').replace(u'\xd6', 'Oe').replace(u'\xe4', 'ae').replace(u'\xc4', 'Ae').replace(u'\xfc', 'ue').replace(u'\xdc', 'Ue').replace(u'\xdf','ss')

    return unicodedata.normalize('NFKD', string).encode('ascii','ignore')

def decode(byte):
    return byte+256 if byte<0 else byte

def int8tofile(bytess):
    g = [chr(decode(k)) for k in bytess]
    return g

def calc_rating(old_rating, new_rating):    
    if new_rating > 10:
        new_rating = 10
    if new_rating < 0:
        new_rating = 0

    return old_rating + (new_rating - old_rating) / 10

