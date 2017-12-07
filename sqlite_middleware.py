#!/usr/bin/env python

# -*- coding: utf-8 -*-

############################################################################
#
#       Licensed under the MIT License (the "License"); you may not use this file
#       except in compliance with the License.  You may obtain a copy of the License
#       in the LICENSE file or at
#
#       https://opensource.org/licenses/MIT
#
#       Unless required by applicable law or agreed to in writing, software
#       distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#       WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#       See the License for the specific language governing permissions and
#       limitations under the License.
#
#        author: fmount <fmount9@autistici.org>
#        version: 0.1
#        company: --
#
#############################################################################


import os
import sys
import json
import sqlite3 as lite
from sqlite3 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
from model import Link, User

from config import CONF

engine = create_engine(CONF.database.sql_engine_prefix + CONF.database.dbname)


def _init_engine(Base):
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    return engine


def _insert_link(link, session):
    session.add(link)
    session.commit()


def _insert_user(user, session):
    session.add(user)
    session.commit()


def _find_object(uid, session):
    result = session.query(Link).filter_by(uuid=uid).all()
    return result


def _get_object(uid, session):
    result = session.query(Link).filter_by(uuid=uid).first()
    return result


def _get_user(username, session):
    result = session.query(User).filter_by(username=username).first()
    return result


#def _get_last_user(session):
#    result = session.query(User).order_by(User.id.desc()).first()
#    return result


def _get_all_users(session):
    result = session.query(User).all()
    return result


def _get_last_object(session, Obj):
    result = session.query(Obj).order_by(Obj.uuid.desc()).first()
    if result is None:
        return 0
    return result.uuid


def _get_all_objects(session):
    result = session.query(Link).all()
    return result


def _delete_object(uid, session, Obj):
    obj = session.query(Obj).filter_by(uuid=uid).first()
    session.delete(obj)
    session.commit()
    return obj


def _clear_table_by_name(Base, session, tname):
    for table in reversed(Base.metadata.sorted_tables):
        if table.name == tname:
            session.execute(table.delete())
            session.commit()


def _clear_database(Base):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
