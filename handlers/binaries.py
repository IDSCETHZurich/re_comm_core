#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     handlers/binaries.py
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

import user_db
import sys
sys.path.append('..')

#ROS imports
import roslib; roslib.load_manifest('re_srvs')
from re_srvs import srv
from transactions import objects
import re_connection

roboearth = re_connection

class BinaryHandler(object):
    def upload(self, req):
        api_key = req["api_key"]
        username = user_db.get_username(api_key)
        if not user_db.get_activity(username):
            raise
    
        transport = roboearth.openDBTransport()
        client = transport['client']
        scanner = client.scannerOpenWithPrefix("Elements", req["identifier"].lower(), [ ])
        res = client.scannerGet(scanner)
        client.scannerClose(scanner)
        if res:
            result = objects.upload(req["file"], req["identifier"].lower(), author=username)
        else:
            roboearth.closeDBTransport(transport)
            

        roboearth.closeDBTransport(transport)
        if result:
            return True
        else:
            return False
