#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     handlers/environments.py
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
from transactions import environments
from transactions import common

#ROS imports
import roslib; roslib.load_manifest('re_srvs')
from re_srvs import srv


class EnvironmentHandler(object):
    def set_environment(self, req):
        try:
            class_ = req.cls
            id_ = req.id
            description = req.description
            environment = req.environment
            api_key = req.apiKey
        
            username = user_db.get_username(api_key)
            if not user_db.get_activity(username):
                raise
            files = {}
            if req.files:
                for file1 in req.files:
                    files[str(file1.name)] = file1

            result = environments.set  (id_=id_,
                                        class_=class_,
                                        author=username,
                                        description=description,
                                        environment=environment,
                                        files=files)
            if result:
                return True
            else:
                return False
        
        except Exception as e:
            print e
            return False
    
    def get_environment(self, req):
        try:
            result = environments.get(query=req.environmentUID, format="json", 
                                      exact=True)
            if result:
                return srv.GetEnvironmentResponse(True, 
                                              result[0]['environments'][0]['environment'], 
                                              [k for k,v in result[0]["files"].items()],
                                              [v['url'] for k,v in result[0]["files"].items()],)
            else:
                return srv.GetEnvironmentResponse(False, '', [], [])
        except Exception as err:
            print err
            return srv.GetEnvironmentResponse(False, '', [], [])
    
    def update_environment(self, req):
        username = user_db.get_username(req.apiKey)
        if not user_db.get_activity(username):
            return False
        
        env = environments.get(query=req.uid, format="json", exact=True)
        if not env: 
            return False
        
        data = {}
        data["description"] = req.description
        data["environment"] = req.environment  
        
        environments.update(id_=req.uid,
                            author=username,
                            data=data)
        return True
    
    def del_environment(self, req):
        return common.del_element(req.environmentUID, req.apiKey, environments)