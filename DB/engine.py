# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from DB.config_db import azureParm, localHost


# dbStr = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
#         ''.format(localHost.username, localHost.password, localHost.host, localHost.port, localHost.dbname)

dbStr = 'postgresql+psycopg2://{}:{}@{}:{}/{}' \
        ''.format(azureParm.username, azureParm.password, azureParm.host, azureParm.port, azureParm.dbname)

engine = create_engine(dbStr)





