#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     apidb_connection.py
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

import sqlite3

from re_connection import DB_PATH

def connect():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    return (c, conn)

def get_username(api_key):
    c, conn = connect()
    t = (api_key,)
    c.execute("select username from db_api_keys where key=?", t)
    api_key = c.fetchone()[0].encode('ascii')
    conn.close()
    return api_key

def get_activity(username):
    c, conn = connect()
    t = (username,)
    c.execute("select is_active from auth_user where username=?", t)
    is_active = c.fetchone()[0]
    conn.close()
    return is_active

