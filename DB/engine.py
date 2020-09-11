# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from db.config_db import  localHost


# dbStr = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
#         ''.format(localHost.username, localHost.password, localHost.host, localHost.port, localHost.dbname)

dbStr = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(localHost.username, localHost.password, localHost.host, localHost.port, localHost.dbname)

engine = create_engine(dbStr, client_encoding='UTF8')





