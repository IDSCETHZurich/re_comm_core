#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     transactions/common.py
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
import re_connection
import hdfs_op as hdfs
import hbase_op as hbase
import user_db

roboearth = re_connection

def removeEmptyFolders(path):
    if not os.path.isdir(path):
        return
    
    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)
    
    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0:
        os.rmdir(path)
        
def delete(request):
    try:
        transport = roboearth.openDBTransport()
        client = transport['client']
        scanner = client.scannerOpenWithPrefix("Elements", request["uid"], [ ])
        res = client.scannerGet(scanner)
        
        subscribers = []
        for r in res[0].columns:
            if r.startswith("file:") or r.startswith("info:picture"):
                hdfs.rm_file(res[0].columns[r].value.replace(roboearth.BINARY_ROOT, roboearth.UPLOAD_DIR))
            if r.startswith("subscriber:"):
                subscribers.append(res[0].columns[r].value)
        
        client.scannerClose(scanner)
        
        for subscriber in subscribers:
            scannersub = client.scannerOpenWithPrefix("Subscriptions", subscriber, [ ])
            user = client.scannerGet(scannersub)
            if user:
                uname, table, uid = user[0].row.split('#',2)
                if uid == request["uid"]:
                    hbase.delete_row(table="Subscriptions", rowKey=uname+"#"+table+"#"+uid)        
            client.scannerClose(scannersub)
        
        roboearth.closeDBTransport(transport)
        
        removeEmptyFolders(roboearth.UPLOAD_DIR+'/elements')
        
        hbase.delete_row('Elements', request["uid"])
        hbase.delete_column('Users', request["username"], 'element:'+request["uid"])
        
        return True
    except Exception as e:
        return False
    
def del_element(id, apiKey, transaction):
    username = user_db.get_username(apiKey)
    if not user_db.get_activity(username):
        return False 

    data = transaction.get(query=id, exact=True)
    if not data:
        return False 

    try:
        request = {}
        request["uid"] = id
        request["username"] = username
        delete(request)
    except Exception as e:
        return False
    return True