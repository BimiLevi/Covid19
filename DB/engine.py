# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from db.config_db import localHost, localTest, azure


localHost_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(localHost.username, localHost.password, localHost.host, localHost.port, localHost.dbname)

localTest_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(localTest.username, localTest.password, localTest.host, localTest.port, localTest.dbname)

azure_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(azure.username, azure.password, azure.host, azure.port, azure.dbname)

engine = create_engine(localHost_str, encoding = 'utf-8')





