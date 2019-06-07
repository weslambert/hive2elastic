#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import sys
import json
import time
from config import parser
from thehive4py.api import TheHiveApi
from thehive4py.query import *
from pymemcache.client.base import Client

memcached_host = parser.get('memcached', 'host')
memcached_port = int(parser.get('memcached', 'port'))
memcached_agetime = int(parser.get('memcached', 'agetime'))
memcached_sleeptime = int(parser.get('memcached', 'sleeptime'))
memcached = Client((memcached_host, memcached_port))

hive_url = parser.get('hive', 'url')
hive_key = parser.get('hive', 'apikey')

api = TheHiveApi(hive_url,hive_key)

ioc_query = {"ioc": "true"}
response = api._TheHiveApi__find_rows('/api/case/artifact/_search?nparent=1', query=ioc_query)


def getObservables():
    if response.status_code == 200:
        #print(json.dumps(response.json(), indent=4, sort_keys=True))
        jsondata = response.json()
        for i in jsondata:
            case_id = str(i['case']['_id'])
            case_title = i['case']['title']
            observable_value = i['data']
            observable_type = i['dataType']
            # Memcached
            if observable_value != "":
                memcached_key = observable_type + '-' + observable_value
                memcached.set(memcached_key, case_id, memcached_agetime)
    time.sleep(memcached_sleeptime)
while True:
  getObservables()
