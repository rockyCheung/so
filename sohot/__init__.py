from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey,Sequence,create_engine
from sqlalchemy.orm import sessionmaker
from celery import Celery
from sohot.config import Config,setup_logging
import os
root_path = os.path.abspath('..')
curdir = os.path.abspath(os.path.dirname(__file__))
default_conf = root_path+'/conf.yml'
context = Config(default_conf)
setup_logging(config=context)
'''
# declare db engine,table base class,session
'''
engine = create_engine('sqlite:///sohot.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
'''
This transport uses only the BROKER_URL setting, which have to be an SQLAlchemy database URI.
'''
BROKER_URL = 'sqla+sqlite:///sohot.db'

#Database backend settings
CELERY_RESULT_BACKEND = 'db+sqlite:///sohot.db'

# echo enables verbose logging from SQLAlchemy.
CELERY_RESULT_ENGINE_OPTIONS = {'echo': True}

# use custom table names for the database result backend.
CELERY_RESULT_DB_TABLENAMES = {
    'task': 'sohot_tasks',
    'group': 'sohot_group',
}

app = Celery('tasks',backend=CELERY_RESULT_BACKEND, broker=BROKER_URL)