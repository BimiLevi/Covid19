# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from db.config_db import localHost, localTest

'''
    OR: Enviornment Variables
'''
localHost_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(localHost.username, localHost.password, localHost.host, localHost.port, localHost.dbname)

localTest_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(localTest.username, localTest.password, localTest.host, localTest.port, localTest.dbname)

engine = create_engine(localHost_str, client_encoding='UTF8')





